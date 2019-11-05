#!/usr/bin/env python3

#This sample reading the 3D acceleration data.
#Install LoRa HAT library with "pip3 install turta-lorahat"

#Raspberry Pi Configuration
# - You should enable SPI and I2C from the Raspberry Pi's configuration.
# To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.

from time import sleep
from turta_lorahat import Turta_Accel

#Initialize
accel = Turta_Accel.AccelTiltSensor()

try:
    while True:
        #Read X, Y and Z-Axis G values in one shot
        accel_xyz = accel.read_accel_xyz()

        #Read the readings
        print("X-Axis..........: " + str(round(accel_xyz[0], 2)) + "G")
        print("Y-Axis..........: " + str(round(accel_xyz[1], 2)) + "G")
        print("Z-Axis..........: " + str(round(accel_xyz[2], 2)) + "G")

        #Wait
        print("-----")
        sleep(0.2)

#Exit on CTRL+C
except KeyboardInterrupt:
    print('Bye.')
