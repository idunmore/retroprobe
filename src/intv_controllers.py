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
from drawing_primitives import draw_filled_circle

# Character Sprites (5x3)
sp_zero = bytearray([0b11111000, 0b10001000, 0b11111000])
sp_one = bytearray([0b10010000,	0b11111000,	0b10000000])
sp_two = bytearray([0b11101000,	0b10101000,	0b10111000])
sp_three = bytearray([0b10001000, 0b10101000, 0b11111000])
sp_four = bytearray([0b00111000, 0b00100000, 0b11111000])
sp_five = bytearray([0b10111000, 0b10101000, 0b11101000])
sp_six = bytearray([0b11111000, 0b10101000,	0b11101000])
sp_seven = bytearray([0b00001000, 0b11101000, 0b00011000])
sp_eight = bytearray([0b11111000, 0b10101000, 0b11111000])
sp_nine = bytearray([0b10111000, 0b10101000, 0b11111000])
sp_clear = bytearray([0b11111000, 0b10001000, 0b10001000])
sp_enter = bytearray([0b11111000, 0b10101000, 0b10001000])

spr_zero = sprites.Sprite(sp_zero, 8, 3)
spr_one = sprites.Sprite(sp_one, 8, 3)
spr_two = sprites.Sprite(sp_two, 8, 3)
spr_three = sprites.Sprite(sp_three, 8, 3)
spr_four = sprites.Sprite(sp_four, 8, 3)
spr_five = sprites.Sprite(sp_five, 8, 3)
spr_six = sprites.Sprite(sp_six, 8, 3)
spr_seven = sprites.Sprite(sp_seven, 8, 3)
spr_eight = sprites.Sprite(sp_eight, 8, 3)
spr_nine = sprites.Sprite(sp_nine, 8, 3)
spr_clear = sprites.Sprite(sp_clear, 8, 3)
spr_enter = sprites.Sprite(sp_enter, 8, 3)

matrix = [spr_clear, spr_seven, spr_four, spr_one,
          spr_zero, spr_eight,  spr_five, spr_two,
          spr_enter, spr_nine, spr_six, spr_three]

def draw_controller(screen, width, button, x, y):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text("Intellivision 1", 0, 0, 1)
	screen.hline(0, 12, width, 1)

	for i in range(0, 3):
		for j in range(0, 4):
			index = (i * 4) + j
			sx = x + 34 + (j * 10)
			sy = y + 12 + (i * 9)
			screen.rect(sx - 2, sy - 2, 9, 7, 1)
			screen.rect(sx - 1, sy - 1, 7, 5, 1)
			matrix[index].render(screen, sx, sy, False, True)
			#screen.rect(sx - 2, sy - 2, 9, 7, 1)
			screen.circle(17,39, 12, 1)

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
