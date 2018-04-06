#!/usr/bin/env python

try:
    import serial   # Import the pySerial modules.
except:
    print('You do not have pySerial installed, which is needed to control the serial port.')
    print('Information on pySerial is at:\nhttp://pyserial.wiki.sourceforge.net/pySerial')

import sys
import time

if len(sys.argv) < 2:
    raise ValueError('No serial port provided')

ser = serial.Serial(sys.argv[1], 115200, timeout=10)

# Reset the Arduino
ser.setDTR(0)
time.sleep(1)
ser.setDTR(1)
time.sleep(3)

if ser.readline().strip() != 'Ready':
    raise ValueError('Received unexpected response from Arduino')

try:
    while True:
        ser.write('a1000 b1000')
        time.sleep(1)
        ser.write('a2000 b2000')
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    ser.close()
