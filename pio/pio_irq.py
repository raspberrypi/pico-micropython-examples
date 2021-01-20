import time
import rp2

@rp2.asm_pio()
def irq_test():
    wrap_target()
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    irq(0)
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    irq(1)
    wrap()


rp2.PIO(0).irq(lambda pio: print(pio.irq().flags()))

sm = rp2.StateMachine(0, irq_test, freq=1000)
sm.active(1)
time.sleep(1)
sm.active(0)