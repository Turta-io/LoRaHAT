#!/usr/bin/env python3

#This sample demonstrates transmitting board temperature over the LoRaWAN protocol. (For US version.)
#Install LoRa HAT library with "pip3 install turta-lorahat"

#Raspberry Pi Configuration
# - You should enable SPI and I2C from the Raspberry Pi's configuration.
# To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.
# - You should swap the serial ports of the Raspberry Pi.
# Set "/dev/ttyAMA0" to 'serial0'. Also, disable the console on 'serial0'.
# For a how-to, visit our documentation at https://docs.turta.io/how-tos/raspberry-pi/raspbian/swapping-the-serial-ports

from time import sleep
from turta_lorahat import Turta_LoRa
from turta_lorahat import Turta_Analog

#Initialize
analog = Turta_Analog.ADC()
lora = Turta_LoRa.RN2XX3(region = Turta_LoRa.REGIONS.US_RN2903, auto_config = Turta_LoRa.CONFIG_MODES.LORA_TX)
print("Radio is set to transmit.")

cnt = 0

try:
    while True:
        #Read LoRa HAT's borad temperature (This is not the ambient temperature)
        board_temp_c = analog.read_temperature()
        print("Board temp:", str(round(board_temp_c, 1)) + "C")

        #Send the payload over the LoRaWAN Protocol
        print("Sending packet...")
        res = lora.send("LoRa board temp: " + str(round(board_temp_c, 1)) + "C")
        print("Result:", res)

        #Wait
        sleep(5)

#Exit on CTRL+C
except KeyboardInterrupt:
    print('Bye.')
