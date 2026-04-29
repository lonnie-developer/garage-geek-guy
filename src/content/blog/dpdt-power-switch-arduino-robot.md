---
title: 'Wiring a DPDT Power Switch to an Arduino Robot — One Switch for Two Batteries'
description: 'A double-pole double-throw toggle switch lets a single big red button power both the Arduino battery and the motor battery at the same time. Here is the wiring, the multimeter checks, the soldering, and the one moment where something disconnected and smoked.'
pubDate: 'October 11 2012'
youtubeId: 'Mt3J9HCa34A'
heroImage: '../../assets/posts/dpdt-power-switch-arduino-robot/thumbnail.jpg'
tags: ['arduino', 'robotics', 'wiring', 'electronics', 'robot-build', 'tutorial']
---

Most Arduino robot builds start with two separate power sources: one battery for the Arduino itself (typically a 9V that feeds the Vin pin or barrel jack) and a separate battery pack for the motors (usually a 4×AA or 6×AA pack wired directly to the motor driver). This is the right approach — motors draw enough current that running them from the same supply as the Arduino causes brownouts and resets. But it creates an obvious annoyance: you need to disconnect two batteries every time you want to power the robot down, and reconnect two batteries every time you want it up.

A DPDT switch solves this cleanly. A double-pole double-throw toggle has two electrically independent switching sections in a single throw — flip it one way, both circuits open; flip it the other, both circuits close. One switch, one motion, both batteries connected. It's one of those wiring improvements that feels obvious in retrospect.

This post covers the full process of adding one to a robot chassis: mounting it, testing with a multimeter, soldering wires to the terminals, dealing with stranded wire, providing strain relief, and one incident near the end where a disconnected wire produced a small puff of smoke before everything worked.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## Understanding the DPDT switch

A single-pole single-throw (SPST) switch is the basic on/off — one circuit, two positions. A double-pole single-throw (DPST) adds a second independent circuit that switches at the same time. That's all a DPDT actually needs to be for this application — the "double throw" part (which adds two separate "on" positions) isn't used here, but DPDT switches are what's commonly available in hobby parts boxes.

The switch has six terminals arranged in two rows of three. Each row is one "pole" — one independent circuit. Within each row, the center terminal is the common (one wire of the circuit), and the two outer terminals are the two "throw" positions. For a simple on/off application, you wire to the center and one outer terminal of each row.

Before wiring anything, use a multimeter in continuity mode to verify which terminals connect to which in each switch position. A DPDT salvaged from a parts box might have different terminal layouts than you expect — flip it one way, probe the pairs, flip it the other way, probe again. This five-minute check saves a lot of debugging later.

## Mounting

The switch goes in an accessible spot on the chassis — visible, reachable, and positioned so it won't accidentally flip during a robot collision. A round toggle switch needs a hole drilled or punched to its diameter; a flat toggle can mount with screws through the panel.

Punching the hole freehand works if you have a screwdriver shaft close to the right diameter to use as a drift punch and a hammer. The result won't win any precision awards, but it holds the switch securely. Getting it perfectly centered matters less than getting it in a position where you can reach it without turning the robot over.

## Working with stranded wire

The wiring here is stranded wire salvaged from old computers — perfectly functional, free, but more annoying to work with than solid-core hookup wire. Stranded wire frays at cut ends, individual strands wander out and can bridge to adjacent terminals, and it doesn't hold solder the same way solid wire does.

The solutions: twist the end of the stranded wire tight before soldering (this holds the individual strands together), add a small touch of solder to the twisted end before the actual joint (this "tins" the end and makes it behave more like solid wire), and work in one smooth motion — get the joint hot, flow the solder, and let it cool without disturbing it. Stranded wire can look soldered when it's actually just clamped cold around a terminal; tug each wire gently after it cools to verify it won't pull free.

If you're building a robot that will see real use, solid-core hookup wire makes this whole section easier. Old computer power supplies are a better source than ribbon cables for this — the internal power wires are thicker gauge and insulated in proper red and black.

## The strain relief argument

A wire that terminates at a switch terminal and can be pulled freely in any direction will eventually pull loose, especially on a robot that gets handled, crashes into walls, and gets opened and closed to swap batteries. Strain relief — whether it's tape, a zip tie looped around the chassis before the connection, or a proper cable clamp — takes the mechanical load off the solder joint and transfers it to the chassis.

The approach here uses a combination of tape to position the wires and zip ties looped through chassis holes to anchor them. The wires can't be pulled directly outward from the terminal because the zip tie catches the load a centimeter back from the joint. It's not elegant, but it holds.

The same principle applies to any wired connection in a robot that moves. When you close the chassis and carry it to the table, every wire in there gets jostled. The ones without strain relief are the ones that fail.

## Mounting the 9V battery pack

The 9V snap connector and battery pack get foam-mounted on the interior chassis wall — a piece of foam cut to roughly the footprint of the battery, glued to the chassis, with the battery sitting against it. This keeps the battery from rattling around and prevents it from shorting against any metal chassis hardware.

The right foam thickness takes a moment to find: too thick and the pack doesn't seat against the chassis wall, too thin and it doesn't cushion anything. Splitting a foam piece in half lengthwise with a knife gets you to the right thickness faster than searching for a thinner piece.

## The smoke moment

Toward the end of this build, a puff of smoke appeared during a power-up test. This sounds alarming and it's worth describing: a wire from the 9V pack had a loose solder joint that pulled slightly free when the chassis was closed. The exposed conductor touched something it shouldn't have for a moment, causing a brief spark and the smoke puff, then nothing further.

The lesson here is: when you see smoke, don't immediately assume the worst. Follow the wires. Find what got hot. In this case, the fix was reattaching one wire end and confirming the joint held. The Arduino was undamaged.

More broadly: solder connections to switch terminals in a bench-controlled environment, not in the chassis. Getting a good joint on a switch that's already mounted and constrained by wires going in three directions is harder than soldering on the bench and then installing. The quality of bench-soldered joints is reliably better.

## First power-up

With the switch wired, one throw-position connects both battery circuits, the other leaves both open. Flipping to "on": the Arduino powers up (the green power LED lights), and the motor driver is live and ready for commands.

The convenience is real. Opening the chassis, pressing one toggle, and having everything dead is a significant quality-of-life improvement over pulling two connectors. When you're in the middle of debugging and you want to cycle power quickly, this is the workflow.

## What you'll need

- DPDT toggle switch (salvaged or ~$3 new; size to match whatever fits your chassis aesthetically)
- 22–24 AWG hookup wire in two colors (red/black or equivalent — the color coding matters for later debugging)
- Soldering iron and solder — a temperature-controlled iron like the Hakko FX-888 makes the small-terminal soldering much more manageable
- Multimeter for switch verification before wiring
- Drill or punch to fit the switch mounting hole
- Zip ties and tape for strain relief
- Small foam piece for battery cushioning

## References and further reading

- [DPDT switch wiring guide](https://en.wikipedia.org/wiki/Switch#Contact_mechanism) — Wikipedia's switch contact mechanism section; the pole/throw nomenclature is explained clearly here
- [Arduino power input specifications](https://docs.arduino.cc/hardware/uno-rev3/) — Uno's Vin pin and barrel jack input voltage range; relevant when wiring in an external switch on the power path
- [Stranded vs. solid-core wire](https://www.allaboutcircuits.com/technical-articles/understanding-wire-gauge-and-stranded-vs-solid-wire/) — All About Circuits article on the mechanical and electrical tradeoffs of each
- [Solder joint quality guide](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — Adafruit's guide to soldering; the "cold joint" section is particularly relevant to switch terminal work
- [Hakko FX-888D temperature-controlled soldering station](https://www.hakko.com/english/products/hakko_fx888d.html) — the station referenced in the video; a reliable long-term bench iron
- [Strain relief techniques for hobby projects](https://www.sparkfun.com/tutorials/220) — SparkFun tutorial on wire strain relief methods
