#!/usr/bin/env python

try:
    import serial
except:
    print('You do not have pySerial installed, which is needed to control the serial port.')
    print('Information on pySerial is at:\nhttp://pyserial.wiki.sourceforge.net/pySerial')

import sys
import time

def send_command(ser, command):
    ser.write(command)
    response = ser.readline().strip()
    if response != 'OK':
        raise ValueError('Received unexpected response from Arduino: {}'.format(response))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise ValueError('Provide the servo Arduino serial port, the winch Arduino serial port, and a printer ID')

    servo_ser = serial.Serial(sys.argv[1], 115200, timeout=30)
    winch_ser = serial.Serial(sys.argv[2], 115200, timeout=30)

    # # Reset the Arduinos
    # servo_ser.setDTR(0)
    # winch_ser.setDTR(0)
    # time.sleep(0.1)
    # servo_ser.setDTR(1)
    # winch_ser.setDTR(1)
    # time.sleep(0.1)

    if servo_ser.readline().strip() != 'Ready':
        raise ValueError('Received unexpected response from servo Arduino')

    if winch_ser.readline().strip() != 'Ready':
        raise ValueError('Received unexpected response from winch Arduino')

    send_command(winch_ser, "i {}".format(sys.argv[3]))
    send_command(servo_ser, "c")
    send_command(winch_ser, "o 75")
    send_command(servo_ser, "f")
    send_command(winch_ser, "o -75")
    send_command(servo_ser, "o")
    send_command(winch_ser, "i 0")
    send_command(winch_ser, "h")

    servo_ser.close()
    winch_ser.close()
