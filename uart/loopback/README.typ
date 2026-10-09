= Using UART on the Raspberry Pi Pico

#let xrefstyle = [short]

Send data from the UART1 port to the UART0 port. Other things to try;

```python
uart0 = UART(0)
```

which will open a UART connection at the default baudrate of 115200, and

```python
uart0.readline()
```

which will read until the CR (\r) and NL (\n) characters, then return the line.

== Wiring information

See @uart-wiring-diagram for wiring instructions.

#figure(caption: [Wiring two of the Pico's ports together. Be sure to wire UART0 TX to UART1 RX and UART0 RX to UART1 TX.],
  image("pico_uart_example.png", width: 75%)
) <uart-wiring-diagram>

== List of Files

A list of files with descriptions of their function;

/ uart.py: \ The example code.

== Bill of Materials

#figure(
    table(
        columns: 3,
        table.header([*Item*], [*Quantity*], [Details]),
        [Breadboard], [1], [generic part],
        [Raspberry Pi Pico], [1], [https://www.raspberrypi.com/products/raspberry-pi-pico/],
  ), caption: [A list of materials required for the example]
) <uart-bom-table>
