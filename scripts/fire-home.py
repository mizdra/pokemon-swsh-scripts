#!/usr/bin/env python3
import argparse
import serial
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

def send(msg, duration=0):
    print(msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

ser = serial.Serial(args.port, 9600)

sleep(1)

send('Button B', 0.1)
sleep(2)
send('Button B', 0.1)
sleep(2)
send('Button HOME', 0.3)
sleep(0.7)

ser.close()
