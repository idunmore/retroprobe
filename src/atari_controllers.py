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
import time

I_WIDTH = 36
I_HEIGHT = 36

def draw_controller(screen, width, button, x, y):
	# Clear screen
	screen.fill(0)

	# Display the title
	screen.text("Atari CX40", 0, 0, 1)
	screen.hline(0, 12, width, 1)

	# Draw a broken outline
	screen.line(x + 3, y, x + I_WIDTH, y, 1)
	screen.line(x , y + 3, x, y + I_HEIGHT - 3, 1)
	screen.line(x + 3, y + I_HEIGHT, x + I_WIDTH, y + I_HEIGHT, 1)
	screen.line(x + 3 + I_WIDTH, y + I_HEIGHT -3 , x + I_WIDTH + 3, y + 3, 1)

	# Draw the corners
	screen.line(x + 3, y, x, y + 3, 1)
	screen.line(x, y + I_HEIGHT -3, x + 3, y + I_HEIGHT, 1)
	screen.line(x + I_WIDTH, y + I_HEIGHT, x + 3 + I_WIDTH, y + I_HEIGHT -3, 1)
	screen.line(x + I_WIDTH + 3, y + 3, x + I_WIDTH, y, 1)
	
	# Trigger and stick state
	screen.text("Button: FIRE", 48, 23, 1)
	screen.text(" Stick: UP", 48, 39, 1)

	# Exit line
	screen.text(" <[Select] to exit.>", 0, 56, 1)			    
	screen.show()

	# Allow for button release
	time.sleep(1)
	while button.value:
		print(button.value)
		pass

	# Allow for button release
	time.sleep(0.5)
	screen.fill(0)

def display_cx40(screen, width, button, x, y):
	draw_controller(screen, width, button, x, y)