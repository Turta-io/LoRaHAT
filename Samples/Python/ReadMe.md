# Python Samples
This directory includes Python samples for Turta LoRa HAT.

## Index
* __accel.py:__ Demonstrates reading the 3D acceleration data.
* __analog_differential.py:__ Demonstrates measuring differential analog inputs from analog ports.
* __analog_single_ended.py:__ Demonstrates measuring single-ended analog inputs from analog ports.
* __digital_port_in_out.py:__ Demonstrates digital port read and write.
* __lora_eu_rx.py:__ Demonstrates receiving packets over the LoRaWAN protocol. (For EU version.)
* __lora_eu_tx.py:__ Demonstrates transmitting board temperature over the LoRaWAN protocol. (For EU version.)
* __lora_us_rx.py:__ Demonstrates receiving packets over the LoRaWAN protocol. (For US version.)
* __lora_us_tx.py:__ Demonstrates transmitting board temperature over the LoRaWAN protocol. (For US version.)
* __tilt_detect.py:__ Demonstrates detecting tilt without using the I2C bus.

## Raspberry Pi Configuration
* You should enable SPI and I2C from the Raspberry Pi's configuration. To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.
* You should swap the serial ports of the Raspberry Pi. Set "/dev/ttyAMA0" to 'serial0'. Also, disable the console on 'serial0'. For a how-to, visit our documentation at [docs.turta.io](https://docs.turta.io/how-tos/raspberry-pi/raspbian/swapping-the-serial-ports).

## Running the Python Samples
* Copy the sample code to your Raspberry Pi.
* Install the libraries with 'pip3 install turta-lorahat' command.
* Run the sample with 'python3 <Sample_Name>.py' command.
* Exit from the sample using CTRL+C or ^C key.

## Documentation
Visit [docs.turta.io](https://docs.turta.io) for documentation.
