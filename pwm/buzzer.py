#Ref - https://micropython-on-wemos-d1-mini.readthedocs.io/en/latest/basics.html#beepers
"""
This script is originally written here -
https://micropython-on-wemos-d1-mini.readthedocs.io/en/latest/basics.html#beepers
But this is modified by Atul N Yadav - 26 Jan 2021 to work with
Raspberry Pi PICO
"""
from machine import Pin, PWM
import time
tempo = 5
tones = {
    'c': 262,
    'd': 294,
    'e': 330,
    'f': 349,
    'g': 392,
    'a': 440,
    'b': 494,
    'C': 523,
    ' ': 0,
}
beeper = PWM(Pin(16)) #, freq=440, duty=512)

#beeper.duty(512)  AttributeError: 'PWM' object has no attribute 'duty'

while(True):
    beeper.freq(1000)
    beeper.duty_u16(512)
    melody = 'cdefgabC'
    rhythm = [8, 8, 8, 8, 8, 8, 8, 8]
    for tone, length in zip(melody, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo/length)
         
    beeper.deinit()
    time.sleep(0.5)
    
    beeper.freq(1000)
    beeper.duty_u16(512)
    melody = 'Cbagfedc'
    rhythm = [8, 8, 8, 8, 8, 8, 8, 8]
    for tone, length in zip(melody, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo/length)
         
    beeper.deinit()
    time.sleep(0.5)
