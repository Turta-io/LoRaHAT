#!/usr/bin/env python3

#This sample demonstrates receiving packets over the LoRaWAN protocol. (For EU version.)
#Install LoRa HAT library with "pip3 install turta-lorahat"

#Raspberry Pi Configuration
# - You should enable SPI and I2C from the Raspberry Pi's configuration.
# To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.
# - You should swap the serial ports of the Raspberry Pi.
# Set "/dev/ttyAMA0" to 'serial0'. Also, disable the console on 'serial0'.
# For a how-to, visit our documentation at https://docs.turta.io/how-tos/raspberry-pi/raspbian/swapping-the-serial-ports

from time import sleep
from turta_lorahat import Turta_LoRa

#Initialize
lora = Turta_LoRa.RN2XX3(region = Turta_LoRa.REGIONS.EU_RN2483, auto_config = Turta_LoRa.CONFIG_MODES.LORA_RX)
print("Radio is set to receive.")

try:
    while True:
        #Check for serial port buffer
        buffer = lora.check_data()

        #If data is received, print it
        if buffer is not None:
            print(buffer)

#Exit on CTRL+C
except KeyboardInterrupt:
    print('Bye.')
