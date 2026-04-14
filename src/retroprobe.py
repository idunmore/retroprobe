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

# Display the Boot Screen
boot_screen.show_boot_screen(screen, SCREEN_WIDTH)

# Setup "Select" and "Next" navigation buttons
button_next = create_button(board.GP16)
button_select = create_button(board.GP17)

# Build an example/placeholder menu for testing
atari_joysticks = Menu("Joysticks")
atari_joysticks.add(MenuItem("CX10 Joystick", launch_game("CX10")))
atari_joysticks.add(MenuItem("CX40 Joystick", launch_game("CX40")))
atari_joysticks.add(MenuItem("CX78 Gamepad",  launch_game("CX78")))
atari_joysticks.add(MenuItem("CX80 Trackball", launch_game("CX80")))
atari_joysticks.add(MenuItem("CX81 Trackball", launch_game("CX81")))

atari = Menu("Atari")
atari.add(MenuItem("Atari 2600",   launch_game("Atari 2600")))
atari.add(MenuItem("Atari 5200",   launch_game("Atari 5200")))
atari.add(atari_joysticks)

intellivision = Menu("Intellivision")
intellivision.add(MenuItem("Intellivision I",  launch_game("Intellivision I")))
intellivision.add(MenuItem("Intellivision II", launch_game("Intellivision II")))

coleco = Menu("ColecoVision")
coleco.add(MenuItem("ColecoVision", launch_game("ColecoVision")))
coleco.add(MenuItem("Coleco VCS Adapter", launch_game("Coleco VCS Adapter")))

sega = Menu("SEGA")
sega.add(MenuItem("Master System", launch_game("Master System")))
sega.add(MenuItem("Genesis/MegaDrive", launch_game("Genesis/MegaDrive")))

standard = Menu("Standard DB9")
standard.add(MenuItem("DB9 (Pins-Only)",
				lambda:db9_display.display_raw_db9(
			 		screen, SCREEN_WIDTH, button_select, False)))
standard.add(MenuItem("DB9 (w/ Connections)",
				lambda:db9_display.display_raw_db9(
					screen, SCREEN_WIDTH, button_select, True)))

root = Menu("Main Menu")
root.add(atari)
root.add(coleco)
root.add(intellivision)
root.add(standard)
#root.add(sega)
root.add(MenuItem("Info",
		lambda: info_screen.show_info_screen(
			screen, SCREEN_WIDTH, button_select)))

# Let the MenuSystem run the Menu and dispatch operations accordingly
MenuSystem(root, screen, button_select, button_next, False).run()