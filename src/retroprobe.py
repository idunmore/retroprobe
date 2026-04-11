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

# Hardware Constants

# Screen Dimensions (in pixels)
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# I2C Channel Pins for Bus 1 w/ SDD1306 OLED Driver
I2C_SDA = board.GP12
I2C_SCL = board.GP13

# Initialize Screen
i2c = busio.I2C(I2C_SCL, I2C_SDA)
screen = adafruit_ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# Display the Boot Screen
boot_screen.show_boot_screen(screen, SCREEN_WIDTH)
