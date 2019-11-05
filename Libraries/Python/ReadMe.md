# Python Libraries
This directory includes Python libraries for Turta LoRa HAT.

## Index
* __Turta_Accel.py:__ Python Library for NXP MMA8491Q 3-Axis Accelerometer & Tilt Sensor.
* __Turta_Analog.py:__ Python Library for TI ADS1018 ADC.
* __Turta_Digital.py:__ Python Library for Digital IO Ports.
* __Turta_LoRa.py:__ Python Library for Microchip RN2903A/RN2483A LoRa Module.

## Installation of Python Libraries
* Use 'pip3 install turta-lorahat' to download and install libraries automatically.
* Use 'pip3 install --upgrade --user turta-lorahat' to update your libraries.
* Use 'pip3 uninstall turta-lorahat' to uninstall the libraries.
* If you wish to install libraries manually, copy the ingredients of Python folder to the project folder.
* To use the 'ATECC608A Cryptographic Co-Processor', please refer to our documentation at [docs.turta.io](https://docs.turta.io).

## Dependencies for Python Libraries
The package installer installs other libraries required for LoRa HAT's operation.
* We're using "pySerial" for UART communication. To install it manually, type 'sudo pip3 install pyserial' to the terminal.
* We're using 'SMBus' for I2C communication. To install it manually, type 'sudo pip3 install smbus' to the terminal.
* We're using 'spidev' for SPI communication. To install it manually, type 'sudo pip3 install spidev' to the terminal.
* We're using 'RPi.GPIO' for GPIO access. To install it manually, type 'sudo pip3 install RPi.GPIO' to the terminal.
* We're using Python 3 for the libraries and samples.

## Raspberry Pi Configuration
* You should enable SPI and I2C from the Raspberry Pi's configuration. To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.
* You should swap the serial ports of the Raspberry Pi. Set "/dev/ttyAMA0" to 'serial0'. Also, disable the console on 'serial0'. For a how-to, visit our documentation at [docs.turta.io](https://docs.turta.io/how-tos/raspberry-pi/raspbian/swapping-the-serial-ports).

## Documentation
Visit [docs.turta.io](https://docs.turta.io) for documentation.
