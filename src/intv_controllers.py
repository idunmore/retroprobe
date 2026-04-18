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
import sprites
from drawing_primitives import filled_circle, bevelled_rect, filled_bevelled_rect

# Constants
KEYPAD_X_OFFSET = 10
LEFT_ACTION_X_OFFSET = 2 
RIGHT_ACTION_X_OFFSET = 48
DISC_X_OFFSET = 90
DISC_Y_OFFSET = 24

matrix = ['1', '4', '7', 'C', '2', '5', '8', '0', '3', '6', '9', 'E']

def draw_controller(screen, width, button, x, y):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text("Intellivision 1", 0, 0, 1)
	screen.hline(0, 12, width, 1)

	for i in range(3):
		for j in range(4):
			bevelled_rect(screen, x + KEYPAD_X_OFFSET + (i * 12), y + (j * 12), 8, 10, 2, 1)
			screen.text(matrix[(i * 4) + j], x + KEYPAD_X_OFFSET + (i * 12) + 3, y + (j * 12) + 2, 1)

	# Verticl Separator
	screen.vline(width // 2, 22, 36, 1)
	
	# Action Buttons

	# Top Buttons - These work as one
	screen.rect(x + LEFT_ACTION_X_OFFSET, y + 13, 5, 9, 1)
	screen.rect(x + RIGHT_ACTION_X_OFFSET, y + 13, 5, 9, 1)

	# Bottom Buttons - These are individual
	screen.rect(x + LEFT_ACTION_X_OFFSET, y + 25, 5, 9, 1)	
	screen.rect(x + RIGHT_ACTION_X_OFFSET, y + 25, 5, 9, 1)

	# Disc
	screen.circle(x + DISC_X_OFFSET, y + DISC_Y_OFFSET, 20, 1)
	screen.circle(x + DISC_X_OFFSET, y + DISC_Y_OFFSET, 18, 1)	

def display_intv(screen, width, button, x, y):	
	# Allow for button release
	time.sleep(0.25)
	while button.value:
		draw_controller(screen, width, button, x, y)
		#draw_state(screen, x, y)
		screen.show()

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)
