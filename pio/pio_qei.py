# Example using PIO to read a quadrature encoder
#
# Demonstrates:
#   - PIO reading 2 pin
# How to force a program to start at 0 by putting nop()
# instructions at the end of the programm


import time
import rp2
from machine import Pin
from rp2 import PIO


@rp2.asm_pio(in_shiftdir=PIO.SHIFT_LEFT)
def QEI_prog():
    #
    # Copyright (c) 2021 pmarques-dev @ github
    #
    # SPDX-License-Identifier: BSD-3-Clause
    #

    #.program quadrature_encoder

    # this code must be loaded into address 0, but at 29 instructions, it probably
    # wouldn't be able to share space with other programs anyway
    #.origin 0


    # the code works by running a loop that continuously shifts the 2 phase pins into
    # ISR and looks at the lower 4 bits to do a computed jump to an instruction that
    # does the proper "do nothing" | "increment" | "decrement" action for that pin
    # state change (or no change)

    # ISR holds the last state of the 2 pins during most of the code. The Y register
    # keeps the current encoder count and is incremented / decremented according to
    # the steps sampled

    # writing any non zero value to the TX FIFO makes the state machine push the
    # current count to RX FIFO between 6 to 18 clocks afterwards. The worst case
    # sampling loop takes 14 cycles, so this program is able to read step rates up
    # to sysclk / 14  (e.g., sysclk 125MHz, max step rate = 8.9 Msteps/sec)


    # 00 state
    
    jmp("update")	# read 00
    jmp("decrement")	# read 01
    jmp("increment")	# read 10
    jmp("update")	# read 11

    # 01 state
    jmp("increment")	# read 00
    jmp("update")	# read 01
    jmp("update")	# read 10
    jmp("decrement")	# read 11

    # 10 state
    jmp("decrement")	# read 00
    jmp("update")	# read 01
    jmp("update")	# read 10
    jmp("increment")	# read 11

    # to reduce code size, the last 2 states are implemented in place and become the
    # target for the other jumps

    # 11 state
    jmp("update")	# read 00
    jmp("increment")	# read 01
    label("decrement")
    # note: the target of this instruction must be the next address, so that
    # the effect of the instruction does not depend on the value of Y. The
    # same is true for the "JMP X--" below. Basically "JMP Y--, <next addr>"
    # is just a pure "decrement Y" instruction, with no other side effects
    jmp(y_dec, "update")	# read 10

    # this is where the main loop starts
    wrap_target()
    label("update")
    # we start by checking the TX FIFO to see if the main code is asking for
    # the current count after the PULL noblock, OSR will have either 0 if
    # there was nothing or the value that was there
    set(x, 0)
    pull(noblock)

    # since there are not many free registers, and PULL is done into OSR, we
    # have to do some juggling to avoid losing the state information and
    # still place the values where we need them
    mov(x, osr)
    mov(osr, isr)

    # the main code did not ask for the count, so just go to "sample_pins"
    jmp(not_x, "sample_pins")

    # if it did ask for the count, then we push it
    mov(isr, y) # we trash ISR, but we already have a copy in OSR
    push()

    label("sample_pins")
    # we shift into ISR the last state of the 2 input pins (now in OSR) and
    # the new state of the 2 pins, thus producing the 4 bit target for the
    # computed jump into the correct action for this state
    mov(isr, null)
    in_(osr, 2)
    in_(pins, 2)
    mov(pc, isr)

    # the PIO does not have a increment instruction, so to do that we do a
    # negate, decrement, negate sequence
    label("increment")
    mov(x, invert(y))
    jmp(x_dec, "increment_cont")
    label("increment_cont")
    mov(y, invert(x))
    wrap() # the .wrap here avoids one jump instruction and saves a cycle too
    # Without these 3 instructions, the code wasn't working.
    # did python put the start of the program somewhere else than at 0 ?
    # With these 3 nop(), there is no choice, it should use the entire 32 bytes of memory
    nop()
    nop()
    nop()

class PIOQEI:
    def __init__(self, sm_id, pin):
        Pin(pin, Pin.IN)
        Pin(pin+1, Pin.IN)

        self.sm = rp2.StateMachine(sm_id, prog=QEI_prog, in_base=pin, in_shiftdir=PIO.SHIFT_LEFT)
        self.sm.active(1)
        

    def get(self):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        self.sm.put(1)
        return self.sm.get()
        

# Create the StateMachine with the QEI program, reading on Pin(2) & Pin(3).
qei1 = PIOQEI(1, 2)
qei2 = PIOQEI(0, 11)

while True:
    print("count1:" + str(qei1.get()))
    print("count2:" + str(qei2.get()))
    time.sleep_ms(100)
    


