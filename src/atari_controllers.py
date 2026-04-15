# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# atari_controllers.py
#
# Probe and Display Implementations for Atari Controllers

# Standard Modules
import time

# Retroprobe Modules
import db9_port_probe
import sprites
from drawing_primitives import draw_filled_circle

# Sprite Data
dir_up = bytearray([
	0b00010000,
	0b00111000,
	0b01111100,
	0b11111110])

dir_down = bytearray([
	0b11111110,
	0b01111100,
	0b00111000,
	0b00010000])

dir_left = bytearray([
	0b00010000,
	0b00110000,
	0b01110000,
	0b11110000,
	0b01110000,
	0b00110000,
	0b00010000])

dir_right = bytearray([
	0b00001000,
	0b00001100,
	0b00001110,
	0b00001111,
	0b00001110,
	0b00001100,
	0b00001000])

# Sprites
sp_up = sprites.Sprite(dir_up, 8,4)
sp_down = sprites.Sprite(dir_down, 8,4)
sp_left = sprites.Sprite(dir_left, 8,7)
sp_right = sprites.Sprite(dir_right, 8,7)

# Constants

HEADER_Y_OFFSET = 16

# Tuple Indexes for pin_stick_map
I_SPRITE = 0
I_DIR = 1
I_X = 2
I_Y = 3

# Image size for CX40 and standard sticks
I_WIDTH = 36
I_HEIGHT = 36

# We only need to specify the non-common pins we want to test for, from left
# (GPIO 0/pin 1) to right (GPIO8/pin 9), and we can omit trailing zeros.
pin_stick_map = {'1': (sp_up, "UP", 17,5),
				 '01': (sp_down, "DN", 17,28),
				 '001': (sp_left, "LE", 7,15),
				 '0001': (sp_right, "RI", 26, 15) }				 

pin_trigger_map = '000001'

def draw_controller(screen, width, button, x, y):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text("Atari CX40", 0, 0, 1)
	screen.hline(0, 12, width, 1)

	# Draw a broken outline
	screen.line(x + 3, y, x + I_WIDTH, y, 1)
	screen.line(x , y + 3, x, y + I_HEIGHT - 3, 1)
	screen.line(x + 3, y + I_HEIGHT, x + I_WIDTH, y + I_HEIGHT, 1)
	screen.line(x + 3 + I_WIDTH, y + I_HEIGHT -3 , x + I_WIDTH + 3, y + 3, 1)

	# Draw the corners
	screen.line(x + 3, y, x, y + 3, 1)
	screen.line(x, y + I_HEIGHT -3, x + 3, y + I_HEIGHT, 1)
	screen.line(x + I_WIDTH, y + I_HEIGHT, x + 3 + I_WIDTH, y + I_HEIGHT - 3, 1)
	screen.line(x + I_WIDTH + 3, y + 3, x + I_WIDTH, y, 1)
	
	# Draw the stick's base
	screen.circle(x + (I_WIDTH // 2) + 2, y + (I_HEIGHT // 2), 5, 1)
	screen.circle(x + (I_WIDTH // 2) + 2, y + (I_HEIGHT // 2), 8, 1)

	# Draw the fire button
	screen.circle(x + 7, y + 7, 4, 1)

	# Trigger and stick state
	screen.text("Button:", x + 48, (y - HEADER_Y_OFFSET) + 23, 1)
	screen.text(" Stick:", x + 48, (y - HEADER_Y_OFFSET) + 39, 1)

	# Exit line
	screen.text(" <[Select] to exit.>", 0, 56, 1)			    
	
def draw_state(screen, x, y):
	connections, detected_pins, pin_states = db9_port_probe.probe_connections()
	# If pin 8 (GND) isn't set, then no other pins matter
	if pin_states[7] == 0: return

	# Do trigger
	if db9_port_probe.are_pins_set(pin_trigger_map, pin_states):
		# Draw the fire button
		draw_filled_circle(screen, x + 7, y + 7, 3, 1)
		screen.text("FIRE", x + 91, (y - HEADER_Y_OFFSET) + 23, 1)

	# Do stick
	stick_dir = ''
	for k, v in pin_stick_map.items():
		if db9_port_probe.are_pins_set(k, pin_states):			
			v[I_SPRITE].render(screen, v[I_X] + x, v[I_Y] + y, 1)
			stick_dir += v[I_DIR] if len(stick_dir) == 0 else f'+{v[I_DIR]}'			
	screen.text(stick_dir, x + 91, (y - HEADER_Y_OFFSET) + 39, 1)

def display_cx40(screen, width, button, x, y):	
	# Allow for button release
	time.sleep(0.25)
	while button.value:
		draw_controller(screen, width, button, x, y)
		draw_state(screen, x, y)
		screen.show()

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)



