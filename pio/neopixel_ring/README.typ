= Using PIO to drive a set of NeoPixel Ring (WS2812 LEDs)

#let xrefstyle = [short]

Combination of the PIO WS2812 demo with the Adafruit 'essential' NeoPixel example code to show off color fills, chases and of course a rainbow swirl on a 16-LED ring.

== Wiring information

See @neopixel-wiring-diagram for wiring instructions.

#figure(caption: [Wiring the 16-LED NeoPixel Ring to Pico],
  image("neopixel_ring.png", width: 75%)
) <neopixel-wiring-diagram>

== List of Files

A list of files with descriptions of their function;

/ neopixel_ring.py: \ The example code.

== Bill of Materials

#figure(
    table(
        columns: 3,
        table.header([*Item*], [*Quantity*], [Details]),
        [Breadboard], [1], [generic part],
        [Raspberry Pi Pico], [1], [https://www.raspberrypi.com/products/raspberry-pi-pico/],
        [NeoPixel Ring], [1], [https://www.adafruit.com/product/1463],
  ), caption: [A list of materials required for the example]
) <ring-bom-table>
