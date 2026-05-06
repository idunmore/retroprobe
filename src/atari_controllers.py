# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.2.0 on 2026-04-20; Raspberry Pi Pico with rp2040

# atari_controllers.py
#
# Probe and Display Implementations for Atari Controllers

# Standard Modules
import time
import math
from collections import OrderedDict

# Retroprobe Modules
import db9_port_probe
import sprites
import shared_sprites
from drawing_primitives import *
from common_display import clear_screen, clear_and_show_title

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

# Paddle Constants

# Pins
PADDLE_0_DIAL_PIN = 1
PADDLE_0_TRIGGER_PIN = 3
PADDLE_1_DIAL_PIN = 0
PADDLE_1_TRIGGER_PIN = 2

# Dimenions and spacing for drawing the paddle controller
DIAL_RADIUS = 19
DIAL_DEAD_ZONE = 0.4
DIAL_CENTER_OFFSET = 5

# Keypad/Keyboard Constants

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
	'''
	Encapsulates a single paddle controller, with a dial and trigger.
	This simplifies handling multiple paddles simultaneously.
	'''

	# Internal Constants
	PADDLE_LOW_VAL = 0
	PADDLE_HIGH_VAL = 255
	PADDLE_VCC_PIN = 6
	PADDLE_GND_PIN = 7
	
	def __init__(self, dial_pin, trigger_pin):
		self._dial = db9_port_probe.analog_pins[dial_pin]
		self._trigger_pin = trigger_pin
		self.reset()		

	@property
	def position(self):
		self.__calc_range()
		return int(adafruit_simplemath.map_range(
			self._dial.value, self._paddle_min, self._paddle_max,
			self.PADDLE_LOW_VAL, self.PADDLE_HIGH_VAL))

	@property
	def trigger(self):		
		pin = db9_port_probe.pins[self._trigger_pin]
		pin.direction = digitalio.Direction.INPUT
		pin.pull = digitalio.Pull.UP
		return not pin.value		

	def __calc_range(self):
		raw_val = self._dial.value
		if raw_val > self._paddle_max:
			self._paddle_max = raw_val
		if raw_val < self._paddle_min:
			self._paddle_min = raw_val

	def reset(self):
		'''
		Resets the paddle's dial range values, and its virtual VCC/GND pins,
		both for intial use (during construction) and for optional reset
		while being actively used.
		'''
		# Setup surrogate/virtual VCC for the paddles dial ...
		self.vcc = db9_port_probe.pins[self.PADDLE_VCC_PIN]
		self.vcc.direction = digitalio.Direction.OUTPUT
		self.vcc.value = True
		# ... and a surrogate/virtual GND ...
		self.gnd = db9_port_probe.pins[self.PADDLE_GND_PIN]
		self.gnd.direction = digitalio.Direction.OUTPUT
		self.gnd.value = False
		# ... and finally reset the dial's range values
		self._paddle_max = 0
		self._paddle_min = 65535

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
		[(2, 5), (2, 7), (2, 9), (5, 7), (7, 9), (9, 5)])] = "5"
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
	clear_and_show_title(screen, name, width)
	
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
	clear_screen(screen)

def draw_keypad_controller(screen, width, button, x, y, name):
	clear_and_show_title(screen, name, width)	
	
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
	clear_screen(screen)

# Paddle Display

def draw_paddle_screen(screen, width, x, y, name):	
	clear_and_show_title(screen, name, width)

	# Vertical Separator
	screen.vline(width // 2, 22, 36, 1)

def draw_paddle_controller(screen, width, x, y, name):
	screen.circle(x + DIAL_RADIUS, y + DIAL_RADIUS, DIAL_RADIUS, 1)
	screen.circle(x + DIAL_RADIUS, y + DIAL_RADIUS, DIAL_RADIUS - 2, 1)

def draw_paddle_state(screen, x, y, paddle, show_dial_value = False):
	real = paddle.position
	trig = paddle.trigger

	# Draw a line representing the dial position, allowing for the fact
	# that the Paddle's range does not describe a full circle
	cx = x + DIAL_RADIUS
	cy = y + DIAL_RADIUS
	start_x = cx
	start_y = cy

	angle = adafruit_simplemath.map_range(
		real, Paddle.PADDLE_LOW_VAL, Paddle.PADDLE_HIGH_VAL,
		DIAL_DEAD_ZONE, (2 * math.pi) - DIAL_DEAD_ZONE)

	if show_dial_value:
		# Override the default starting point for the line, to make room
		# for the dial's value.
		start_x = cx + int(math.sin(angle) * DIAL_CENTER_OFFSET)
		start_y = cy - int(math.cos(angle) * DIAL_CENTER_OFFSET)
	
	end_x = cx + int(math.sin(angle) * (DIAL_RADIUS - 1))
	end_y = cy - int(math.cos(angle) * (DIAL_RADIUS - 1))

	screen.line(start_x, start_y, end_x, end_y, 1)

	if show_dial_value:
		# Show the dial's numeric value
		screen.text(f"[{real:3}]", x + DIAL_RADIUS - 14, y + 16, 1)

	# Now do the trigger
	if trig:
		# Draw the fire button		
		filled_bevelled_rect(screen, x - 8, y - 2, 6, 10, 2, 1)
	else:		
		bevelled_rect(screen, x - 8, y - 2, 6, 10, 2, 1)	

def display_paddle(screen, width, button_select, button_next,
	x, y, name="CX30 Paddle Controller", show_dial_value = False):
	# Allow for button release
	time.sleep(0.25)
	# Reset GPIO pin states in case other controller types have been used
	# and thier remnant-settings interfere with the paddle's dial reading	
	db9_port_probe.reset_gpio()
	paddle_0 = Paddle(PADDLE_0_DIAL_PIN, PADDLE_0_TRIGGER_PIN)
	paddle_1 = Paddle(PADDLE_1_DIAL_PIN, PADDLE_1_TRIGGER_PIN)

	while button_select.value:
		draw_paddle_screen(screen, width, x, y, name)
		draw_paddle_controller(screen, width, 12, 20, name)
		draw_paddle_controller(screen, width, 80, 20, name)
		draw_paddle_state(screen, 12, 20, paddle_0, show_dial_value)
		draw_paddle_state(screen, 80, 20, paddle_1, show_dial_value)
		screen.show()	

		# Toggle dial value display on [Next] button press
		if not button_next.value:
			show_dial_value = not show_dial_value

	# Allow for button release
	time.sleep(0.5)
	clear_screen(screen)