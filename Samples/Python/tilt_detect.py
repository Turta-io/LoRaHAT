#!/usr/bin/env python3

#This sample demonstrates detecting tilt without using the I2C bus.
#Install LoRa HAT library with "pip3 install turta-lorahat"

from time import sleep
from turta_lorahat import Turta_Accel

#Initialize
accel = Turta_Accel.AccelTiltSensor()

try:
    while True:
        #Read tilt states in one shot
        tilt_xyz = accel.read_tilt_xyz()

        #Print the readings
        print("X-Tilt..........: " + ("Tilt detected." if tilt_xyz[0] else "No tilt."))
        print("Y-Tilt..........: " + ("Tilt detected." if tilt_xyz[1] else "No tilt."))
        print("Z-Tilt..........: " + ("Tilt detected." if tilt_xyz[2] else "No tilt."))

        #Wait
        print("-----")
        sleep(0.5)

#Exit on CTRL+C
except KeyboardInterrupt:
    print('Bye.')
