from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio
from time import sleep, ticks_ms, ticks_diff

pwm_out = PWM(Pin(16))

pwm_out.freq(100)
pwm_out.duty_u16((2**16-1)//2)

@asm_pio()
def pwmin():
    pull(block)           # wait for activation
    
    set(x, 0)               # Set x = 0
    mov(x, x | (0b01 << 3)) # invert x = Max-Value for 32 bits. (0b01 << 3) sets the invert bit.
    
    wait(1, pin, 0)         # wait for a full PWM cycle to start measurement
    wait(0, pin, 0)         # wait for pin to be low
    
    label("count_low")          
    jmp(pin, "out_low")         # jump to output if pin is high
    jmp(x_dec, "count_low")     # jump back to count loop, decrement X
    label("out_low")
    
    mov(isr, x)             # move x into ISR
    push(noblock)             # push into fifo
    
    label("count_high")
    jmp(x_dec, "next")      # count down X, jump to next instruction
    label("next")
    jmp(pin, "count_high")  # as long as the pin is high, jump back up to continue countdown
    
    mov(isr, x)             # move x into ISR
    push(noblock)           # push into fifo
    irq(0)

base_frq = 100_000_000
sm = rp2.StateMachine(0, pwmin, freq=base_frq, jmp_pin=Pin(16), in_base=Pin(16))
sm.active(1)

'''
W A R N I N G

This example code will hang, if no PWM signal is present,
e.g. when the PWM is at 0% or 100% duty cycle.

'''
def readPwm(sm):
    # Send data to start measurement
    sm.put(0)
 
    low = sm.get()
    total = sm.get()
    
    # Convert to duration
    low = 2**32 - 1 - low
    total = 2**32 - 1 - total
    
    # Total is in ticks, based on base_frq.
    # Due to the code, it counts by 1 for every 2 clock cycles
    period = total / base_frq * 2
    
    return {
        "period":period,
        "duty_low":low/total,
        "duty":1.0-(low/total),
        "freq":1/period
        }

print("PWMIn Selfcheck")

for f in [100, 200, 500,
          1_000, 2_000, 5_000,
          10_000, 20_000, 50000,
          100_000, 200_000, 500_000]:
    for d in [0.1, 0.25, 0.5, 0.75, 0.9]:
        # Set new output
        pwm_out.freq(f)
        pwm_out.duty_u16(int((2**16-1)*d))
 
        # Wait a bit
        sleep(0.5)
        
        read = readPwm(sm)
        diff_freq = abs(read["freq"]-f)
        diff_duty = abs(read["duty"]-d)
        
        if (diff_freq <= f*0.01) and (diff_duty < 0.01):
            print("{} Hz / {} duty OK".format(f, d))
        else:
            print("{} Hz / {} duty OUTSIDE LIMITS ---------".format(f, d))
            
        print("\t{:.2f} Hz / {:.2f} duty cycle measured".format(read["freq"], read["duty"]))
            
        print("\tDiff: {:.2f} Hz".format(diff_freq))
        print("\tDiff: {:.2%} of freq".format(abs(1.0-read["freq"]/f)))
        print("\tDiff: {:.2%} duty cycle".format(diff_duty))
        print("")
