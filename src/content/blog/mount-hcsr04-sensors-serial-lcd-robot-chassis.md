---
title: 'Two-Story Robot Chassis — Mounting 4 HC-SR04 Sensors and a Serial LCD'
description: 'Running out of room inside the cardboard chassis means adding another box on top. Here is the two-deck build: stacking a Stellaris launchpad box on top of the robot, cutting slots for four HC-SR04 sensors, mounting a serial LCD in the front panel, and why serial beats parallel when pins are running low.'
pubDate: 'October 08 2012'
youtubeId: 'URGjWwuNToE'
heroImage: '../../assets/posts/mount-hcsr04-sensors-serial-lcd-robot-chassis/thumbnail.jpg'
tags: ['arduino', 'robot', 'chassis', 'hc-sr04', 'lcd', 'tutorial']
---

The single-box cardboard chassis had a problem: the motor gearbox, TB6612FNG motor driver, Arduino Nano, and battery packs filled the interior. There was no clean way to mount four ultrasonic sensors pointing outward, run their wiring inside, and also fit an LCD display — not without the whole thing looking like a rat's nest and being impossible to service.

The solution: a second box on top. Two decks, each with its own function. The lower box keeps everything it already has. The upper deck is exclusively for sensors and the display.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The two-box design

The top deck comes from a Stellaris Launchpad shipping box — slightly smaller than the bottom box, but the same footprint. Gorilla Glue bonds the two boxes lid-to-lid. A roll of packing tape holds the lid closed while the glue sets (at least 12 hours). Once cured, the result opens like a clamshell from two directions: lift the top box for access to the sensor and display deck, or open the bottom box for access to electronics and batteries.

The advantages over adding more stuff to a single box: each deck can be opened independently, components on both levels stay accessible, and there's a clean physical separation between moving parts / power components (bottom) and sensors / display (top).

## Modifying the HC-SR04s for slotted mounting

Standard HC-SR04 sensors come with male header pins. To mount them flush through slots in cardboard, those headers need to go — female headers soldered in their place let Dupont cables connect directly to the sensor from behind without any pins protruding.

The process: desolder the existing male header pins, clean the pads, then solder female headers in the same holes. Standard desoldering braid works fine. This takes about 5 minutes per sensor.

**Cutting the sensor slots:** mark the slot positions on the top box face with a marker, using the sensor body as a template. Score along the marks with a box cutter in multiple shallow passes rather than trying to cut through in one go — cardboard tears instead of cuts if you apply too much force at once. The sensors slot in from outside to inside, fitting snugly enough that hot glue only needs to fill the gaps rather than bear the full load.

Sensor positions on the top deck: two at the front (angled slightly left and right of center), one on each side facing perpendicular. This gives the robot 270° of sensing coverage without having to rotate.

## Serial LCD instead of parallel

The display is a serial LCD (SparkFun-style serial interface, sometimes called a "serial backpack" or "serial character LCD") rather than the parallel HD44780 wiring or an I²C backpack. Serial LCDs use a single wire for data — they only need one digital pin plus power and ground.

The reason for choosing serial here: the Arduino Nano is already spending a lot of pins on sensors and motor control. A parallel LCD would claim 6 digital pins. An I²C LCD would take A4 and A5. A serial LCD takes just one digital pin. With four HC-SR04 sensors (8 pins for trig/echo), the TB6612FNG (6 pins), and power connections, pin budget is tight. Serial was the right call.

The tradeoff is cost: serial LCD modules run around $10–12, versus $3–5 for a plain LCD with a parallel interface. For a project where pin count is the constraint, that premium is worth it.

## Mounting the LCD

The LCD gets a cutout in the front face of the top deck, sized to let the display bezel sit flush. Mark the cutout from behind using the display as a template, score and cut with a box cutter. Getting the hole right-sized matters — too large and the display falls through; too tight and you're trimming after the fact.

Before gluing the display in place, build up a small hot-glue pad on the side opposite the backlight housing. The backlight protrudes slightly on one side, and without a shim the display sits crooked. The glue pad levels it out.

Securing the display: hot glue was attempted but ran out mid-job. Packing tape turned out to work surprisingly well — the display fits snugly enough in the cutout that tape holding the edges keeps it firmly in place. A small trimmer pot on the back of the display adjusts contrast; leave it accessible.

## What this build enables

With the two-story chassis complete: four sensors facing outward from the top deck, display visible from the front, wiring running down through a hole between decks to the electronics below. The [wiring post](/blog/wire-4-hcsr04-sensors-i2c-lcd-robot) covers connecting all four sensors to the Nano's digital pins, and the [code post](/blog/arduino-robot-4-hcsr04-sensors-code) covers reading them sequentially and displaying distances on the LCD.

The cardboard construction isn't pretty, but it's the kind of chassis that actually gets built in an evening and then revised over the following weeks as the project evolves. Version two — if it ever happens — will be informed by everything this version taught about sensor placement, cable routing, and the practical constraints of fitting all this hardware into a rolling platform.

## References and further reading

- [Tamiya twin motor gearbox (Item #70168)](https://www.tamiyausa.com/shop/educational-construction/twin-motor-gearbox-kit/) — the drive system on this chassis
- [Cardboard chassis build post](/blog/diy-arduino-robot-chassis-cardboard) — the original single-deck build this two-story design extends
- [SparkFun serial LCD (16×2)](https://www.sparkfun.com/products/9395) — the serial LCD module type used here; single-wire interface, about $10
- [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — operating voltage, current draw, and echo timing
- [Robot wiring and power post](/blog/clean-up-arduino-robot-wiring-power) — the pre-sensor wiring cleanup that preceded this build
