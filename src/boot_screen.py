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

# Retroprobe Modules
import sprites

# Sprite Data
squid_open = bytearray([0x0F, 0x00,	0x7F, 0xE0, 0xFF, 0xF0,	0xE6, 0x70,
					   	0xFF, 0xF0,	0x19, 0x80,	0x36, 0xC0,	0xC0, 0x30])

squid_closed = bytearray([0x0F, 0x00, 0x7F, 0xE0, 0xFF, 0xF0, 0xE6, 0x70,
						  0xFF, 0xF0, 0x39, 0xC0, 0x66, 0x60, 0x30, 0xC0])

crab_open = bytearray([0x20, 0x80, 0x91, 0x20, 0xBF, 0xA0, 0xEE, 0xE0,
					   0xFF, 0xE0, 0x7F, 0xC0, 0x20, 0x80, 0x40, 0x40])

crab_closed = bytearray([0x20, 0x80, 0x11, 0x00, 0x3F, 0x80, 0x6E, 0xC0,
						 0xFF, 0xE0, 0xBF, 0xA0, 0xA0, 0xA0, 0x1B, 0x00])

jelly_open = bytearray([0x18, 0x3C,	0x7E, 0xDB,	0xFF, 0x24,	0x5A, 0xA5])

jelly_closed = bytearray([0x18,	0x3C, 0x7E,	0xDB, 0xFF, 0x5A, 0x81,	0x42])

spr_squid_open = sprites.Sprite(squid_open, 16, 8)
spr_squid_closed = sprites.Sprite(squid_closed, 16, 8)
spr_crab_open = sprites.Sprite(crab_open, 16, 8)
spr_crab_closed = sprites.Sprite(crab_closed, 16, 8)
spr_jelly_open = sprites.Sprite(jelly_open, 8, 8)
spr_jelly_closed = sprites.Sprite(jelly_closed, 8, 8)

# Boot Screen Display (Placeholder)
def show_boot_screen(screen, width, button):
	
	exit = False

	for i in range(19):	    
		screen.fill(0)

		# Display the title
		screen.text("RetroProbe by @Torq", 0, 0, 1)
		screen.hline(0, 12, width, 1)

		# Display the sprites, alternating between open and closed states
		for x in range(7):
			if i % 2 == 0:
				spr_squid_open.render(screen, x * 16 + i, 25)
				spr_crab_open.render(screen, x * 16 + 1 + i, 35)
				spr_jelly_open.render(screen, x * 16 + 2 + i, 45)
			else:
				spr_squid_closed.render(screen, x * 16 + i, 25)
				spr_crab_closed.render(screen, x * 16 + 1 + i, 35)
				spr_jelly_closed.render(screen, x * 16 + 2 + i, 45)

			if not button.value:
				exit = True
				break

		screen.show()
		if not button.value or exit:
			break

# Boot Screen Display (Placeholder)
# def show_boot_screen(screen, width, button):
# 	for i in range(10):	    
# 		screen.fill(0)

# 		# Display the title
# 		screen.text("RetroProbe by @Torq", 0, 0, 1)
# 		screen.hline(0, 12, width, 1)

# 		# Draw random bits to simulate "booting"
# 		for line in range(5):
# 			bits = [random.randint(0, 1) for _ in range(21)]
# 			bit_string = ''.join(map(str, bits))
# 			screen.text(bit_string, 0, 16 + line * 10, 1)
		
# 		screen.show()

# 		# Allow button to exit the boot screen early
# 		if not button.value:
# 			break
		