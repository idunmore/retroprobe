# Assembling RetroProbe

RetroProbe is easily assembled using a minimum number of parts.  It can be built on prototyping shields (solder and solder-less), perf-board, a custom PCB or assembled on a solder-less breadboard.

Connections between the primary components are as follows:

![RetroProbe](pi_pico_connections.png)

Where **two** connections are indicated in the "Pi Pico" column, those two pins (or the pin and ground) should be connected.  For example, DB9 Pin 1 is connected to GPIO pin 4 (GP4) and in turn to GPIO pin 27 (aka A1).

Connections to the MALE DE9 connector assume pin assignments are depicted below; for convince both front and rear (solder-side) PIN numbers are illustrated:

![RetroProbe](DE9_connections.png)

## Breadboard Assembly
RetroProbe can easily be built on a solder-less breadboard.

Two suggested layouts, that minimize the amount of external wiring required, are shown below.

The first is for the [official Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) RP2040 (green PCB, 2MB flash storage):

![RetroProbe](wiring_pi_official.png)

The second is for a common, cheaper, clone of the Raspberry Pi Pico RP2040 ([purple PCB](https://www.aliexpress.us/item/3256810075498433.html?gatewayAdapt=glo2usa), 16MB flash storage):

![RetroProbe](wiring_pi_clone.png)

**NOTE:** For the Pi clone assembly, ignore the pin vs. GND pad *shapes* and follow the actual pin designations on the board - this is an artifact of using a standard Pi Pico "part" in the diagram.

## Parts

The following is a list of parts required to do a solder-less build of RetroProbe via Amazon.

 - [0.96" OLED I2C SSD1306
   Display](https://www.amazon.com/dp/B09C5K91H7)
   
  
 - [Pi Pico RP2040 Microcontroller (w/ pre-soldered
   headers)](https://www.amazon.com/Raspberry-Pre-Soldered-Microcontroller-Development-Dual-Core/dp/B08X7HN2VG)
   
 - [DB9 Male Connector (w/ Screw
   Terminals)](https://www.amazon.com/dp/B0G2W6JVD1)
   
 - [Tactile Micro Momentary
   Switches](https://www.amazon.com/DAOKI-Miniature-Momentary-Tactile-Quality/dp/B01CGMP9GY)
   
 - [Breadboards (Solderless) w/ Jumper
   Wires](https://www.amazon.com/BOJACK-Values-Solderless-Breadboard-Flexible/dp/B08Y59P6D1)
   
 - [Resistor Kit (1%, 1/4W, metal film, 50
   values)](https://www.amazon.com/dp/B07P3MFG5D)
   
 - [Breadboard Jumper Wires
   (pre-formed)](https://www.amazon.com/dp/B08YRGVYPV)

For some parts, this involves buying kits of parts (sometimes with multiple additional values); this is for simplicity - you'll have all the parts required and more - and to avoid setting up vendor accounts/paying mutliple shipping fees.

You can use alternate sources (e.g., Mouser, Digi-Key, etc.) to find individual parts if you prefer, and will save money doing so, however not all of the solder-less parts are necessarily available there.
