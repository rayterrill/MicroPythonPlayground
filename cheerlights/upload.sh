#!/bin/bash

#ex: ./board.sh /dev/tty.usbserial-00E904FC

BOARD=$1

ampy --port $BOARD put boot.py
ampy --port $BOARD put captive_dns.py
ampy --port $BOARD put captive_http.py
ampy --port $BOARD put captive_portal.py
ampy --port $BOARD put connected.html
ampy --port $BOARD put credentials.py
ampy --port $BOARD put index.html
ampy --port $BOARD put main.py
ampy --port $BOARD put server.py
