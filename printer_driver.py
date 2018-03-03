#!/usr/bin/env python
# encoding: utf-8
try:
	import serial	# Import the pySerial modules.
except:
	print('You do not have pySerial installed, which is needed to control the serial port.')
	print('Information on pySerial is at:\nhttp://pyserial.wiki.sourceforge.net/pySerial')

import os
import sys
import time


class SerialSender:
	"""
		A utility class for communication with the Arduino from python.
		Intended for g-code only. Raises ValueException if the arduino
		returns an unexpected response. Usually caused by sending invalid
		g-code.
	"""

	_verbose = False
	block = "empty"

	def __init__(self, port, baud, verbose=False):
		"""
			Opens the serial port and prepares for writing.
			port MUST be set, and values are operating system dependant.
		"""
		self._verbose = verbose

		if self._verbose:
			print >> sys.stdout, "Opening serial port: " + port

		#Timeout value 10" max travel, 1RPM, 20 threads/in = 200 seconds
		self.ser = serial.Serial(port, baud, timeout=200)

		if self._verbose:
			print >> sys.stdout, "Serial Open?: " + str(self.ser.isOpen())
			print >> sys.stdout, "Baud Rate: " + str(self.ser.baudrate)

	def reset(self):
		"""
			Resets the arduino by droping DTR for 1 second
			This will then wait for a response ("ready") and return.
		"""
		#Reboot the arduino, and wait for it's response
		if self._verbose:
			print "Resetting arduino..."

		self.ser.setDTR(0)
		# There is presumably some latency required.
		time.sleep(1)
		self.ser.setDTR(1)
		time.sleep(3)
		self.read("Start")

	def write(self, block):
		"""
			Writes one block of g-code out to arduino and waits for an "ok".
			This version will wait for an "ok" before returning and prints any intermediate output received.
			No error will be raised if non-ok response is received.  Loop in read() is infinite if "ok"
			does not come back!
			This routine also removes all whitespace before sending it to the arduino,
			which is handy for gcode, but will screw up if you try to do binary communications.
		"""
		if self._verbose:
			print "> " + block

		# The arduino GCode interperter firmware doesn't like whitespace
		# and if there's anything other than space and tab, we have other problems.
		block=block.strip()
		#Skip blank blocks.
		if len(block) == 0:
                        print("Blank Block")
			return

		self.ser.write(block + "\n")
                print(block)
		self.read("OK")

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
		while True:
			response = self.ser.readline().strip()
			if expect is None:
				return

			if expect.lower() in response.lower():
				if self._verbose:
					print "< " + response
				return
			else:
				#Just print the response since it is useful data or an error message
				print "< " + response


	def close():
		"""
			Closes the serial port, terminating communications with the arduino.
		"""
		if self._verbose:
			print >> sys.stdout, "Closing serial port."
		self.ser.close()

		if self._verbose:
			print >> sys.stdout, "Serial Open?: " + str(self.ser.isOpen())

printer = SerialSender("/dev/ttyACM0", 9600, verbose=True)
printer.write("G90")
printer.write("G1 X100 F3600")
printer.write("G1 X0 F3600")
printer.write("M32 top.gcode")
