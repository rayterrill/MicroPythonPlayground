# Setup

1. Install esptool (later versions didn't appear to work correctly)
```
pip3 install esptool==1.3
```
2. Download latest firmware from: https://micropython.org/download/esp8266/
3. Connect device to your computer and find the serial port:
  * Mac:
  ```
  ls /dev/tty.*
  ```
4. Erase flash:
```
python3 -m esptool --port /dev/tty.usbserial-00E904FC --baud 125000 erase_flash
```
5. Install with esptool:
```
python3 -m esptool --port /dev/tty.usbserial-00E904FC --baud 125000 write_flash 0 ~/Downloads/esp8266-1m-20220117-v1.18.bin
```
6. At this point, you should be able to connect with wifi to your board (AP: MicroPython-******), and connect via serial to the REPL with something like:
```
screen /dev/tty.usbserial-00E904FC 115200
```

### Running Code on the Board in Real Time
```
ampy --port /dev/tty.usbserial-00E904FC run main.py
```

### Pushing Code to the Board
```
ampy --port /dev/tty.usbserial-00E904FC put main.py
```