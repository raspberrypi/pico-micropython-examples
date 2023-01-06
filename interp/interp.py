from machine import mem32

# initialise lane 0 on interp: set that we are using all 32 bits
mem32[0xD0000000 | 0xAC] = 0x1F << 10

# set up 9 x table example - write to accum[0] and base[0] registers
mem32[0xD0000000 | 0x80] = 0
mem32[0xD0000000 | 0x88] = 9

# read pop register 10 times
for j in range(10):
    print(mem32[0xD0000000 | 0x94])