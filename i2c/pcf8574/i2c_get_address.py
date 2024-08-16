import machine

# Initialize I2C bus on pins 16 (SDA) and 17 (SCL) with a frequency of 400kHz
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)

# print the I2C address
print('I2C address:')
print(hex(i2c.scan()[0]), ' (hex)')
