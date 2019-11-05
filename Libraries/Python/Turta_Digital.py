# Turta LoRa HAT Helper for Raspbian.
# Distributed under the terms of the MIT license.

# Python Library for Digital IO Ports.
# Version 1.0.0
# Released: November 5th, 2019

# Visit https://docs.turta.io for documentation.

import RPi.GPIO as GPIO

class DigitalPort(object):
    """Digital IO Ports."""

    #Variables
    is_initialized = False

    #Port Pins
    d1, d2, d3, d4 = 21, 22, 23, 24

    def __init__(self, d1In = True, d2In = True, d3In = True, d4In = True):
        """Initiates the GPIO pins.

        Parameters:
        d1In (bool): Pin 1 direction (True for input, False for output, True is default)
        d2In (bool): Pin 2 direction (True for input, False for output, True is default)
        d3In (bool): Pin 3 direction (True for input, False for output, True is default)
        d4In (bool): Pin 4 direction (True for input, False for output, True is default)"""

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        if (d1In):
            GPIO.setup(self.d1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        else:
            GPIO.setup(self.d1, GPIO.OUT)
            GPIO.output(self.d1, GPIO.LOW)

        if (d2In):
            GPIO.setup(self.d2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        else:
            GPIO.setup(self.d2, GPIO.OUT)
            GPIO.output(self.d2, GPIO.LOW)

        if (d3In):
            GPIO.setup(self.d3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        else:
            GPIO.setup(self.d3, GPIO.OUT)
            GPIO.output(self.d3, GPIO.LOW)

        if (d4In):
            GPIO.setup(self.d4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        else:
            GPIO.setup(self.d4, GPIO.OUT)
            GPIO.output(self.d4, GPIO.LOW)

        self.is_initialized = True
        return

    #GPIO Read and Write Methods

    def read(self, ch):
        """Reads the digital input.

        Parameters:
        ch (byte): IO Channel (1 to 4)

        Returns:
        bool: Pin input state (True for high, False for low)"""

        if (ch == 1):
            return GPIO.input(self.d1)
        elif (ch == 2):
            return GPIO.input(self.d2)
        elif (ch == 3):
            return GPIO.input(self.d3)
        elif (ch == 4):
            return GPIO.input(self.d4)
        else:
            return 0

    def write(self, ch, st):
        """Sets the digital output.

        Parameters:
        ch (byte): IO Channel (1 to 4)
        st (bool): Pin output state (True for high, False for low)"""

        if (ch == 1):
            GPIO.output(self.d1, GPIO.HIGH if st else GPIO.LOW)
        elif (ch == 2):
            GPIO.output(self.d2, GPIO.HIGH if st else GPIO.LOW)
        elif (ch == 3):
            GPIO.output(self.d3, GPIO.HIGH if st else GPIO.LOW)
        elif (ch == 4):
            GPIO.output(self.d4, GPIO.HIGH if st else GPIO.LOW)
        return

    def toggle(self, ch):
        """Inverts the digital output.

        Parameters:
        ch (byte): IO Channel (1 to 4)"""

        self.write(ch, not self.read(ch))
        return

    #Disposal

    def __del__(self):
        """Releases the resources."""

        try:
            if self.is_initialized:
                GPIO.cleanup()
                del self.is_initialized
        except:
            pass
