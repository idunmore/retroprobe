# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# Circuit Python & Adafruit Modules
import board
import busio
import digitalio

# Constants
NUM_PINS = 9
OFF = 0
ON = 1

# DB9 Connector Layout - Male Connector, Front View
#
#  1 2 3 4 5  |  GPIO pins 0 to 4 (left to right)
#   6 7 8 9   |  GPIO pins 5 to 8 (left to right)

# DB9 connector pins are numbered 1-9, but we're zero based, so DB9 pin 1 is
# GPIO pin 0 and, thus, db9_pins[0]
db9_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
			board.GP5, board.GP6, board.GP7, board.GP8]

# Create digital IO pin objects for db9 pins
pins = [digitalio.DigitalInOut(pin) for pin in db9_pins]

def probe_connections():
	'''
	Tests all pins in the pins[] array for connections to all other pins
	in the array, and returns all the connections, list of pins active and
	the states of each pin.
	'''
	connections = []
	detected_pins = set()
	pin_states = [OFF] * NUM_PINS

	# Test each pin ... where i and j are indexes of the pins being tested
	# to see if they connect to each other
	for i in range(len(pins)):
		# Set all pins to be Inputs with pull-up
		for pin in pins:
			pin.direction = digitalio.Direction.INPUT
			pin.pull = digitalio.Pull.UP

		# Make one pin and output, and turn it off
		pins[i].direction = digitalio.Direction.OUTPUT
		pins[i].value = False

		# Test pin i against all other pins
		for j in range(len(pins)):
			if i != j and not pins[j].value:
				if (j + 1, i + 1) not in connections:
					connections.append((i + 1, j + 1))

				detected_pins.add(i + 1)
				detected_pins.add(j + 1)
				pin_states[j] = ON
	
	return connections, detected_pins, pin_states

def are_pins_set(pins, pin_states):
	'''
	Checks to see if the pin positions marked as set (1) in "pins" are also set
	in pin_states[].  We don't compare unset (0) pins, and we don't care if
	other pins are set in pin_states[] but not in pins.
	'''
	for i, bit in enumerate(pins):
		if bit == "0": continue
		if bit == "1" and pin_states[i] != 1 : return False
	return True

def all_pins_set(pins, pin_states):
	'''
	Checks to see if ALL the pins marked as set (1) in "pins" are also set
	in pin_states[], and that all pins marked as unset (0) in "pins" are also
	unset in pin_states[].
	'''
	for i, bit in enumerate(pins):
		if bit == "0" and pin_states[i] != 0 : return False
		if bit == "1" and pin_states[i] != 1 : return False
	return True
