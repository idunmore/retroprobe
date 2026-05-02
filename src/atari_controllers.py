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
from collections import OrderedDict

# Retroprobe Modules
import db9_port_probe
import sprites
import shared_sprites
from drawing_primitives import filled_circle, bevelled_rect, filled_bevelled_rect

# Circuit Python & Adafruit Modules
import board
import analogio
import digitalio
import adafruit_simplemath

# Sprites
sp_up = sprites.Sprite(shared_sprites.dir_up, 8,4)
sp_down = sprites.Sprite(shared_sprites.dir_down, 8,4)
sp_left = sprites.Sprite(shared_sprites.dir_left, 8,7)
sp_right = sprites.Sprite(shared_sprites.dir_right, 8,7)

# Constants

HEADER_Y_OFFSET = 16

# Tuple Indexes for pin_stick_map
I_SPRITE = 0
I_DIR = 1
I_X = 2
I_Y = 3

# CX40 Constants

# Image size for CX40 and standard sticks
I_WIDTH = 36
I_HEIGHT = 36

# CX 40 Pins

# Ground on CX40 is pin 8, which maps to GPIO pin 7
CX40_GND_PIN = 7 

# We only need to specify the non-common pins we want to test for, from left
# (GPIO 0/pin 1) to right (GPIO8/pin 9), and we can omit trailing zeros.
pin_stick_map = {"1": (sp_up, "UP", 17,5),
				 "01": (sp_down, "DN", 17,28),
				 "001": (sp_left, "LE", 7,15),
				 "0001": (sp_right, "RI", 26, 15) }				 

pin_trigger_map = "000001"

paddle0_max = 0
paddle0_min = 65535
paddle1_max = 0
paddle1_min = 65535

# Keypad/Keyboard Constants

# Paddle Constants
PADDLE_0_DIAL_PIN = 1
PADDLE_0_TRIGGER_PIN = 3
PADDLE_1_DIAL_PIN = 0
PADDLE_1_TRIGGER_PIN = 4
PADDLE_VCC_PIN = 6
PADDLE_GND_PIN = 7

paddle0_dial = db9_port_probe.analog_pins[PADDLE_0_DIAL_PIN]
paddle1_dial = db9_port_probe.analog_pins[PADDLE_1_DIAL_PIN]

# Setup a surrogate VCC pin (digital output, True, at 3.3v) to drive the pot
vcc = db9_port_probe.pins[PADDLE_VCC_PIN]
vcc.direction = digitalio.Direction.OUTPUT
vcc.value = True

# Display offets and spacing
KEYPAD_X_OFFSET = 40
KEYPAD_X_SPACING = 16
KEYPAD_Y_SPACING = 12
KEY_WIDTH = 10
KEY_HEIGHT = 10

# Empty Keypad Maps
keypad_connection_map = OrderedDict()
key_labels = []
keys = []

# Paddle Class
class Paddle:

	PADDLE_LOW_VAL = 0
	PADDLE_HIGH_VAL = 255

	def __init__(self, dial_pin, trigger_pin):
		self._dial = db9_port_probe.analog_pins[dial_pin]
		self._trigger = db9_port_probe.pins[trigger_pin]

		self._paddle_max = 0
		self._paddle_min = 65535

	@property
	def position(self):
		self._calc_range()
		pos = int(adafruit_simplemath.map_range(
			self._dial.value, self._paddle_min, self._paddle_max,
			PADDLE_LOW_VAL, PADDLE_HIGH_VAL))

		return pos

	def __calc_range(self):
		raw_val = self._dial_value
		if raw_val > self._paddle_max:
			self._paddle_max = raw_val
		if raw_val < self._paddle_min:
			self._paddle_min = raw_val


def connections_to_key(connections):
	return ", ".join([f"{a}-{b}" for a, b in connections])

def build_keypad_maps():
	# Connection Dictionary w/ labels for CX21, CX50 (etc.)		
	keypad_connection_map[connections_to_key(
		[(1, 5), (1, 7), (1, 9), (5, 7), (5, 9), (7, 9)])] = "1"
	keypad_connection_map[connections_to_key(
		[(1, 5), (1, 7), (1, 9), (5, 7), (7, 9), (9, 5)])] = "2"
	keypad_connection_map[connections_to_key(
		[(1, 6), (5, 7), (5, 9), (7, 9)])] = "3"
	keypad_connection_map[connections_to_key(
		[(2, 5), (2, 7), (2, 9), (5, 7), (5, 9), (7, 9)])] = "4"
	keypad_connection_map[connections_to_key(
		[(2, 5), (2, 7), (2, 9), (5, 7), (7, 9), (9,5)])] = "5"
	keypad_connection_map[connections_to_key(
		[(2, 6), (5, 7), (5, 9), (7, 9)])] = "6"
	keypad_connection_map[connections_to_key(
		[(3, 5), (3, 7), (3, 9), (5, 7), (5, 9), (7, 9)])] = "7"
	keypad_connection_map[connections_to_key(
		[(3, 5), (3, 7), (3, 9), (5, 7), (7, 9), (9, 5)])] = "8"
	keypad_connection_map[connections_to_key(
		[(3, 6), (5, 7), (5, 9), (7, 9)])] = "9"
	keypad_connection_map[connections_to_key(
		[(4, 5), (4, 7), (4, 9), (5, 7), (5, 9), (7, 9)])] = "*"
	keypad_connection_map[connections_to_key(
		[(4, 5), (4, 7), (4, 9), (5, 7), (7, 9), (9, 5)])] = "0"
	keypad_connection_map[connections_to_key(
		[(4, 6), (5, 7), (5, 9), (7, 9)])] = "#"
	keypad_connection_map[connections_to_key(
		[(5, 7), (5, 9), (7, 9)])] = "?"

	# Indexable list of Key Labels, for drawing keypad
	key_labels.extend([v for v in keypad_connection_map.values()])

	# Indexable List of Key Pressesd (by connection map key), for checking
	# key state during drawing
	keys.extend([k for k in keypad_connection_map.keys()])

def draw_joystick_controller(screen, width, button, x, y, name):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text(name, 0, 0, 1)
	screen.hline(0, 12, width, 1)

	# Draw the stick outline
	bevelled_rect(screen, x, y, I_WIDTH, I_HEIGHT, 3, 1)
	
	# Draw the stick's base
	screen.circle(x + (I_WIDTH // 2) + 2, y + (I_HEIGHT // 2), 5, 1)
	screen.circle(x + (I_WIDTH // 2) + 2, y + (I_HEIGHT // 2), 8, 1)

	# Draw the fire button
	screen.circle(x + 7, y + 7, 4, 1)

	# Trigger and stick state
	screen.text("Button:", x + 48, (y - HEADER_Y_OFFSET) + 23, 1)
	screen.text(" Stick:", x + 48, (y - HEADER_Y_OFFSET) + 39, 1)	    
	
def draw_joystick_state(screen, x, y):
	connections, detected_pins, pin_states = db9_port_probe.probe_connections()
	# If pin 8 (GND) isn't set, then no other pins matter
	if pin_states[CX40_GND_PIN] == 0: return

	# Do trigger
	if db9_port_probe.are_pins_set(pin_trigger_map, pin_states):
		# Draw the fire button
		filled_circle(screen, x + 7, y + 7, 3, 1)
		screen.text("FIRE", x + 91, (y - HEADER_Y_OFFSET) + 23, 1)

	# Do stick
	stick_dir = ""
	for k, v in pin_stick_map.items():
		if db9_port_probe.are_pins_set(k, pin_states):			
			v[I_SPRITE].render(screen, v[I_X] + x, v[I_Y] + y, 1)
			stick_dir += v[I_DIR] if len(stick_dir) == 0 else f"+{v[I_DIR]}"			
	screen.text(stick_dir, x + 91, (y - HEADER_Y_OFFSET) + 39, 1)

def display_joystick(screen, width, button, x, y, name="CX40 Joystick"):	
	# Allow for button release
	time.sleep(0.25)
	while button.value:
		draw_joystick_controller(screen, width, button, x, y, name)
		draw_joystick_state(screen, x, y)
		screen.show()

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)

def draw_keypad_controller(screen, width, button, x, y, name):
	# Clear the screen
	screen.fill(0)

	# Display the title
	screen.text(name, 0, 0, 1)
	screen.hline(0, 12, width, 1)
	screen.vline(KEYPAD_X_OFFSET - 7, 20, 40, 1)
	screen.vline(KEYPAD_X_OFFSET + (3 * KEYPAD_X_SPACING) + 4, 20, 40, 1)
	
def draw_keypad_state(screen, x, y):
	# Get the current connections and their corresponding dictionary key
	connections, detected_pins, pin_states = db9_port_probe.probe_connections()	
	key = connections_to_key(connections)
	
	# Draw the keypad, row by row
	for j in range(4):
		for i in range(3):
			index = (j * 3) + i
			key_pressed = False
			if key == keys[index]:
				# Draw the activated key (filled key, black text)
				filled_bevelled_rect(screen,
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING),
					y + (j * KEYPAD_Y_SPACING), KEY_WIDTH, KEY_HEIGHT, 2, 1)				
				key_pressed = True
			else:
				# Draw the deactivated key (black key, white text)
				bevelled_rect(screen,
					x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING),
					y + (j * KEYPAD_Y_SPACING), KEY_WIDTH, KEY_HEIGHT, 2, 1)
				
			# Show key label; inverted color if key is pressed
			screen.text(key_labels[index],
				x + KEYPAD_X_OFFSET + (i * KEYPAD_X_SPACING) + 4,
				y + (j * KEYPAD_Y_SPACING) + 2,
				1 if not key_pressed else 0)

def display_keypad(screen, width, button, x, y, name="Atari Keypad Controller"):
	# Allow for button release
	time.sleep(0.25)	

	build_keypad_maps()	
	
	while button.value:
		draw_keypad_controller(screen, width, button, x, y, name)
		draw_keypad_state(screen, x, y)
		screen.show()

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)		


def draw_paddle_controller(screen, width, button, x, y, name):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text(name, 0, 0, 1)
	screen.hline(0, 12, width, 1)
	
def draw_paddle_state(screen, x, y):
	paddle_range = 0
	raw = paddle0_dial.value
	# print(f"Raw Dial Value: {raw}")
	global paddle0_max, paddle0_min
	if raw > paddle0_max:
		paddle0_max = raw
	if raw < paddle0_min:
		paddle0_min = raw		
	
	real = int(adafruit_simplemath.map_range(raw, paddle0_min, paddle0_max, 0, 255))

	print(f"Real Dial Value: {real}") 	

def display_paddle(screen, width, button, x, y, name="CX30 Paddle Controller"):
	# Allow for button release
	time.sleep(0.25)	

	build_keypad_maps()	
	
	while button.value:
		draw_paddle_controller(screen, width, button, x, y, name)
		draw_paddle_state(screen, x, y)
		screen.show()

	global paddle_max, paddle_min
	paddle_max = 0
	paddle_min = 65535
	
	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)		