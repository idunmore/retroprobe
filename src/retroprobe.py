# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# Standard Modules

# Circuit Python & Adafruit Modules
import board
import busio
import digitalio
import adafruit_ssd1306
import adafruit_framebuf

# Retroprobe Modules
import boot_screen
import info_screen
import db9_display
import atari_controllers
import intv_controllers
from menu import *

# Hardware Constants

# Screen Dimensions (in pixels)
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# I2C Channel Pins for Bus 1 w/ SDD1306 OLED Driver
I2C_SDA = board.GP12
I2C_SCL = board.GP13

# Utility Functions
def create_button(gpio_pin):
	'''Creates a "button"; a GPIO pin configured for digital input.'''
	button = digitalio.DigitalInOut(gpio_pin)
	button.direction = digitalio.Direction.INPUT
	button.pull = digitalio.Pull.UP
	return button

# Placeholder Functions
def launch_game(name):
    return lambda: print(f"Launching {name}...")

# Initialize Screen
i2c = busio.I2C(I2C_SCL, I2C_SDA)
screen = adafruit_ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# Setup "Select" and "Next" navigation buttons
button_next = create_button(board.GP16)
button_select = create_button(board.GP17)

# Display the Boot Screen
boot_screen.show_boot_screen(screen, SCREEN_WIDTH, button_select)

# Add Atari Controller Categories and Controllers to the Menu
atari = Menu("Atari")

atari_joysticks = Menu("Joysticks")
atari_joysticks.add(MenuItem("CX10 Joystick",
		lambda:atari_controllers.display_joystick(
			screen,	SCREEN_WIDTH, button_select, 4, 21, "CX10 Joystick")))
atari_joysticks.add(MenuItem("CX40 Joystick",
		lambda:atari_controllers.display_joystick(
			screen,	SCREEN_WIDTH, button_select, 4, 21, "CX40 Joystick")))

atari_keypads = Menu("Keypads")
atari_keypads.add(MenuItem("CX21 Video Touch Pad",
		lambda:atari_controllers.display_keypad(
			screen,	SCREEN_WIDTH, button_select, 0, 16, "CX21 Video Touch Pad")))
atari_keypads.add(MenuItem("CX50 Keyboard",
		lambda:atari_controllers.display_keypad(
			screen,	SCREEN_WIDTH, button_select, 0, 16, "CX50 Keyboard")))

atari_paddles = Menu("Paddles")
atari_paddles.add(MenuItem("CX30 Paddle",
		lambda:atari_controllers.display_paddle(
			screen,	SCREEN_WIDTH, button_select, button_next, 0, 16,
			"CX30 Paddle", False)))
atari_paddles.add(MenuItem("CX30 (w/ Dial Value)",
		lambda:atari_controllers.display_paddle(
			screen,	SCREEN_WIDTH, button_select, button_next, 0, 16,
			"CX30 Paddle", True)))

atari.add(atari_joysticks)
atari.add(atari_keypads)
atari.add(atari_paddles)

# Intellivision Controllers and Categories
intellivision = Menu("Intellivision")
intellivision.add(MenuItem("Intellivision",
		lambda:intv_controllers.display_intv(
			screen, SCREEN_WIDTH, button_select, 4, 16, "Intellivision")))
intellivision.add(MenuItem("Intellivision 2",
		lambda:intv_controllers.display_intv(
			screen, SCREEN_WIDTH, button_select, 4, 16, "Intellivision 2")))
intellivision.add(MenuItem("Super Video Arcade",
		lambda:intv_controllers.display_intv(
			screen, SCREEN_WIDTH, button_select, 4, 16, "Super Video Arcade")))

# Raw Port Probe Options
standard = Menu("Raw 9-pin DSUB")
standard.add(MenuItem("DB9 (Pins-Only)",
				lambda:db9_display.display_raw_db9(
			 		screen, SCREEN_WIDTH, button_select, button_next, False)))
standard.add(MenuItem("DB9 (w/ Connections)",
				lambda:db9_display.display_raw_db9(
					screen, SCREEN_WIDTH, button_select, button_next, True)))

root = Menu("RetroProbe Main Menu")
root.add(atari)
root.add(intellivision)
root.add(standard)
root.add(MenuItem("Info",
		lambda: info_screen.show_info_screen(
			screen, SCREEN_WIDTH, button_select)))

# Let the MenuSystem run the Menu and dispatch operations accordingly
MenuSystem(root, screen, button_select, button_next, False, True).run()