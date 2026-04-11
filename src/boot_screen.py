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
import random

# Boot Screen Display (Placeholder)
def show_boot_screen(screen, width):
	while True:	    
	    screen.fill(0)

	    # Display the title
	    screen.text("RetroProbe by @Torq", 0, 0, 1)
	    screen.hline(0, 12, width, 1)

	    # Display shifting binary streams
	    for line in range(5):
	        bits = [random.randint(0, 1) for _ in range(21)]
	        bit_string = ''.join(map(str, bits))
	        screen.text(bit_string, 0, 16 + (line * 10), 1)

	    screen.show()