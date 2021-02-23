from machine import UART, Pin

uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), bits=8, parity=None, stop=1)
uart1.write(b'UART on GPIO8&9 at 9600 baud\n\r')

uart0 = UART(0)
uart0.write(b'UART on GPIO0&1 at 115200 baud\n\r')

rxData = bytes()
while uart0.any() > 0:
    rxData += uart0.read(1)

print(rxData)