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

def draw_filled_circle(screen, x, y, radius, color):
    for i in range(-radius, radius):
        for j in range(-radius, radius):
            if i ** 2 + j ** 2 <= radius ** 2:
                screen.pixel(x + i, y + j, color)

def draw_triangle(screen, x, y, x1, y1, x2, y2, color):
	screen.line(x, y, x1, y1, color)
	screen.line(x1, y1, x2, y2, color)
	screen.line(x2, y2, x, y, color)