#!/usr/bin/env python3
import argparse
import serial
from time import sleep
from datetime import date

from util.controller import Controller

# ## スクリプトの書式
# ```
# $ ./scripts/manual.py /dev/tty.usbserial*
# ```

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()
ser = serial.Serial(args.port, 9600)
controller = Controller(ser, date(2000, 1, 1))

sleep(1)

controller.manual()
