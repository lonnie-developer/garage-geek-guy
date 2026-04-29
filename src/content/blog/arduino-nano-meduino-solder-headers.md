---
title: 'Arduino Nano Unboxing and Soldering the Headers (Meduino Clone)'
description: 'Three Meduino Nano clones arrive from eBay — same ATmega328P as the Uno, but small enough to live on the breadboard. Here is how to solder the headers so it actually stays there.'
pubDate: 'August 14 2012'
youtubeId: 'w9Ru2k_K-4s'
heroImage: '../../assets/posts/arduino-nano-meduino-solder-headers/thumbnail.jpg'
tags: ['arduino', 'nano', 'soldering', 'meduino', 'atmega328p']
---

*This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

There's a shape problem with the Arduino Uno that nobody talks about. It's a fine board, but it's a rectangle with female headers on one side and a barrel jack on the other, and once you add a breadboard and the wires connecting the two you've committed a meaningful chunk of your project's real estate to just keeping the brain talking to the prototype area. For a permanent build in a project box that's tolerable. For a little robot chassis where you're already fighting for every square centimeter, it starts to feel like a lot.

The Arduino Nano solves this in the most direct way possible: it's the same ATmega328P running at the same 16 MHz, with the same number of I/O pins, just compressed down to a board about the size of a stick of gum. And — this is the part that changes how you think about layouts — it plugs directly into the breadboard. The Nano straddles a breadboard's center gap, its pins drop into rows on both sides, and suddenly you have one thing where you used to have two things and a rat's nest between them.

This post walks through picking up three Meduino Nanos from eBay, what you get for about $12.60 a piece, and how to solder the header pins so the board actually seats properly on a breadboard.

## The Nano vs. the Uno: what's actually the same

The ATmega328P is the chip. Both the Nano and the Uno run one. Same 32 KB of flash, same 2 KB of SRAM, same 1 KB of EEPROM, same 14 digital I/O pins (6 of which do PWM), same 8 analog inputs. You write the same Arduino sketches for both, you use the same libraries, the IDE doesn't care which board you're targeting once you've selected the right one in the board menu.

The differences are about form factor and a couple of edge cases. The Nano doesn't have a DC barrel jack — you power it over USB or through the VIN pin. It uses a Mini-B USB connector rather than the standard USB-A that the Uno uses. And the USB-to-serial bridge chip is often different: the Nano commonly uses a CH340G or FT232RL rather than the ATmega16U2 on later Unos. That last point matters if you're on macOS and your board isn't showing up in the port list — you may need to install a CH340 driver separately.

There's also a 3.3V/5V mode switch on the Nano (and its clones) that you won't find on the Uno. At 3.3V mode the board runs at reduced speed — handy if you're interfacing with 3.3V sensors without a level shifter, less useful for general-purpose work. For almost everything you'll do at the bench, leave it at 5V.

## What's a Meduino?

The Meduino is a clone — a third-party board built around the ATmega328P that replicates the Nano's pinout, dimensions, and USB connectivity. These arrived from Guangdong, China, shipped in small plastic bags. At $12.60 plus $1.50 shipping per board, they were meaningfully cheaper than official Nanos at the time. Three boards shipped together for about $42 total.

What you give up with a clone is usually the official branding, the silkscreen quality, and occasionally the USB chip — the Meduino uses a CH340G rather than the FTDI FT232RL. The CH340 drivers were not pre-installed on Windows at the time, so you sometimes had to hunt them down. Today the situation is better: modern Arduino IDE versions handle the CH340 transparently on most systems. The functional capabilities are otherwise identical to an official Nano.

## Soldering the headers

The Nano ships with the header pins separate — two strips of breakaway male headers that need to be soldered in. This is a 10-minute job if you're comfortable with a soldering iron, and the breadboard itself makes it easier than it looks.

The trick is to use the breadboard as a fixture. Drop both header strips into the breadboard rows where the Nano will eventually sit, then lay the Nano on top with its holes resting on the pin shanks. The breadboard holds the pins upright and at the correct spacing while you work. Without it you're trying to hold the board flat, keep the pins vertical, and apply solder simultaneously — not impossible, but annoying.

The pin pads on the Nano are small. You don't need much solder — enough to form a small dome over each pad and pin shank, that's it. A common beginner mistake is trying to build a big bead; what you actually want is the solder wicking in by capillary action when you hold the iron to the joint for a second or two. A cold joint shows up as a dull, grainy-looking surface rather than a smooth shiny dome. If you see one, reheat it and let a fresh bit of solder flow.

Going back over a joint you're unsure about is fine. The pad isn't going anywhere and these aren't particularly heat-sensitive components. A bad joint that stays bad is much more annoying to debug later than spending an extra ten seconds on it now.

One thing that's harder to see than you expect: the solder going into the joint. These are small pads and at normal working distance it's hard to tell whether the solder has flowed fully around the pin or just bridged the top. A side-view check after each row — get your eye down to bench level and look along the line of pins — will show you quickly whether the domes are formed symmetrically or if something looks flat or bridged.

## What you have at the end

Once the headers are soldered the Nano plugs into the breadboard and stays there. The pins on both sides give you direct access to every I/O line, power, and ground without a single jumper wire connecting two separate boards. VIN, 5V, 3.3V, and two GND pins are all available. Every digital pin is accessible. The analog pins are on the opposite side.

This becomes useful immediately if you're building anything where the Arduino is embedded in the project rather than sitting alongside it. On a robot chassis, being able to snap the Nano directly onto the control breadboard means the brain and the prototype circuit are a single unit — easier to route wires, easier to mount, and less likely to fall apart when the chassis vibrates.

The Meduino ships with the Blink sketch pre-loaded, which you'll see running as soon as you power it up. That's the same default sketch as the Uno. From there, point the Arduino IDE at "Arduino Nano" in the board list, select the right COM port, and you're writing and uploading code exactly the same way you always have.

## What you'll need

- Arduino Nano or compatible clone (Meduino, or any ATmega328P-based Nano-footprint board)
- Two strips of breakaway male header pins (usually included with the board)
- Soldering iron (a $30 station beats a $10 RadioShack wand, but either will work)
- Solder (60/40 or 63/37 rosin-core, thin gauge)
- A breadboard to use as a soldering fixture

## References and further reading

- [Arduino Nano product page](https://store.arduino.cc/products/arduino-nano) — official specs and pinout diagram
- [Arduino Comparison Guide — SparkFun](https://learn.sparkfun.com/tutorials/arduino-comparison-guide/atmega328-boards) — ATmega328 board comparison
- [ATmega328P datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf) — the definitive reference for the chip underneath both boards
- [CH340 driver information](https://sparks.gogo.co.nz/ch340.html) — if your Nano clone isn't showing up in the port list
