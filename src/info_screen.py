# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040

# Standard Modules
import sys
import time

# Retroprobe Modules
from common_display import clear_screen, clear_and_show_title

# Info Screen Display
def show_info_screen(screen, width, button):	
	clear_and_show_title(screen, "RetroProbe Info", width)

	# Retroprobe version
	screen.text("v.0.0.6a/2026-05-03", 0, 16, 1)

	# Python (Micro Python) and Circuit Python versions
	ver = sys.version
	mpy_ver = ver[:ver.find(";")]
	cpy_ver = ver[ver.find("n ") + 2:ver.rfind(" o")]	
	screen.text(f"mp:{mpy_ver}/cp:{cpy_ver}", 0, 26, 1)
	screen.text("Pi Pico RP2040/16MB",0, 36, 1)
	screen.text("(C) 2026, IMD Labs",0, 46, 1)
	screen.text("<[Select] to exit.>", 0, 56, 1)			    
	screen.show()

	# Allow for button release
	time.sleep(1)
	while button.value:
		pass

	# Allow for button release
	time.sleep(0.5)
	clear_screen(screen)