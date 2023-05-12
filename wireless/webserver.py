import network
import socket
import time

from machine import Pin

led = Pin(15, Pin.OUT)

ssid = 'YOUR NETWORK NAME'
password = 'YOUR NETWORK PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024).decode()
        print(request)

        led_on = '/light/on' in request
        led_off = '/light/off' in request
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        if led_on:
            print("led on")
            led.on()
            text = "LED is ON"

        elif led_off:
            print("led off")
            led.off()
            text = "LED is OFF"

        else:
            print("no LED command")
            text = "Access the /light/on and /light/off pages to control the LED!"

        response = html % text

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError:
        cl.close()
        print('connection closed')