#!/bin/zsh

Help()
{
	# Display Help
	echo "RetroProbe - build.sh Script"
	echo
	echo "Syntax: build.sh [clean|h|help]"
	echo "  options:"
	echo "    clean       - Perform a clean build (destroys dist/)."
	echo "    -h | --help - Displays this Help info."
	echo
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
	Help
	exit
fi

# Clean the dist/ folder if requested
if [ "$1" = "clean" ]; then
	echo "Cleaning ..."
	cd dist/
	rm -rf *
	cd ..	
fi

# The build is simply copying and/or compiling files from their origins to
# dist/ following a structure that can be directly copied to the Circuit
# Python file systems

# Do libraries
mkdir -p dist/lib
cp lib/adafruit_displayio_ssd1306.mpy dist/lib/adafruit_displayio_ssd1306.mpy
cp lib/adafruit_framebuf.mpy dist/lib/adafruit_framebuf.mpy
cp lib/adafruit_ssd1306.mpy dist/lib/adafruit_ssd1306.mpy

# Do fonts
cp fonts/font5x8.bin dist/font5x8.bin

# Do code
cp src/code.py dist/code.py
mpy-cross src/retroprobe.py -o dist/retroprobe.mpy
mpy-cross src/boot_screen.py -o dist/boot_screen.mpy
mpy-cross src/info_screen.py -o dist/info_screen.mpy
mpy-cross src/menu.py -o dist/menu.mpy
mpy-cross src/sprites.py -o dist/sprites.mpy
mpy-cross src/db9_port_probe.py -o dist/db9_port_probe.mpy
mpy-cross src/db9_display.py -o dist/db9_display.mpy
mpy-cross src/drawing_primitives.py -o dist/drawing_primitives.mpy
mpy-cross src/shared_sprites.py -o dist/shared_sprites.mpy
mpy-cross src/atari_controllers.py -o dist/atari_controllers.mpy
exit
