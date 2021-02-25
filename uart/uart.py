from machine import UART, Pin
import time

uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

txData = b'hello world\n\r'
uart1.write(txData)
time.sleep(1)
rxData = bytes()
while uart0.any() > 0:
    rxData += uart0.read()
    
print(rxData.decode('utf-8'))