= Using a SSD1306-based OLED graphics display

#let xrefstyle = [short]

Display an image and text on I2C driven SSD1306-based OLED graphics display.

== Wiring information

See @oled-wiring-diagram for wiring instructions.


#figure(caption: [Wiring the OLED to Pico using I2C],
  image("pico-and-oled.png", width: 75%)
) <oled-wiring-diagram>

== List of Files

A list of files with descriptions of their function;

/ i2c_1306oled_using_defaults.py: \ The example code.
/ i2c_1306oled_with_freq.py: \ The example code, explicitly sets a frequency.

== Bill of Materials

#figure(
    table(
        columns: 3,
        table.header([*Item*], [*Quantity*], [Details]),
        [Breadboard], [1], [generic part],
        [Raspberry Pi Pico], [1], [https://www.raspberrypi.com/products/raspberry-pi-pico/],
        [Monochrome 128x32 I2C OLED Display], [1], [https://www.adafruit.com/product/931],
  ), caption: [A list of materials required for the example]
) <oled-bom-table>
