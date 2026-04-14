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

# Retroprobe Modules
import db9_port_probe

# Map of Pin Numbers (per DB9 connector) and their display coordinates.
# (Viewed from the front of the male DB9 socket; Pin 1 is top left)
pin_positions = {
    1: (25, 26), 2: (45, 26), 3: (65, 26), 4: (85, 26), 5: (105, 26),    
    6: (35, 42), 7: (55, 42), 8: (75, 42), 9: (95, 42)
}

def draw_filled_circle(screen, x, y, r, color):
    '''Draws a filled circle of radius are, centered at x, y'''
    for i in range(-r, r):
        for j in range(-r, r):
            if i**2 + j**2 <= r**2:
                screen.pixel(x + i, y + j, color)

def draw_port(screen, connections, detected_pins, pin_states):
    '''Draws a DB9 port, showing pins and connection state'''
    screen.fill(0)
    screen.text("Male DB9 - Front View", 0, 0, 1)

    # Draw the port outline
    screen.hline(0,12,128,1)
    screen.hline(10,16,108,1)
    screen.hline(20,53,88,1)
    screen.line(10,16,20,53,1)
    screen.line(118,16,108,53,1)

    # Draw the pins; empty circles if not connected to anything,
    # filled circles if the pin is connected.
    for pin, (x, y) in pin_positions.items():
        if pin in detected_pins:
            draw_filled_circle(screen, x -1, y, 7, 1)
            screen.text(str(pin), x - 3, y - 3, 0)  
        else:
            screen.circle(x - 1, y, 7, 1)
            screen.text(str(pin), x - 3, y - 3, 1)

    screen.text(" <[Select] to exit.>", 0, 56, 1)
    screen.show()

def display_raw_db9(screen, width, button):
	'''Display the raw DB9 pin activations; exit on [Select]'''
	while True:
		connections, detected_pins, pin_states = db9_port_probe.probe_connections()
		draw_port(screen, connections, detected_pins, pin_states)
		time.sleep(0.05)
		if not button.value: break
