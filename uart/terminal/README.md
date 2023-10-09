# Pico serial terminal

A simple example to allow a Pico to act as a serial terminal into another Raspberry Pi computer.
Useful for setting up a Pi when network setup fails for some reason.
Should work for Windows, Linux, or Mac host machines.

1. Add `enable_uart=1` to the Raspberry Pi computer `config.txt` and boot it.
2. Connect pins `pico:{1,2,3}` to `pi:{10,8,6}`
3. Connect to Pico using [Thonny][thonny]
4. From Thonny, run `terminal.py` on Pico, then power up the Pi

[thonny]: https://thonny.org/

You should now have a serial terminal to your Raspberry Pi computer through your Pico.

### Errata / Bugs

* Input is only taken a whole line at a time after the EOL character.
* Line input is ALWAYS echoed back to the terminal as a new line, even passwords
* Control characters are dropped so no curses tools (like `raspi-config`) work

For a full-fledged serial interface, look at [picoprobe][probe] referenced in Appendix A of the [Pico Getting Started Guide][get-start].

[get-start]: https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf#page=61
[probe]: https://github.com/raspberrypi/picoprobe/
