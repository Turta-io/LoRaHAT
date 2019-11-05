# Turta LoRa HAT Helper for Raspbian.
# Distributed under the terms of the MIT license.

# Python Library for Microchip RN2903A/RN2483A LoRa Module.
# Version 1.0.0
# Released: November 5th, 2019

# Visit https://docs.turta.io for documentation.

from enum import Enum
from time import sleep
import serial

#Enumerations

#CONFIG_MODES: Auto configuration modes for initialization
class CONFIG_MODES(Enum):
    NONE    = 0
    LORA_RX = 1
    LORA_TX = 2

#REGIONS: LoRa Module regions
class REGIONS(Enum):
    US_RN2903 = 0
    EU_RN2483 = 1

#COMMANDS: Command types
class CMD_TYPES(Enum):
    SYS       = "sys"
    SYS_SET   = "sys set"
    SYS_GET   = "sys get"
    MAC       = "mac"
    MAC_SET   = "mac set"
    MAC_GET   = "mac get"
    RADIO     = "radio"
    RADIO_SET = "radio set"
    RADIO_GET = "radio get"
    RADIO_RX  = "radio rx"
    RADIO_TX  = "radio tx"

#LEDs: Status LEDs
class LEDS(Enum):
    CON = "GPIO2"
    ACT = "GPIO1"
    ERR = "GPIO0"

#LED STATES: LED States
class LED_STATES(Enum):
    ON  = "0"
    OFF = "1"

#MODES: Operating modes
class RADIO_MODES(Enum):
    LORA = "lora"
    FSK  = "fsk"

#UPLINK PAYLOAD TYPES: Uplink payload types
class UPLINK_PAYLOAD_TYPES(Enum):
    CONFIRMED   = "cnf"
    UNCONFIRMED = "uncnf"

#JOIN_PROCEDURE_TYPES: Join procedure types
class JOIN_PROCEDURE_TYPES(Enum):
    OTAA = "otaa"
    ABP  = "abp"

#AR_STATES: Automatic reply states
class AR_STATES(Enum):
    ON  = "on"
    OFF = "off"

#CH_STATUS: Ch Status
class CH_STATUS(Enum):
    ON  = "on"
    OFF = "off"

#DEVICE_CLASS: LoRaWAN Device classes
class DEVICE_CLASS(Enum):
    A = "a"
    C = "c"

#MCAST_STATES: Multicast states
class MCAST_STATES(Enum):
    ON  = "on"
    OFF = "off"

#EU_FREQ_BANDS: Frequency bands for the EU version
class EU_FREQ_BANDS(Enum):
    NONE = ""
    F_433_MHZ = "433"
    F_868_MHZ = "868"

#FREQUENCIES: Frequencies in 600kHz steps
class FREQUENCIES(Enum):
    F_923_3_MHZ = "923300000"
    F_923_9_MHZ = "923900000"
    F_924_5_MHZ = "924500000"
    F_925_1_MHZ = "925100000"
    F_925_7_MHZ = "925700000"
    F_926_3_MHZ = "926300000"
    F_926_9_MHZ = "926900000"
    F_927_5_MHZ = "927500000"

#CW_MODES: Continuous wave modes
class CW_MODES(Enum):
    ON  = "on"
    OFF = "off"

#FREQ_BANDS: Frequency bands in kHz
class FREQ_BANDS(Enum):
    F_250_0_KHZ = "250"
    F_125_0_KHZ = "125"
    F_62_5_KHZ  = "62.5"
    F_31_3_KHZ  = "31.3"
    F_15_6_KHZ  = "15.6"
    F_7_8_KHZ   = "7.8"
    F_3_9_KHZ   = "3.9"
    F_200_0_KHZ = "200"
    F_100_0_KHZ = "100"
    F_50_0_KHZ  = "50"
    F_25_0_KHZ  = "25"
    F_12_5_KHZ  = "12.5"
    F_6_3_KHZ   = "6.3"
    F_3_1_KHZ   = "3.1"
    F_166_7_KHZ = "166.7"
    F_83_3_KHZ  = "83.3"
    F_41_7_KHZ  = "41.7"
    F_20_8_KHZ  = "20.8"
    F_10_4_KHZ  = "10.4"
    F_5_2_KHZ   = "5.2"
    F_2_6_KHZ   = "2.6"

#GFBTS: Gaussian baseband data shaping
class GFBTS(Enum):
    G_NONE = "none"
    G_1_0  = "1.0"
    G_0_5  = "0.5"
    G_0_3  = "0.3"

#RADIO_BW: Operating radio bandwidth in kHz
class RADIO_BW(Enum):
    BW_125 = "125"
    BW_250 = "250"
    BW_500 = "500"

#CODING_RATES: Coding rates
class CODING_RATES(Enum):
    R_4_5 = "4/5"
    R_4_6 = "4/6"
    R_4_7 = "4/7"
    R_4_8 = "4/8"

#CRC_HEADER_STATES: CRC Header states
class CRC_HEADER_STATES(Enum):
    ON  = "on"
    OFF = "off"

#IQI_STATES: Invert IQ states
class IQI_STATES(Enum):
    ON  = "on"
    OFF = "off"

#SPREADING_FACTORS: Spreading Factors
class SPREADING_FACTORS(Enum):
    SF7  = "sf7"
    SF8  = "sf8"
    SF9  = "sf9"
    SF10 = "sf10"
    SF11 = "sf11"
    SF12 = "sf12"   

class RN2XX3:
    """Microchip RN2XX3 LoRa Module"""

    #UART Device
    sp = serial.Serial('/dev/serial0', 57600, timeout=2, write_timeout=2)

    #Variables
    auto = CONFIG_MODES.NONE
    err_on = False

    #UART Communication

    def _write_data(self, cmd_type, data):
        """Writes data to the UART device.

        Parameters:
        cmd_type (str): Command type
        data (str): Payload to send
        
        Returns:
        str: Response from the device"""

        wb = str(cmd_type.value + " " + ' '.join([str(e) for e in data]))

        self.sp.write((wb + "\r\n").encode("utf-8"))
        res = self.sp.readline()[0:-2].decode("utf-8")
        return res if res is not None else "no_response"

    def _read_data(self, cmd_type, data):
        """Reads data from the UART device.

        Parameters:
        cmd_type (str): Command type
        data (str): Payload to send

        Returns:
        str: Response from the device"""

        rb = str(cmd_type.value + " " + ' '.join([str(e) for e in data]))

        self.sp.write((rb + "\r\n").encode("utf-8"))
        res = self.sp.readline()[0:-2].decode("utf-8")
        return res if res is not None else "no_response"

    def check_data(self):
        """Checks the serial port buffer for received data.

        Returns:
        str: If auto mode is selected, the function returns received data. If manual mode is selected, it returns the LoRa module's raw output."""

        res = self.sp.readline()[0:-2].decode("utf-8")

        if res is "":
            return None
        else:
            if self.auto == CONFIG_MODES.NONE:
                #No autoconfig, return received data.
                return res
            elif self.auto == CONFIG_MODES.LORA_RX:
                #System is configured as LoRa receiver.
                #Process data for RX mode.
                return self._auto_rx_routine(res)
            else:
                return None

    def check_uart_buffer(self):
        """Checks the serial port buffer for received data.

        Returns:
        str: UART read buffer."""

        res = self.sp.readline()[0:-2].decode("utf-8")

        if res is "":
            return None
        else:
            return res

    def send_uart_data(self, data):
        """Writes data to the UART device.

        Parameters:
        data (str): Payload to send
        
        Returns:
        str: Response from the device"""

        wb = str(cmd_type.value + " " + ' '.join([str(e) for e in data]))

        self.sp.write((wb + "\r\n").encode("utf-8"))
        res = self.sp.readline()[0:-2].decode("utf-8")
        return res if res is not None else "no_response"

    def _auto_rx_routine(self, data):
        """Processes received data.

        Parameters:
        data (str): Received data from the UART

        Returns:
        str: Received data"""

        res = None

        if data == "radio_err":                             #If radio error has occured
            self.set_led(LEDS.CON, LED_STATES.OFF)          #Turn CON LED off
            self.set_led(LEDS.ERR, LED_STATES.ON)           #Turn ERR LED on
            self.radio_rx(0)                                #Restart radio
            self.set_led(LEDS.ERR, LED_STATES.OFF)          #Turn ERR LED off
            self.set_led(LEDS.CON, LED_STATES.ON)           #Turn CON LED on
            return res

        elif data.startswith("radio_rx", 0, 8):             #If a message has received
            self.set_led(LEDS.ACT, LED_STATES.ON)           #Turn ACT LED on
            self.radio_rx(0)                                #Process received data
            res = bytes.fromhex(data[10:]).decode("utf-8")  #Remove "radio_rx  " characters from the buffer
            self.set_led(LEDS.ACT, LED_STATES.OFF)          #Turn ACT LED off
            return res

        else:
            return None

    def send(self, data):
        """Broadcasts data for auto TX mode operation.

        Parameters:
        data (string): Data to send

        Returns:
        str: Response from the LoRa module"""

        data = str(data)
        if len(data) > 255:
            raise ValueError('data length is outside of 0 and 255.')

        res = None
        wb = data.encode("utf-8").hex()
        if self.err_on == True:
            self.err_on = False
            self.set_led(LEDS.ERR, LED_STATES.OFF)
        self.set_led(LEDS.ACT, LED_STATES.ON)
        res = self.radio_tx(wb)
        self.set_led(LEDS.ACT, LED_STATES.OFF)
        if res == "busy" or res == "invalid_param" or res == "err":
            self.err_on = True
            self.set_led(LEDS.ERR, LED_STATES.ON)
        return res

    #Initialization

    def __init__(self, region = REGIONS.US_RN2903, auto_config = CONFIG_MODES.NONE, freq_us = 915000000, freq_eu = 868000000):
        """Initiates the RN2XX3A LoRa module.
        
        Parameters:
        region (REGIONS): LoRa Module region.
        auto_config (CONFIG_MODES): LoRa Module operating mode. NONE is for manual configuration. LORA_TX and LORA_RX are for automatic configuration. (MODES.CONFIG_MODES.NONE is default)
        freq (int): LoRa radio frequency for auto configuration. (Default is 915000000)"""

        if region not in REGIONS:
            raise ValueError('region is not a member of REGIONS.')
        if auto_config not in CONFIG_MODES:
            raise ValueError('auto_config is not a member of CONFIG_MODES.')

        freq = freq_us if region == REGIONS.US_RN2903 else freq_eu

        self._set_initial_settings(auto_config, freq)
        self.is_initialized = True
        sleep(0.5)

    #System Commands (Sys)

    def sys_sleep(self, length):
        """Puts the system to sleep for the specified number of milliseconds.

        Parameters:
        length (int): Number of milliseconds the system is put to sleep (100 to 4294967296)

        Returns:
        str: Response from the device"""

        if length < 100 or length > 4294967296:
            raise ValueError('length is outside of 100 and 4294967296.')
        res = self._write_data(CMD_TYPES.SYS, ["sleep", length])
        return res

    def sys_reset(self):
        """Resets and restarts the LoRa module; stored LoRaWAN protocol settings will be loaded automatically upon reboot.

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.SYS, ["reset"])
        return res

    def sys_factory_reset(self):
        """Resets the module’s configuration data and user EEPROM to factory default values and restarts the module.

        Returns:
        str: Firmware version and release date (RN2XX3 X.Y.Z MMM DD YYYY HH:MM:SS)"""

        res = self._write_data(CMD_TYPES.SYS, ["factoryRESET"])
        return res

    def sys_set_nvm(self, address, data):
        """Allows the user to modify the user EEPROM at <address> with the value supplied by <data>.

        Parameters:
        address (str): hexadecimal number representing user EEPROM address (300 to 3FF)
        data (str): hexadecimal number representing data (00 to FF)

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.SYS_SET, ["nvm", address, data])
        return res
    
    def sys_get_ver(self):
        """Returns the information related to the hardware platform, firmware version, release date and time-stamp on firmware creation.

        Returns:
        str: Firmware version and release date (RN2XX3 X.Y.Z MMM DD YYYY HH:MM:SS)"""

        val = self._read_data(CMD_TYPES.SYS_GET, ["ver"])
        return val

    def sys_get_nvm(self, address):
        """Returns the data stored in the user EEPROM of the RN2XX3 module at the requested <address> location.

        Parameters:
        address (str): Hexadecimal number representing user EEPROM address (300 to 3FF)

        Returns:
        str: 00–FF (hexadecimal value from 00 to FF) if the address is valid"""

        val = self._read_data(CMD_TYPES.SYS_GET, ["nvm", address])
        return val

    def sys_get_vdd(self):
        """Gets the Voltage applied to the VDD pins.

        Returns:
        str: mV Measured on the VDD pins (0 to 3600)"""

        val = self._read_data(CMD_TYPES.SYS_GET, ["vdd"])
        return val

    def sys_get_hweui(self):
        """Reads the preprogrammed EUI node address from the RN2XX3 module.

        Returns:
        str: Hexadecimal number representing the preprogrammed EUI node address"""

        val = self._read_data(CMD_TYPES.SYS_GET, ["hweui"])
        return val

    #LoRaWAN Class A and Class C Protocol Commands (MAC)

    def mac_reset(self, band = EU_FREQ_BANDS.NONE):
        """Sets default values for most of the LoRaWAN parameters. Everything set prior to this command will lose its set value, being reinitialized to the default value, including setting the cryptographic keys to 0.

        Parameters:
        band (EU_FREQ_BANDS): Frequency Band for EU version. Set 'NONE' for US version.

        Returns:
        str: Response from the device"""

        if band not in EU_FREQ_BANDS:
            raise ValueError('band is not a member of EU_FREQ_BANDS.')

        cmd = None
        if band == EU_FREQ_BANDS.NONE:
            cmd = "reset"
        elif band == EU_FREQ_BANDS.F_433_MHZ:
            cmd = "reset 433"
        elif band == EU_FREQ_BANDS.F_868_MHZ:
            cmd = "reset 868"
        res = self._write_data(CMD_TYPES.MAC, [cmd])
        return res

    def mac_tx(self, uplink_payload_type, portno, data):
        """Automatically reset the software LoRaWAN stack and initialize it with the default parameters.

        Parameters:
        uplink_payload_type (UPLINK_PAYLOAD_TYPES): Uplink payload type, either confirmed or unconfirmed
        portno (int): Port number (1 to 223)
        data (str): Hexadecimal value; the length of <data> bytes capable of being transmitted are dependent upon the set data rate

        Returns:
        str: First response from the device; this command may reply with multiple responses"""

        if uplink_payload_type not in UPLINK_PAYLOAD_TYPES:
            raise ValueError('uplink_payload_type is not a member of UPLINK_PAYLOAD_TYPES.')
        if portno < 1 or portno > 223:
            raise ValueError('portno is outside of 1 and 223.')
        res = self._write_data(CMD_TYPES.MAC, ["tx", uplink_payload_type.value, portno, data])
        return res

    def mac_join(self, mode):
        """Informs the RN2XX3 module it should attempt to join the configured network.

        Parameters:
        mode (JOIN_PROCEDURE_TYPES): Join procedure type

        Returns:
        str: First response from the device; this command may reply with two responses"""

        if mode not in JOIN_PROCEDURE_TYPES:
            raise ValueError('mode is not a member of JOIN_PROCEDURE_TYPES.')
        res = self._write_data(CMD_TYPES.MAC, ["join", mode.value])
        return res

    def mac_save(self):
        """Saves the LoRaWAN protocol configuration parameters to the EEPROM. Upon the next system reset the LoRaWAN protocol configuration will be initialized with the last saved parameters.

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC, ["save"])
        return res

    def mac_force_enable(self):
        """Restores the module’s connectivity by allowing it to send data.

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC, ["forceENABLE"])
        return res

    def mac_pause(self):
        """Pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration.

        Returns:
        str: The number of milliseconds the MAC can be paused (0 to 4294967295)"""

        res = self._write_data(CMD_TYPES.MAC, ["pause"])
        return res

    def mac_resume(self):
        """Resumes LoRaWAN stack functionality, in order to continue normal functionality after being paused.

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC, ["resume"])
        return res

    def mac_set_appkey(self, appkey):
        """Sets the application key for the module. The application key is used to derive the security credentials for communication during over-the-air activation.

        Parameters:
        appkey (str): 16-byte hexadecimal number representing the application key

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["appkey", appkey])
        return res

    def mac_set_appskey(self, appsesskey):
        """Sets the application session key for the module. This key provides security for communication between module and application server.

        Parameters:
        appsesskey (str): 16-byte hexadecimal number representing the application session key

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["appskey", appsesskey])
        return res

    def mac_set_ar(self, state):
        """Sets the state of the automatic reply.

        Parameters:
        state (AR_STATES): Automatic reply state

        Returns:
        str: Response from the device"""

        if state not in AR_STATES:
            raise ValueError('state is not a member of AR_STATES.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["ar", state.value])
        return res

    def mac_set_bat(self, level):
        """Sets the battery level required for Device Status Answer frame in use with the LoRaWAN Class A protocol.

        Parameters:
        level (int): The level of the battery (0 to 255) 0 Means external power, 1 means low level, 254 means high level, 255 means the end device was not able to measure the battery level

        Returns:
        str: Response from the device"""

        if level < 0 or level > 255:
            raise ValueError('level is outside of 0 and 255.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["bat", level])
        return res

    def mac_set_ch_freq(self, channel_id, frequency):
        """Sets the operational frequency on the given <channel ID> for the EU version. The default channels (0-2) cannot be modified in terms of frequency.

        Parameters:
        channel_id (int): The channel number (from 3 to 15)
        frequency (int): The frequency in Hz (863000000 to 870000000 or 433050000 to 434790000)

        Returns:
        str: Response from the device"""

        if channel_id < 3 or channel_id > 15:
            raise ValueError('channel_id is outside of 3 and 15.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["ch freq", channel_id, frequency])
        return res

    def mac_set_ch_dcycle(self, channel_id, duty_cycle):
        """Sets the duty cycle used on the given <channel ID> for the EU version.

        Parameters:
        channel_id (int): The channel number (0 to 15)
        duty_cycle (int): The duty cycle (0 to 65535)

        Returns:
        str: Response from the device"""

        if channel_id < 0 or channel_id > 15:
            raise ValueError('channel_id is outside of 0 and 15.')
        if duty_cycle < 0 or duty_cycle > 65535:
            raise ValueError('duty_cycle is outside of 0 and 65535.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["ch dcycle", channel_id, duty_cycle])
        return res

    def mac_set_ch_drrange(self, channel_id, min_range, max_range):
        """Sets the operating data rate range, min. to max., for the given <channelID>.

        Parameters:
        channel_id (int): The channel number (0 to 71 for the US, 0 to 15 for the EU)
        min_range (int): The minimum data rate (0 to 3 for the US, 0 to 7 for the EU)
        max_range (int): The maximum data rate (0 to 3 for the US, 0 to 7 for the EU)

        Returns:
        str: Response from the device"""

        if channel_id < 0 or channel_id > 71:
            raise ValueError('channel_id is outside of 0 and 71.')
        if min_range < 0 or min_range > 7:
            raise ValueError('min_range is outside of 0 and 7.')
        if max_range < 0 or max_range > 7:
            raise ValueError('max_range is outside of 0 and 7.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["ch drrange", channel_id, min_range, max_range])
        return res

    def mac_set_ch_status(self, channel_id, status):
        """Sets the operation of the given <channelID>.

        Parameters:
        channel_id (int): The channel number (0 to 71)
        status (CH_STATUS): The state (on or off)

        Returns:
        str: Response from the device"""

        if channel_id < 0 or channel_id > 71:
            raise ValueError('channel_id is outside of 0 and 71.')
        if status not in CH_STATUS:
            raise ValueError('status is not a member of CH_STATUS.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["ch status", channel_id, status.value])
        return res
    
    def mac_set_class(self, device_class):
        """Sets the end device LoRaWAN operating class.

        Parameters:
        device_class (DEVICE_CLASS): The LoRaWAN device class (a or c)

        Returns:
        str: Response from the device"""

        if device_class not in DEVICE_CLASS:
            raise ValueError('device_class is not a member of DEVICE_CLASS.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["class", device_class.value])
        return res

    def mac_set_devaddr(self, address):
        """Configures the module with a 4-byte unique network device address. The address must be unique to the current network.

        Parameters:
        address (str): 4-byte hexadecimal number representing the device address (00000000 to FFFFFFFF)

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["devaddr", address])
        return res

    def mac_set_deveui(self, deveui):
        """Sets the globally unique device identifier for the module.

        Parameters:
        deveui (str): 8-byte hexadecimal number representing the device EUI

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["deveui", deveui])
        return res

    def mac_set_dnctr(self, f_cnt_down):
        """Sets the value of the downlink frame counter that will be used for the next downlink reception.

        Parameters:
        f_cnt_down (int): The value of the downlink frame counter that will be used for the next downlink reception (0 to 4294967295)

        Returns:
        str: Response from the device"""

        if f_cnt_down < 0 or f_cnt_down > 4294967295:
            raise ValueError('f_cnt_down is outside of 0 and 4294967295.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["dnctr", f_cnt_down])
        return res

    def mac_set_dr(self, datarate):
        """Sets the data rate to be used for the next transmission.

        Parameters:
        datarate (int): Data rate (0 to 4 for US, 0 to 7 for EU, but within the limits of the data rate range for the defined channels)

        Returns:
        str: Response from the device"""

        if datarate < 0 or datarate > 7:
            raise ValueError('datarate is outside of 0 and 7.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["dr", datarate])
        return res

    def mac_set_linkchk(self, linkcheck):
        """Sets the time interval for the link check process to be triggered periodically.

        Parameters:
        linkcheck (int): The time interval in seconds for the link check process (0 to 65535)

        Returns:
        str: Response from the device"""

        if linkcheck < 0 or linkcheck > 65535:
            raise ValueError('linkcheck is outside of 0 and 65535.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["linkchk", linkcheck])
        return res

    def mac_set_mcast(self, state):
        """Sets the end device multicast state (mcast) to either be enabled or disabled.

        Parameters:
        state (MCAST_STATES): End device multicast state (on or off)

        Returns:
        str: Response from the device"""

        if state not in MCAST_STATES:
            raise ValueError('state is not a member of MCAST_STATES.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["mcast", state.value])
        return res

    def mac_set_mcastappskey(self, mcast_application_session_key):
        """Sets the multicast application session key for the module.

        Parameters:
        mcast_application_session_key (str): 16-byte hexadecimal number representing the application session key

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["mcastappskey", mcast_application_session_key])
        return res

    def mac_set_mcastdevaddr(self, mcast_address):
        """Configures the module with a 4-byte multicast network device address.

        Parameters:
        mcast_address (str): 4-byte hexadecimal number representing the device multicast address (00000000 to FFFFFFFF)

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["mcastdevaddr", mcast_address])
        return res
    
    def mac_set_mcastdnctr(self, f_mcast_cntdown):
        """Sets the value of the multicast downlink frame counter that will be used for the next downlink reception.

        Parameters:
        f_mcast_cntdown (int): The value of the multicast downlink frame counter (0 to 4294967295)

        Returns:
        str: Response from the device"""

        if f_mcast_cntdown < 0 or f_mcast_cntdown > 4294967295:
            raise ValueError('f_mcast_cntdown is outside of 0 and 4294967295.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["mcastdnctr", f_mcast_cntdown])
        return res

    def mac_set_mcastnwkskey(self, mcast_network_session_key):
        """Sets the multicast network session key for the module.

        Parameters:
        mcast_network_session_key (str): 16-byte hexadecimal number representing the network session key

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["mcastnwkskey", mcast_network_session_key])
        return res

    def mac_set_nwkskey(self, nwk_sess_key):
        """Sets the network session key for the module.

        Parameters:
        nwk_sess_key (str): 16-byte hexadecimal number representing the network session key

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["nwkskey", nwk_sess_key])
        return res

    def mac_set_pwridx(self, pwr_index):
        """Sets the output power to be used on the next transmissions.

        Parameters:
        pwr_index (int): Index value for the output power (5 to 10 on the US 902-928 frequency band)

        Returns:
        str: Response from the device"""

        if pwr_index < 5 or pwr_index > 10:
            raise ValueError('pwr_index is outside of 5 and 10.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["pwridx", pwr_index])
        return res

    def mac_set_retx(self, re_tx_nb):
        """Sets the number of retransmissions to be used for an uplink confirmed packet, if no downlink acknowledgment is received from the server.

        Parameters:
        re_tx_nb (int): The number of retransmissions for an uplink confirmed packet (0 to 255)

        Returns:
        str: Response from the device"""

        if re_tx_nb < 0 or re_tx_nb > 255:
            raise ValueError('re_tx_nb is outside of 0 and 255.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["retx", re_tx_nb])
        return res

    def mac_set_rx2_us(self, data_rate, frequency):
        """Sets the data rate and frequency used for the second Receive window, for US version.

        Parameters:
        data_rate (int): Data rate (8 to 13)
        frequency (FREQUENCIES): Frequency (923300000 to 927500000 Hz in 600kHz steps)

        Returns:
        str: Response from the device"""

        if data_rate < 8 or data_rate > 13:
            raise ValueError('data_rate is outside of 8 and 13.')
        if frequency not in FREQUENCIES:
            raise ValueError('frequency is not a member of FREQUENCIES.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["rx2", data_rate, frequency.value])
        return res

    def mac_set_rx2_eu(self, data_rate, frequency):
        """Sets the data rate and frequency used for the second Receive window, for EU version.

        Parameters:
        data_rate (int): Data rate (0 to 7)
        frequency (int): Frequency in Hz (863000000 to 870000000 or 433050000 to 434790000)

        Returns:
        str: Response from the device"""

        if data_rate < 0 or data_rate > 7:
            raise ValueError('data_rate is outside of 0 and 7.')
        if frequency < 433050000 or frequency > 870000000:
            raise ValueError('frequency is outside of 433050000 and 870000000.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["rx2", data_rate, frequency.value])
        return res

    def mac_set_rxdelay1(self, rx_delay):
        """Sets the delay between the transmission and the first Reception window to the <rxDelay> in milliseconds.

        Parameters:
        rx_delay (int): The delay between the transmission and the first Reception window in milliseconds (0 to 65535)

        Returns:
        str: Response from the device"""

        if rx_delay < 0 or rx_delay > 65535:
            raise ValueError('rx_delay is outside of 0 and 65535.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["rxdelay1", rx_delay])
        return res

    def mac_set_sync(self, synch_word):
        """Sets the synchronization word for the LoRaWAN communication.

        Parameters:
        synch_word (str): one byte long hexadecimal number representing the synchronization word for the LoRaWAN communication

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.MAC_SET, ["sync", synch_word])
        return res

    def mac_set_upctr(self, f_cnt_up):
        """Sets the value of the uplink frame counter that will be used for the next uplink transmission.

        Parameters:
        f_cnt_up (int): the value of the uplink frame counter that will be used for the next uplink transmission (0 to 4294967295)

        Returns:
        str: Response from the device"""

        if f_cnt_up < 0 or f_cnt_up > 4294967295:
            raise ValueError('f_cnt_up is outside of 0 and 4294967295.')
        res = self._write_data(CMD_TYPES.MAC_SET, ["upctr", f_cnt_up])
        return res

    def mac_get_adr(self):
        """Returns the state of the adaptive data rate mechanism.

        Returns:
        str: state of the adaptive data rate mechanism (on or off)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["adr"])
        return val

    def mac_get_appeui(self):
        """Returns the application identifier for the module. The application identifier is a value given to the device by the network.

        Returns:
        str: 8-byte hexadecimal number representing the application EUI"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["appeui"])
        return val

    def mac_get_ar(self):
        """Returns the current state for the automatic reply (AR) parameter.

        Returns:
        str: The state of the automatic reply (on or off)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["ar"])
        return val

    def mac_get_ch_freq(self, channel_id):
        """Returns the frequency on the requested <channelID>.

        Parameters:
        channel_id (int): Channel number (0 to 71)

        Returns:
        str: The frequency of the channel"""
        
        if channel_id < 0 or channel_id > 71:
            raise ValueError('channel_id is outside of 0 and 71.')
        val = self._read_data(CMD_TYPES.MAC_GET, ["ch freq", channel_id])
        return val

    def mac_get_ch_dcycle(self, channel_id):
        """Returns the duty cycle on the requested <channelID>.

        Parameters:
        channel_id (int): Channel number (0 to 15)

        Returns:
        str: Duty cycle of the channel (0 to 65535)"""
        
        if channel_id < 0 or channel_id > 15:
            raise ValueError('channel_id is outside of 0 and 15.')
        val = self._read_data(CMD_TYPES.MAC_GET, ["ch freq", channel_id])
        return val

    def mac_get_ch_drrange(self, channel_id):
        """Returns the allowed data rate index range on the requested <channelID>.

        Parameters:
        channel_id (int): Channel number (0 to 71 for US, 0 to 15 for EU)

        Returns:
        str: Minimum and maximum data rate of the channel"""

        if channel_id < 0 or channel_id > 71:
            raise ValueError('channel_id is outside of 0 and 71.')
        val = self._read_data(CMD_TYPES.MAC_GET, ["ch drrange", channel_id])
        return val

    def mac_get_ch_status(self, channel_id):
        """Returns if <channelID> is currently enabled for use.

        Parameters:
        channel_id (int): Channel number (0 to 71 for US, 0 to 15 for EU)

        Returns:
        str: The state of the channel (on or off)"""

        if channel_id < 0 or channel_id > 71:
            raise ValueError('channel_id is outside of 0 and 71.')
        val = self._read_data(CMD_TYPES.MAC_GET, ["ch status", channel_id])
        return val

    def mac_get_class(self):
        """Return the LoRaWAN operation class as set in the module.

        Returns:
        str: A single letter (A or C)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["class"])
        return val

    def mac_get_dcycleps(self):
        """Returns the duty cycle prescaler.

        Returns:
        str: The prescaler value (0 to 65535)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["dcycleps"])
        return val

    def mac_get_devaddr(self):
        """Returns the current end-device address of the module.

        Returns:
        str: 4-byte hexadecimal number representing the device address (00000000 to FFFFFFFF)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["devaddr"])
        return val

    def mac_get_deveui(self):
        """Returns the globally unique end-device identifier, as set in the module.

        Returns:
        str: 8-byte hexadecimal number representing the device EUI"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["deveui"])
        return val

    def mac_get_dnctr(self):
        """Returns the value of the downlink frame counter that will be used for the next downlink reception.

        Returns:
        str: The value of the downlink frame counter that will be used for the next downlink reception (0 to 4294967295)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["dnctr"])
        return val

    def mac_get_dr(self):
        """Returns the current data rate.

        Returns:
        str: Current data rate"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["dr"])
        return val

    def mac_get_gwnb(self):
        """Returns the number of gateways that successfully received the last Link Check Request frame command, as received in the last Link Check Answer.

        Returns:
        str: The number of gateways (0 to 255)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["gwnb"])
        return val

    def mac_get_mcast(self):
        """Returns the multicast state as set in the module.

        Returns:
        str: The multicast state of the module (on or off)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["mcast"])
        return val

    def mac_get_mcastdevaddr(self):
        """Returns the current multicast end-device address of the module.

        Returns:
        str: 4-byte hexadecimal number representing the device multicast address (00000000 to FFFFFFFF)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["mcastdevaddr"])
        return val

    def mac_get_mcastdnctr(self):
        """Returns the value of the downlink frame counter that will be used for the next downlink reception.

        Returns:
        str: Value of the downlink frame counter that will be used for the next multilink downlink reception (0 to 4294967295)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["mcastdnctr"])
        return val

    def mac_get_mrgn(self):
        """Returns the demodulation margin as received in the last Link Check Answer frame.

        Returns:
        str: The demodulation margin (0 to 255)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["mrgn"])
        return val

    def mac_get_pwridx(self):
        """Returns the current output power index value.

        Returns:
        str: Current output power index value"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["pwridx"])
        return val

    def mac_get_retx(self):
        """Returns the currently configured number of retransmissions which are attempted for a confirmed uplink communication when no downlink response has been received.

        Returns:
        str: The number of retransmissions (0 to 255)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["retx"])
        return val

    def mac_get_rx2(self):
        """Returns the current data rate and frequency configured to be used during the second Receive window.

        Returns:
        str: The data rate configured for the second Receive window and the frequency configured for the second Receive window"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["rx2"])
        return val

    def mac_get_rxdelay1(self):
        """Returns the interval, in milliseconds, for rxdelay1.

        Returns:
        str: The interval, in milliseconds, for rxdelay1 (0 to 65535)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["rxdelay1"])
        return val

    def mac_get_rxdelay2(self):
        """Returns the interval, in milliseconds, for rxdelay2.

        Returns:
        str: The interval, in milliseconds, for rxdelay2 (0 to 65535)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["rxdelay2"])
        return val

    def mac_get_status(self):
        """Returns the synchronization word for the LoRaWAN communication.

        Returns:
        str: one byte long hexadecimal number representing the synchronization word for the LoRaWAN communication"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["status"])
        return val

    def mac_get_sync(self):
        """Returns the synchronization word for the LoRaWAN communication.

        Returns:
        str: One byte long hexadecimal number representing the synchronization word for the LoRaWAN communication"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["sync"])
        return val

    def mac_get_upctr(self):
        """Returns the value of the uplink frame counter that will be used for the next uplink transmission.

        Returns:
        str: The value of the uplink frame counter that will be used for the next uplink transmission (0 to 4294967295)"""

        val = self._read_data(CMD_TYPES.MAC_GET, ["upctr"])
        return val

    #Transceiver Commands (Radio)

    def radio_rx(self, rx_window_size):
        """Opens the radio receiver. The mac pause command must be called before any radio transmission or reception, even if no MAC operations have been initiated before.

        Parameters:
        rx_window_size (int): The number of symbols (for LoRa modulation) or time out in milliseconds (for FSK modulation) that the receiver will be opened (0 to 65535); set <rxWindowSize> to 0 in order to enable the Continuous Reception mode. Continuous Reception mode will be exited once a valid packet is received.

        Returns:
        str: First response from the device; this command may reply with two responses"""

        if rx_window_size < 0 or rx_window_size > 65536:
            raise ValueError('rx_window_size is outside of 0 and 65536.')
        res = self._write_data(CMD_TYPES.RADIO_RX, [rx_window_size])
        return res

    def radio_tx(self, data):
        """Transmits the data passed.

        Parameters:
        data (str): Hexadecimal value representing the data to be transmitted (0 to 255 bytes for LoRa modulation and from 0 to 64 bytes for FSK modulation)

        Returns:
        str: First response from the device; this command may reply with two responses"""

        res = self._write_data(CMD_TYPES.RADIO_TX, [data])
        return res

    def radio_cw(self, state):
        """Enables or disables the CW mode on the module.

        Parameters:
        state (CW_MODES): The state of the Continuous Wave (CW) mode (on or off)

        Returns:
        str: Response from the device"""

        if state not in CW_MODES:
            raise ValueError('state is not a member of CW_MODES.')
        res = self._write_data(CMD_TYPES.RADIO, ["cw", state.value])
        return res

    def radio_rxstop(self):
        """Causes the radio to exit Continuous Receive mode.

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.RADIO, ["rxstop"])
        return res

    def radio_set_afcbw(self, auto_freq_band):
        """Modifies the automatic frequency correction bandwidth for receiving/transmitting.

        Parameters:
        auto_freq_band (FREQ_BANDS): The automatic frequency correction, in kHz

        Returns:
        str: Response from the device"""

        if auto_freq_band not in FREQ_BANDS:
            raise ValueError('auto_freq_band is not a member of FREQ_BANDS.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["afcbw", auto_freq_band.value])
        return res

    def radio_set_bitrate(self, fsk_bitrate):
        """Sets the FSK bit rate value.

        Parameters:
        fsk_bitrate (int): The FSK bit rate value (1 to 300000)

        Returns:
        str: Response from the device"""

        if fsk_bitrate < 1 or fsk_bitrate > 300000:
            raise ValueError('fsk_bitrate is outside of 1 and 300000.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["bitrate", fsk_bitrate])
        return res

    def radio_set_bt(self, gf_bt):
        """Modifies the data shaping applied to FSK transmissions.

        Parameters:
        gf_bt (GFBTS): The Gaussian baseband data shaping, enabling GFSK modulation.

        Returns:
        str: Response from the device"""

        if gf_bt not in GFBTS:
            raise ValueError('gf_bt is not a member of GFBTS.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["bt", gf_bt.value])
        return res

    def radio_set_bw(self, bandwidth):
        """Sets the operating radio bandwidth for LoRa operation.

        Parameters:
        bandwidth (RADIO_BW): The operating radio bandwidth, in kHz

        Returns:
        str: Response from the device"""

        if bandwidth not in RADIO_BW:
            raise ValueError('bandwidth is not a member of RADIO_BW.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["bw", bandwidth.value])
        return res

    def radio_set_cr(self, coding_rate):
        """Modifies the coding rate currently being used by the radio.

        Parameters:
        coding_rate (CODING_RATES): The coding rate

        Returns:
        str: Response from the device"""

        if coding_rate not in CODING_RATES:
            raise ValueError('coding_rate is not a member of CODING_RATES.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["cr", coding_rate.value])
        return res

    def radio_set_crc(self, crc_header):
        """Enables or disables the CRC header for communications.

        Parameters:
        crc_header (CRC_HEADER_STATES): The state of the CRC header (on or off)

        Returns:
        str: Response from the device"""

        if crc_header not in CRC_HEADER_STATES:
            raise ValueError('crc_header is not a member of CRC_HEADER_STATES.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["crc", crc_header.value])
        return res

    def radio_set_fdev(self, freq_dev):
        """Sets the frequency deviation during operation.

        Parameters:
        freq_dev (int): Frequency deviation (0 to 200000)

        Returns:
        str: Response from the device"""

        if freq_dev < 0 or freq_dev > 200000:
            raise ValueError('freq_dev is outside of 0 and 200000.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["fdev", freq_dev])
        return res

    def radio_set_freq(self, frequency):
        """Changes the communication frequency of the radio transceiver.

        Parameters:
        frequency (int): Frequency in Hz (902000000 to 928000000 for US, 433050000 to 434790000 or 863000000 to 870000000 for EU)

        Returns:
        str: Response from the device"""

        if frequency < 433050000 or frequency > 928000000:
            raise ValueError('frequency is outside of 433050000 and 928000000.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["freq", frequency])
        return res

    def radio_set_iqi(self, iq_invert):
        """Enables or disables the Invert IQ for communications.

        Parameters:
        iq_invert (IQI_STATES): The state of the invert IQ (on or off)

        Returns:
        str: Response from the device"""

        if iq_invert not in IQI_STATES:
            raise ValueError('iq_invert is not a member of IQI_STATES.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["iqi", iq_invert.value])
        return res

    def radio_set_mod(self, mode):
        """The modulation method being used by the module.

        Parameters:
        mode (RADIO_MODES): The modulation method (LoRa or FSK)

        Returns:
        str: Response from the device"""

        if mode not in RADIO_MODES:
            raise ValueError('mode is not a member of RADIO_MODES.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["mod", mode.value])
        return res

    def radio_set_prlen(self, preamble):
        """Sets the preamble length for transmit/receive.

        Parameters:
        preamble (int): The preamble length (0 to 65535)

        Returns:
        str: Response from the device"""

        if preamble < 0 or preamble > 65535:
            raise ValueError('preamble is outside of 0 and 65535.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["prlen", preamble])
        return res

    def radio_set_pwr(self, pwr_out):
        """Changes the transceiver output power.

        Parameters:
        pwr_out (int): Transceiver output power (2 to 20 for US, -3 to 15 for EU)

        Returns:
        str: Response from the device"""

        if pwr_out < -3 or pwr_out > 20:
            raise ValueError('pwr_out is outside of -3 and 20.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["pwr", pwr_out])
        return res

    def radio_set_rxbw(self, rx_bandwidth):
        """Sets the signal bandwidth when receiving.

        Parameters:
        rx_bandwidth (FREQ_BANDS): The signal bandwidth, in kHz

        Returns:
        str: Response from the device"""

        if rx_bandwidth not in FREQ_BANDS:
            raise ValueError('rx_bandwidth is not a member of FREQ_BANDS.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["rxbw", rx_bandwidth.value])
        return res

    def radio_set_sf(self, spreading_factor):
        """Sets the spreading factor used during transmission.

        Parameters:
        spreading_factor (SPREADING_FACTORS): Spreading factor

        Returns:
        str: Response from the device"""

        if spreading_factor not in SPREADING_FACTORS:
            raise ValueError('spreading_factor is not a member of SPREADING_FACTORS.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["sf", spreading_factor.value])
        return res

    def radio_set_sync(self, sync_word):
        """Configures the sync word used during communication.

        Parameters:
        sync_word (str): The sync word used during communication (For LoRa modulation one byte is used, for FSK up to eight bytes can be entered)

        Returns:
        str: Response from the device"""

        res = self._write_data(CMD_TYPES.RADIO_SET, ["sync", sync_word])
        return res

    def radio_set_wdt(self, watchdog):
        """Updates the time-out length, in milliseconds, applied to the radio Watchdog Timer.

        Parameters:
        watchdog (int): The time-out length for the Watchdog Timer (0 to 4294967295; set to 0 to disable this functionality)

        Returns:
        str: Response from the device"""

        if watchdog < 0 or watchdog > 4294967295:
            raise ValueError('watchdog is outside of 0 and 4294967295.')
        res = self._write_data(CMD_TYPES.RADIO_SET, ["wdt", watchdog])
        return res

    def radio_get_afcbw(self):
        """Reads back the status of the Automatic Frequency Correction Bandwidth.

        Returns:
        str: Automatic frequency correction band, in kHz"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["afcbw"])
        return val

    def radio_get_bitrate(self):
        """Reads back the configured bit rate for FSK communications.

        Returns:
        str: The configured bit rate (1 to 300000)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["bitrate"])
        return val

    def radio_get_bt(self):
        """Reads back the current configuration for data shaping applied to FSK transmissions.

        Returns:
        str: The configuration for data shaping"""
        
        val = self._read_data(CMD_TYPES.RADIO_GET, ["bt"])
        return val

    def radio_get_bw(self):
        """Reads back the current operating radio bandwidth used by the transceiver.

        Returns:
        str: The current operating radio bandwidth, in kHz"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["bw"])
        return val

    def radio_get_cr(self):
        """Reads back the current value settings used for the coding rate during communication.

        Returns:
        str: The current value settings used for the coding rate."""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["cr"])
        return val

    def radio_get_crc(self):
        """Reads back the status of the CRC header, to determine if it is to be included during operation.

        Returns:
        str: Status of the CRC header (on or off)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["crc"])
        return val

    def radio_get_fdev(self):
        """Reads frequency deviation setting on the transceiver.

        Returns:
        str: Frequency deviation setting (0 to 200000)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["fdev"])
        return val

    def radio_get_freq(self):
        """Reads back the current operation frequency of the module.

        Returns:
        str: Frequency in Hz"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["freq"])
        return val

    def radio_get_iqi(self):
        """Reads back the status of the Invert IQ functionality.

        Returns:
        str: Status of the Invert IQ functionality (on or off)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["iqi"])
        return val

    def radio_get_mod(self):
        """Reads back the current mode of operation of the module.

        Returns:
        str: Current mode of operation of the module (lora or fsk)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["mod"])
        return val

    def radio_get_prlen(self):
        """Reads the current preamble length used for communication.

        Returns:
        str: The preamble length (0 to 65535)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["prlen"])
        return val

    def radio_get_pwr(self):
        """Reads back the current power level settings used in operation.

        Returns:
        str: Current power level"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["pwr"])
        return val

    def radio_get_rssi(self):
        """Reads back the radio Received Signal Strength Indication (rssi) value for the last received frame.

        Returns:
        str: The rssi for the last received frame"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["rssi"])
        return val

    def radio_get_rxbw(self):
        """Reads back the signal bandwidth used for receiving.

        Returns:
        str: The signal bandwidth, in kHz"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["rxbw"])
        return val

    def radio_get_sf(self):
        """Reads back the current spreading factor being used by the transceiver.

        Returns:
        str: The current spreading factor"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["sf"])
        return val

    def radio_get_snr(self):
        """Reads back the Signal Noise Ratio (SNR) for the last received packet.

        Returns:
        str: The signal to noise ratio (SNR) (-128 to 127)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["snr"])
        return val

    def radio_get_sync(self):
        """Reads back the configured synchronization word used for radio communication.

        Returns:
        str: The synchronization word used for radio communication"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["sync"])
        return val

    def radio_get_wdt(self):
        """Reads back the length used for the watchdog time-out in milliseconds.

        Returns:
        str: The length used for the watchdog time-out (0 to 4294967295)"""

        val = self._read_data(CMD_TYPES.RADIO_GET, ["wdt"])
        return val

    #Module Configuration

    def _set_initial_settings(self, auto_config, freq):
        """Initiates the RN2XX3A LoRa module.

        Parameters:
        auto_config (CONFIG_MODES): LoRa Module operating mode. NONE is for manual configuration. LORA_TX and LORA_RX are for automatic configuration. (MODES.CONFIG_MODES.NONE is default)
        freq (int): LoRa radio frequency for auto configuration. (Default is 915000000 for US)."""

        self.auto = auto_config
        self.sys_reset()

        self.config_led(LEDS.CON)
        self.config_led(LEDS.ACT)
        self.config_led(LEDS.ERR)

        self.set_led(LEDS.CON, LED_STATES.OFF)
        self.set_led(LEDS.ACT, LED_STATES.OFF)
        self.set_led(LEDS.ERR, LED_STATES.OFF)

        sleep(0.5)

        if auto_config == CONFIG_MODES.LORA_RX:
            self.radio_set_mod(RADIO_MODES.LORA)            #radio set mod lora
            self.radio_set_freq(freq)                       #radio set freq <freq>
            self.radio_set_sf(SPREADING_FACTORS.SF7)        #radio set sf sf7
            self.radio_set_bw(RADIO_BW.BW_125)              #radio set bw 125
            self.radio_set_cr(CODING_RATES.R_4_5)           #radio set cr 4/5
            self.radio_set_crc(CRC_HEADER_STATES.ON)        #radio set crc on
            self.radio_set_sync(12)                         #radio set sync 12
            self.radio_set_wdt(0)                           #radio set wdt 0
            self.radio_set_pwr(14)                          #radio set pwr 14
            sleep(0.1)
            self.mac_pause()                                #mac pause
            sleep(0.1)
            self.radio_rx(0)                                #radio rx 0
            self.set_led(LEDS.CON, LED_STATES.ON)
        elif auto_config == CONFIG_MODES.LORA_TX:
            self.radio_set_mod(RADIO_MODES.LORA)            #radio set mod lora
            self.radio_set_freq(freq)                       #radio set freq <freq>
            self.radio_set_sf(SPREADING_FACTORS.SF7)        #radio set sf sf7
            self.radio_set_bw(RADIO_BW.BW_125)              #radio set bw 125
            self.radio_set_cr(CODING_RATES.R_4_5)           #radio set cr 4/5
            self.radio_set_crc(CRC_HEADER_STATES.ON)        #radio set crc on
            self.radio_set_sync(12)                         #radio set sync 12
            self.radio_set_wdt(0)                           #radio set wdt 0
            self.radio_set_pwr(14)                          #radio set pwr 14
            sleep(0.1)
            self.mac_pause()                                #mac pause
        else:
            pass
        return

    #LED Control
    def config_led(self, led):
        """Sets the LED status.

        Parameters:
        led (LEDS): LEDs; Con, Act or Err

        Returns:
        str: Response from the device"""

        if led not in LEDS:
            raise ValueError('led is not a member of LEDS.')
        res = self._write_data(CMD_TYPES.SYS_SET, ["pinmode", led.value, "digout"])
        return res

    def set_led(self, led, state):
        """Sets the LED status.

        Parameters:
        led (LEDS): LEDs; Con, Act or Err
        state (LED_STATES): LED state, on or off

        Returns:
        str: Response from the device"""

        if led not in LEDS:
            raise ValueError('led is not a member of LEDS.')
        if state not in LED_STATES:
            raise ValueError('state is not a member of LED_STATES.')
        res = self._write_data(CMD_TYPES.SYS_SET, ["pindig", led.value, state.value])
        return res

    #Disposal

    def __del__(self):
        """Releases the resources. Stops the radio if auto mode is selected."""

        try:
            if self.is_initialized:
                if(self.auto != CONFIG_MODES.NONE):
                    self.radio_rxstop()
                self.set_led(LEDS.CON, LED_STATES.OFF)
                self.set_led(LEDS.ACT, LED_STATES.OFF)
                self.set_led(LEDS.ERR, LED_STATES.OFF)
                self.sp.close()
                del self.is_initialized
        except:
            pass
