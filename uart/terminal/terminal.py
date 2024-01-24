#!/usr/bin/env micropython
from _thread import start_new_thread
from machine import UART, Pin

UART0 = 0 # uart0 is the FIRST uart
TX=0      # Default Pin number for TX on Pico uart0
RX=1      # Default Pin number for RX on Pico uart0
VS=2      # comment reminder: DONT FORGET to connect the common Ground (VSS)

uart = UART(UART0, 115200, parity=None, bits=8, stop=1, tx=Pin(TX, Pin.OUT), rx=Pin(RX, Pin.IN))

# Type a line (plus enter) in REPL to transmit down UART
def TX():
    while True:
        line = input() + "\n"
        uart.write(line.encode())

# Busy thread to relay EVERY character arriving from uart
def RX():
    while True:
        recv = uart.read()
        if(recv):
            try:
                print(recv.decode(), end='')
            except UnicodeError:
                # Caught a control char in buffer, eject it and move along
                fix = [x for x in recv if x <= 127]
                print(bytes(fix).decode(), end='')

# Run busy thread on second processor
start_new_thread(RX, tuple([]))
# Run input wait on this (BSP) processor
TX()
