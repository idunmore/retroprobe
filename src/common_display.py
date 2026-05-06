# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.2.0 on 2026-04-20; Raspberry Pi Pico with rp2040

# common_display.py
#
# Common display functions for RetroProbe,

def clear_screen(screen):
	# Semantic helper for clearer, cleaner, modular code
	screen.fill(0)

def show_title(screen, name, width):
	# Display the title and a segregating line below
	screen.text(name, 0, 0, 1)
	screen.hline(0, 12, width, 1)

def clear_and_show_title(screen, name, width):
	# Clear the screen and show the title
	clear_screen(screen)
	show_title(screen, name, width)