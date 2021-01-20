from machine import Pin, I2C

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) 
i2c.scan()
i2c.writeto(76, b'123')
i2c.readfrom(76, 4)

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
i2c.scan()
i2c.writeto_mem(76, 6, b'456')
i2c.readfrom_mem(76, 6, 4)
