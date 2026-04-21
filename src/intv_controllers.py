# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# intv_controllers.py
#
# Probe and Display Implementations for Intellivision Controllers

# Standard Modules
import time

# Retroprobe Modules
import db9_port_probe
from drawing_primitives import *

# Constants

# Display offets and spacing
KEYPAD_X_OFFSET = 10
KEYPAD_X_SPACING = 12
KEYPAD_Y_SPACING = 12
KEY_WIDTH = 8
KEY_HEIGHT = 10

LEFT_ACTION_X_OFFSET = 2 
RIGHT_ACTION_X_OFFSET = 48
DISC_X_OFFSET = 90
DISC_Y_OFFSET = 24
DISC_DIR_TEXT_X = 96

# Pin state maps for the action buttons
PIN_BUTTON_MAP_TOP = "000001010"
PIN_BUTTON_MAP_LEFT = "000000110"
PIN_BUTTON_MAP_RIGHT = "000001100"

# Key and Pin to Keypad maps are linear, but result in the following layout:
key_label = ["1", "2", "3",
		  	 "4", "5", "6",
		  	 "7", "8", "9",
		  	 "C", "0", "E"]

pin_keypad_map = ["000101000", "000100100", "000100010",
				  "001001000", "001000100", "001000010",
				  "010001000", "010000100", "010000010",
				  "100001000", "100000100", "100000010"]

# Line End, and Name for Disc Directions - 16 Entries, Indexed by Pin State
pin_disc_map = {"010000000" : (90, 8, "N"),
				"010010001"	: (96, 7, "NNE"),
				"011000000" : (102, 14, "NE"),
				"110010001" : (84, 7, "NNW"),
				"110000000" : (78, 14, "NW"),
				"100010001" : (74, 20, "WNW"),				
				"100000000" : (72, 24, "W"),
				"100110001" : (74, 28, "WSW"),
				"011010001" : (106, 20, "ENE"),
				"001000000" : (108, 24, "E"),
				"001010001" : (106, 28, "ESE"),
				"000100000" : (90, 40, "S"),
				"001110001" : (96, 38, "SSE"),
				"001100000" : (102, 34, "SE"),
				"000110001" : (84, 38, "SSW"),
				"100100000" : (78, 34, "SW")}

def draw_controller(screen, width, x, y, name):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text(f"{name}", 0, 0, 1)
	screen.hline(0, 12, width, 1)	

	# Verticl Separator
	screen.vline(width // 2, 22, 36, 1)
	
	# Disc
	screen.circle(x + DISC_X_OFFSET, y + DISC_Y_OFFSET, 20, 1)
	screen.circle(x + DISC_X_OFFSET, y + DISC_Y_OFFSET, 18, 1)	

def draw_action_buttons(screen, x, y, pin_states):
	# Top Buttons - These work as one
	if db9_port_probe.are_pins_set(PIN_BUTTON_MAP_TOP, pin_states):
		filled_rect(screen, x + LEFT_ACTION_X_OFFSET, y + 13, 5, 9, 1)
		filled_rect(screen, x + RIGHT_ACTION_X_OFFSET, y + 13, 5, 9, 1)
	else:
		screen.rect(x + LEFT_ACTION_X_OFFSET, y + 13, 5, 9, 1)
		screen.rect(x + RIGHT_ACTION_X_OFFSET, y + 13, 5, 9, 1)

	# Bottom Left Button
	if db9_port_probe.are_pins_set(PIN_BUTTON_MAP_LEFT, pin_states):
		filled_rect(screen, x + LEFT_ACTION_X_OFFSET, y + 25, 5, 9, 1)
	else:
		screen.rect(x + LEFT_ACTION_X_OFFSET, y + 25, 5, 9, 1)

	# Bottom Right Button
	if db9_port_probe.are_pins_set(PIN_BUTTON_MAP_RIGHT, pin_states):
		filled_rect(screen, x + RIGHT_ACTION_X_OFFSET, y + 25, 5, 9, 1)
	else:
		screen.rect(x + RIGHT_ACTION_X_OFFSET, y + 25, 5, 9, 1)

def draw_keypad(screen, x, y, pin_states):
	for j in range(4):
		for i in range(3):
			if db9_port_probe.are_pins_set(
				pin_keypad_map[(j * 3) + i], pin_states):
				# Draw the activated key (filled key, black text)
				filled_bevelled_rect(screen,
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING),
					y + (j * KEYPAD_Y_SPACING), KEY_WIDTH, KEY_HEIGHT, 2, 1)
				
				screen.text(key_label[(j * 3) + i], 
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING) + 3,
					y + (j * KEYPAD_Y_SPACING) + 2, 0)
			else:
				# Draw the deactivated key (black key, white text)
				bevelled_rect(screen,
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING),
					y + (j * KEYPAD_Y_SPACING), KEY_WIDTH, KEY_HEIGHT, 2, 1)
				
				screen.text(key_label[(j * 3) + i],
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING) + 3,
					y + (j * KEYPAD_Y_SPACING) + 2, 1)

def draw_disc(screen, x, y, pin_states):
	for pin_state, disc_info in pin_disc_map.items():		
		if db9_port_probe.all_pins_set(pin_state, pin_states):
			# Draw a line indicating the direction being pressed ...
			screen.line(x + DISC_X_OFFSET, y + DISC_Y_OFFSET,
				x + disc_info[0], y + disc_info[1], 1)
			# ... and display the direction name in the top line, erasing
			# part of the name if it's too long and conflicts with the name
			screen.fill_rect(DISC_DIR_TEXT_X - 7, 0, 128-DISC_DIR_TEXT_X, 8, 0)
			screen.text(f'[{disc_info[2]}]', DISC_DIR_TEXT_X, 0, 1)

def draw_state(screen, x, y):
	# Get controller state
	connections, detected_pins, pin_states = db9_port_probe.probe_connections()

	# Handle the action buttons
	draw_action_buttons(screen, x, y, pin_states)
	draw_keypad(screen, x, y, pin_states)
	draw_disc(screen, x, y, pin_states)

def display_intv(screen, width, button, x, y, name = "Intellivision"):	
	# Allow for button release
	time.sleep(0.25)
	while button.value:
		draw_controller(screen, width, x, y, name)
		draw_state(screen, x, y)
		screen.show()

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)
