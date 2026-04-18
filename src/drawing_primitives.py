# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# drawing_primitives.py
#
# Additional drawing primitives for Adafruit_framebuf and SSD1306

def filled_circle(screen, x, y, radius, color):
    for i in range(-radius, radius):
        for j in range(-radius, radius):
            if i ** 2 + j ** 2 <= radius ** 2:
                screen.pixel(x + i, y + j, color)

def triangle(screen, x, y, x1, y1, x2, y2, color):
	screen.line(x, y, x1, y1, color)
	screen.line(x1, y1, x2, y2, color)
	screen.line(x2, y2, x, y, color)

def filled_rect(screen, x, y, width, height, color):
    for i in range(x, x + width):
        for j in range(y, y + height):
            screen.pixel(i, j, color)

def bevelled_rect(screen, x, y, width, height, bevel, color):
    # Draw a broken outline
	screen.line(x + bevel, y, x + width, y, color)
	screen.line(x , y + bevel, x, y + height - bevel, color)
	screen.line(x + bevel, y + height, x + width, y + height, color)
	screen.line(x + bevel + width, y + height -bevel , x + width + bevel, y + bevel, color)

	# Draw the corners
	screen.line(x + bevel, y, x, y + bevel, color)
	screen.line(x, y + height -bevel, x + bevel, y + height, color)
	screen.line(x + width, y + height, x + width + bevel, y + height - bevel, color)
	screen.line(x + width + bevel, y + bevel, x + width, y, color)

def filled_bevelled_rect(screen, x, y, width, height, bevel, color):
    # Draw the top bevelled area
    for i in range(bevel):
        screen.line(x + bevel - i, y + i, x + (width - bevel) + bevel + i, y + i, color)
    # Then fill the area between the top and bottom bevels        
    for i in range(height - (bevel * 2)):
        screen.line(x, y + bevel + i, x + width + bevel, y + bevel + i, color)
    # Finally, draw the bottom bevelled area
    for i in range(bevel + 1):
        screen.line(x + i, y + i + height - bevel,
            x + width + bevel - i, y + i + height - bevel, color)    

    