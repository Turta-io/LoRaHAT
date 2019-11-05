#!/usr/bin/env python3

#This sample demonstrates measuring single-ended analog inputs from analog ports.
#Install LoRa HAT library with "pip3 install turta-lorahat"

#Raspberry Pi Configuration
# - You should enable SPI and I2C from the Raspberry Pi's configuration.
# To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.

from time import sleep
from turta_lorahat import Turta_Analog

#Initialize
analog = Turta_Analog.ADC()

try:
    while True:
        #Read analog channel 1 on left analog port
        a1 = analog.read(Turta_Analog.CH.SINGLE_1)

        #Read analog channel 2 on left analog port
        a2 = analog.read(Turta_Analog.CH.SINGLE_2)

        #Read analog channel 3 on right analog port
        a3 = analog.read(Turta_Analog.CH.SINGLE_3)

        #Read analog channel 4 on right analog port
        a4 = analog.read(Turta_Analog.CH.SINGLE_4)

        #Read board temperature
        board_temp_c = analog.read_temperature()
        board_temp_f = analog.read_temperature(True)

        #Print the readings
        print("Analog Input 1..: " + str(a1))
        print("Analog Input 2..: " + str(a2))
        print("Analog Input 3..: " + str(a3))
        print("Analog Input 4..: " + str(a4))
        print("Board Temp......: " + str(round(board_temp_c, 1)) + "C" + \
              " / " + str(round(board_temp_f, 1)) + "F")

        #Wait
        print("-----")
        sleep(0.5)

#Exit on CTRL+C
except KeyboardInterrupt:
    print('Bye.')
