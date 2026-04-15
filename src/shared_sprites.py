# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# shared_sprites.py
#
# Shared Sprite Data, for use across multiple controller types.  Data, only
# so consumers can create instances of only the sprites they need.

# Sprite Data

# Directions (small, broad, arrows)
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
