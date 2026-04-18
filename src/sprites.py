# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# Circuit Python & Adafruit Modules
import adafruit_framebuf

# Classes

class Sprite:
	'''
	Simple "Sprite" class, using adafruit framebuf for source 1-bit color
	bitmaps and setting pixels in the display as they match those the buffer.
	'''
	def __init__(self, bitmap, width, height):
		'''Creates "sprite" from MHSBM format (1-bit/pixel) byte array.'''
		self._bitmap = adafruit_framebuf.FrameBuffer(
    		bitmap, width, height, adafruit_framebuf.MHMSB)
		self._width = width
		self._height = height
	
	def render(self, screen, x, y, transparent = False, invert = False):
		'''Render the Sprite data to the Screen'''
		for bitmap_y in range(self._height):
			for bitmap_x in range(self._width):
				pixel = self._bitmap.pixel(bitmap_x, bitmap_y)
				
				# Invert the pixel if inversion is set
				if invert:
					pixel = 1 if pixel == 0 else 0

				# Don't draw the pixel if it is a 0 and we want transparency
				if not transparent or pixel == 1:					
					screen.pixel(x + bitmap_x, y + bitmap_y, pixel)
