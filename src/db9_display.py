# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.2.0 on 2026-04-20; Raspberry Pi Pico with rp2040

# Standard Modules
import time

# Retroprobe Modules
from drawing_primitives import filled_circle
import db9_port_probe
from common_display import clear_screen, clear_and_show_title

# Constants
PIN_RADIUS = 7
PIN_TEXT_OFFSET = 3

# Map of Pin Numbers (per DB9 connector) and their display coordinates.
# (Viewed from the front of the male DB9 socket; Pin 1 is top left)
pin_positions = {
	1: (25, 26), 2: (45, 26), 3: (65, 26), 4: (85, 26), 5: (105, 26),    
	6: (35, 48), 7: (55, 48), 8: (75, 48), 9: (95, 48)
}

def show_connections_flag(screen, enabled):
	if enabled:
		screen.circle(4, 32, 4, 1)
		screen.circle(4, 48, 4, 1)
		screen.line(4, 35, 4, 45, 1)

def draw_port(screen, connections, detected_pins, pin_states,
			  show_connections = False):
	'''Draws a DB9 port, showing pins and connection state'''
	clear_and_show_title(screen, "Male DB9 - Front View", 128)

	# Draw the port outline	
	screen.hline(10,16,108,1)
	screen.hline(20,58,88,1)
	screen.line(10,16,20,58,1)
	screen.line(118,16,108,58,1)

	# Draw the pins; empty circles if not connected to anything,
	# filled circles if the pin is connected.
	for pin, (x, y) in pin_positions.items():
		if pin in detected_pins:
			filled_circle(screen, x -1, y, PIN_RADIUS, 1)
			screen.text(str(pin), x - PIN_TEXT_OFFSET, y - PIN_TEXT_OFFSET, 0)  
		else:
			screen.circle(x - 1, y, PIN_RADIUS, 1)
			screen.text(str(pin), x - PIN_TEXT_OFFSET, y - PIN_TEXT_OFFSET, 1)

	# Only draw connections between pins, if requested
	if show_connections:
		show_connections_flag(screen, show_connections)
		draw_connections(screen, connections)

def draw_connections(screen, connections):
	'''Draws the connections between shorted pins'''
	drawn_connections = set()
	for pin_start, pin_end in connections:
		if (pin_end, pin_start) in drawn_connections:
			continue
		drawn_connections.add((pin_start, pin_end))
		x1, y1 = pin_positions[pin_start]
		x2, y2 = pin_positions[pin_end]
		mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
		if y1 == y2:
			mid_y -= 10
		else:
			mid_x += 10 if x1 < x2 else -10

		screen.line(x1, y1, mid_x, mid_y, 1)
		screen.line(mid_x, mid_y, x2, y2, 1)

def display_raw_db9(screen, width, select_button, next_button,
 					show_connections = False):
	'''Display the raw DB9 pin activations; exit on [Select]'''
	while True:
		connections, detected_pins, pin_states = db9_port_probe.probe_connections()
		draw_port(screen, connections, detected_pins, pin_states, show_connections)
		screen.show()
		time.sleep(0.05)

		# Toggle connection lines on/off when [Next] is pressed ... 
		if not next_button.value:
			show_connections = not show_connections
		
		# Exit this display when [Select] is pressed
		if not select_button.value:
			break

	# Allow for button release
	time.sleep(0.5)
	clear_screen(screen)