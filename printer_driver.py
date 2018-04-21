#!/usr/bin/env python
# encoding: utf-8
try:
    import serial   # Import the pySerial modules.
except:
    print('You do not have pySerial installed, which is needed to control the serial port.')
    print('Information on pySerial is at:\nhttp://pyserial.wiki.sourceforge.net/pySerial')

import os
import sys
import time


class Printer:
    """
        A utility class for communication with the Arduino from python.
        Intended for g-code only. Raises ValueException if the arduino
        returns an unexpected response. Usually caused by sending invalid
        g-code.
    """

    _verbose = False
    block = "empty"

    def __init__(self, port, baud, mp=True, verbose=False):
        """
            Opens the serial port and prepares for writing.
            port MUST be set, and values are operating system dependant.
        """
        self._verbose = verbose
        self.busy = False
        self.is_mp = mp

        if self._verbose:
            print( "Opening serial port: " + port)

        #Timeout value 10" max travel, 1RPM, 20 threads/in = 200 seconds
        # self.ser = serial.Serial(port, baud, rtscts=True, timeout=15)
        self.ser = serial.Serial(port, baud, dsrdtr=True, timeout=2.0)

        time.sleep(0.1)
        time.sleep(0.1)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        if self._verbose:
            print(sys.stdout, "Serial Open?: " + str(self.ser.isOpen()))
            print(sys.stdout, "Baud Rate: " + str(self.ser.baudrate))

    def reset(self):
        """
            Resets the arduino by droping DTR for 1 second
            This will then wait for a response ("ready") and return.
        """
        #Reboot the arduino, and wait for it's response
        if self._verbose:
            print("Resetting arduino...")

        self.ser.setDTR(0)
        # There is presumably some latency required.
        time.sleep(1)
        self.ser.setDTR(1)
        time.sleep(3)
        self.read("Start")

    def write(self, block, resp=False):
        """
            Writes one block of g-code out to arduino and waits for an "ok".
            This version will wait for an "ok" before returning and prints any intermediate output received.
            No error will be raised if non-ok response is received.  Loop in read() is infinite if "ok")i
            does not come back!
            This routine also removes all whitespace before sending it to the arduino,
            which is handy for gcode, but will screw up if you try to do binary communications.
        """
        self.ser.flushInput()
        self.ser.flushOutput()
        if self._verbose:
            print("> " + block)

        # The arduino GCode interperter firmware doesn't like whitespace
        # and if there's anything other than space and tab, we have other problems.
        block=block.strip()
        #Skip blank blocks.
        if len(block) == 0:
            print("Blank Block")
            return None

        self.ser.flush()
        self.ser.write( (block + "\n").encode() )
        print("Writing : " + block)
        if resp:
            return None
        return self.read("OK")

    def read(self, expect=None):
        """
            This routine should never be called directly. It's used by write() and reset()
            to read a one-line response from the Arduino.
            This version will wait for an "ok" before returning and prints any intermediate output received.
            No error will be raised if non-ok response is received.  Loop is infinite if "ok"
            does not come back!
        """
        #The g-code firmware returns exactly ONE line per block of gcode sent.
        #Unless it is M104, M105 or other code that returns info!!
        #It WILL return "ok" once the command has finished sending and completed.
        print(expect)
        while True:
            print("__________________________")
            response = self.ser.readline().strip()
            print("response", response)
            if expect is None:
                return None

            if expect.lower() in response.lower():
                if self._verbose:
                    print("< " + response)
                return response
            else:
                #Just print the response since it is useful data or an error message
                # print "< " + response
                return response


    def close():
        """
            Closes the serial port, terminating communications with the arduino.
        """
        if self._verbose:
            print(sys.stdout, "Closing serial port.")
        self.ser.close()

        if self._verbose:
            print(sys.stdout, "Serial Open?: " + str(self.ser.isOpen()))

    def start_print_from_sd(self, sd_file):
        self.busy = True
        print("____________________________________")
        print("Printing file: " + sd_file)
        print(self.write("M23 " + sd_file))
        time.sleep(0.5)
        self.write("M400")
        time.sleep(0.5)
        print(self.write("M24"))
        time.sleep(0.5)
        print(self.write("M400"))
        time.sleep(0.5)

    def is_busy(self):
        return self.busy

    def is_finished(self):
        for _ in range(1):
            time.sleep(10)
            response = self.write("M27") # check on SD print status
            if response == "":
                return False
            ratio = [int(s) for s in response.split()[-1].split("/") if s.isdigit()]
            if not len(ratio) == 2:
                return False
            print(ratio)
            r = ratio[0]/ratio[1]
            print(self.write("M400"))
            print(response)
            if r == 1:
                print("Finished Printing")
                time.sleep(1.0)
                self.busy = False
                self.removal_pos()
                self.write("M400") # Waitf for current move to finish
                time.sleep(1.0)
                return True
        return False

    def removal_pos(self):
        self.write("G28 X Y") # Home X and Y axis
        self.write("G90")
        # z 40 for now for speed of tests
        self.write("G0 X0 Y0 Z40 F10000")
        self.write("M400")
        # self.write("G0 X0 Y100 Z100 F10000")

    def startup(self):
        self.write("G28 X Y") # Home X and Y axis
        print("x")
        self.write("M104 S199") # Set extruder temperature to 199 degrees celcius
        print("a")
        self.write("M140 S59k") # Set bed temperature to 59 degrees celcius
        print("a")
        self.write("M21") # Set bed temperature to 59 degrees celcius
        print("c")
        time.sleep(0.4)
