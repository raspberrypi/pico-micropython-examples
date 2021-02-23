from machine import UART, Pin
from time import sleep_us

class myUART(UART):
    def readUntil(self, termination, maxlen=-1, includeTermination=True):
        result = ''
        while maxlen < 0 or len(result) < maxlen:
            if self.any():
                #print("here")
                result += chr(self.read(1)[0])
                #print(result)
                if result.endswith(termination):
                    if not includeTermination:
                        result = result[:-len(termination)]
                    break
            sleep_us(10)
        return result

uart = myUART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)

uart.write("AT+GMR\r\n")
print(uart.readUntil('OK',maxlen=-1, includeTermination=True))