# Turta LoRa HAT Helper for Raspbian.
# Distributed under the terms of the MIT license.

# Python Library for TI ADS1018 ADC.
# Version 1.0.0
# Released: November 5th, 2019

# Visit https://docs.turta.io for documentation.

from enum import IntEnum
from time import sleep
import spidev

#Enumerations

#SS: Single-shot conversion start
class SS(IntEnum):
    NO_EFFECT = 0b0
    START     = 0b1

#CH: Input multiplexer configuration (MUX register)
class CH(IntEnum):
    SINGLE_1         = 0b100
    SINGLE_2         = 0b101
    SINGLE_3         = 0b110
    SINGLE_4         = 0b111
    DIFFERENTIAL_1_2 = 0b000
    DIFFERENTIAL_3_4 = 0b011

#PGA: Programmable gain amplifier configuration
class PGA(IntEnum):
    FSR_4_096 = 0b001
    FSR_2_048 = 0b010
    FSR_1_024 = 0b011
    FSR_0_512 = 0b100
    FSR_0_256 = 0b101

#MODE: Device operating mode
class MODE(IntEnum):
    CONTINUOUS  = 0b0
    SINGLE_SHOT = 0b1

#DR: Data rate
class DR(IntEnum):
    SPS_128  = 0b000
    SPS_250  = 0b001
    SPS_490  = 0b010
    SPS_920  = 0b011
    SPS_1600 = 0b100
    SPS_2400 = 0b101
    SPS_3300 = 0b110

#TS_MODE: Temperature sensor mode
class TS_MODE(IntEnum):
    ADC = 0b0
    TS  = 0b1

#PULL_UP_EN: Pullup enable
class PULL_UP_EN(IntEnum):
    DIBABLE = 0b0
    ENABLE  = 0b1

#NOP: No operation
class NOP(IntEnum):
    INVALID = 0b00
    VALID   = 0b01

class ADC(object):
    "ADS1018 Analog-to-Digital Converter."

    #Variables
    is_initialized = False
    conf_h = None
    conf_l = None
    current_channel = None

    #SPI Device
    spi = None

    #Initialization

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)                 #Bus 0, Device 0
        self.spi.max_speed_hz = 1000000     #1MHz
        self.spi.mode = 0b01                #CPOL 0, CHPA 1
        self.spi.bits_per_word = 8          #8 Bits per word
        self._set_initial_settings()
        self.is_initialized = True
        return

    #Device Configuration

    def _set_initial_settings(self):
        """Sets default configuration."""

        self.config(CH.SINGLE_1, PGA.FSR_4_096, MODE.CONTINUOUS, DR.SPS_250, TS_MODE.ADC)
        return

    def config(self, ch, pga, mode, dr, ts_mode):
        """Configures the device.

        Parameters:
        ch (CH): Input channel (Input multiplexer configuration)
        pga (PGA): Programmable gain amplifier configuration
        mode (MODE): Device operating mode
        dr (DR): Data rate
        ts_mode (TS_MODE): Temperature sensor mode"""

        if ch not in CH:
            raise ValueError('ch is not a member of CH.')

        if pga not in PGA:
            raise ValueError('pga is not a member of PGA.')

        if mode not in MODE:
            raise ValueError('mode is not a member of MODE.')

        if dr not in DR:
            raise ValueError('dr is not a member of DR.')

        if ts_mode not in TS_MODE:
            raise ValueError('ts_mode is not a member of TS_MODE.')

        # Set config
        self.conf_h = ch << 4 | pga << 1 | mode
        self.conf_l = dr << 5 | ts_mode << 4 | PULL_UP_EN.ENABLE << 3 | NOP.VALID << 1 | 0b1
        
        # Send config
        self.spi.xfer2([self.conf_h, self.conf_l])
        self.current_channel = ch
        sleep(0.015)

        return

    #ADC Read Methods

    def read(self, ch):
        """Reads the analog value.

        Parameters:
        ch (CH): Analog input channel

        Returns:
        int: Analog readout"""

        if ch not in CH:
            raise ValueError('ch is not a member of CH.')

        #Clear MUX and TS_MODE
        self.conf_h &= 0x8F
        self.conf_l &= 0xEB

        #Set config
        self.conf_h |= SS.START << 7 | ch << 4

        #Wait for conversion if channel is changed
        if(self.current_channel != ch):
            self.spi.xfer2([self.conf_h, self.conf_l])
            self.current_channel = ch
            sleep(0.015)

        #Read conversion
        conv = self.spi.xfer2([self.conf_h, self.conf_l])
        return conv [0] << 4 | conv[1] >> 4

    def read_temperature(self, fahrenheit = False):
        """Reads the internal IC temperature.

        Parameters:
        fahrenheit (bool): True for Fahrenheit output, False for Celcius output (False is default)

        Returns:
        float: Internal IC temperature"""

        #Enable temperature sensor mode
        self.conf_l |= 0x10
        self.spi.xfer2([self.conf_h, self.conf_l])
        sleep(0.015)
        
        #Read conversion
        conv = self.spi.xfer2([self.conf_h, self.conf_l])
        conv2 = conv [0] << 4 | conv[1] >> 4

        #Disable temperature sensor mode
        self.conf_l &= 0xEF
        self.spi.xfer2([self.conf_h, self.conf_l])

        #Convert reading to temperature
        if (conv2 >> 15 == 0):
            temp = conv2 * 0.125
        else:
            temp = ((conv2 ^ 65535) - 1)  * -0.125

        #Convert to Fahrenheit if requested
        if (fahrenheit):
            temp = (temp * 1.8) + 32

        return temp

    #Disposal

    def __del__(self):
        """Releases the resources."""

        try:
            if self.is_initialized:
                self.spi.close()
                del self.is_initialized
        except:
            pass
