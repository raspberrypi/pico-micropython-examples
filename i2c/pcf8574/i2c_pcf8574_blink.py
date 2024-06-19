# Add more IO Pins via a PCF8574 Remote 8-Bit I/O Expander

from machine import Pin, I2C
import utime

# Initialize I2C bus on pins 16 (SDA) and 17 (SCL) with a frequency of 400kHz
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)

# Address of the PCF8574 I/O expander on the I2C bus
address = 0x20

def toggle_pins():
    try:
        for i in range(8):
            # Create a bitmask to set each pin high one at a time
            pin_state = 1 << i
            
            # Write the bitmask to the PCF8574
            i2c.writeto(address, bytearray([pin_state]))
            
            # Sleep for 200ms to keep the pin high
            utime.sleep(0.2)
            
            # Reset all pins to low
            i2c.writeto(address, bytearray([0x00]))
    except OSError as e:
        # Print an error message if there is an issue accessing the I2C device
        print("Error accessing the I2C device:", e)

# Continuously toggle the pins
while True:
    toggle_pins()