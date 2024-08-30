from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
