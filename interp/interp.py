# demonstrate driving low level rp2040 functions from Python by
# direct register access - see datasheet at 
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
# for details

from machine import mem32

# base address of SIO
SIO_BASE = 0xD0000000

# INTERP0 registers
INTERP0_ACCUM0 = 0xD0000000 + 0x80
INTERP0_BASE0 = 0xD0000000 + 0x88
INTERP0_POP_LANE0 = 0xD0000000 + 0x94
INTERP0_CTRL_LANE0 = 0xD0000000 + 0xAC

# initialise lane 0 on interp: set that we are using all 32 bits
mem32[INTERP0_CTRL_LANE0] = 0x1F << 10

# set up 9 x table example - write to accum[0] and base[0] registers
mem32[INTERP0_ACCUM0] = 0
mem32[INTERP0_BASE0] = 9

# read pop register 10 times
for j in range(10):
    print(mem32[INTERP0_POP_LANE0])