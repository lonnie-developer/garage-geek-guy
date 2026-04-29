---
title: 'Arduino Lite Brite Clock: Parts List and What Everything Is For'
description: 'Everything you need to build the Arduino Lite Brite Clock — 46 LEDs, two flavors of resistors, a Lite Brite, a push button pair, and the tools to put it all together.'
pubDate: 'July 26 2012'
youtubeId: '5M8CppUg8js'
heroImage: '../../assets/posts/arduino-lite-brite-clock-parts/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'parts-list']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [concept and multiplexing post](/blog/arduino-lite-brite-clock-led-multiplexing) covers why the build works the way it does — start there if you haven't.

---

Before any soldering gets done, it helps to have everything on the table. This post covers the complete parts list for the Lite Brite Clock, what each part is for, and a few sourcing notes.

## The display

**The Lite Brite toy** is the centerpiece. Any standard Lite Brite with a pegboard panel works — the holes are sized for 5mm LEDs, which happen to fit snugly without modification. An older, used Lite Brite is fine. The one in this build belonged to a daughter who outgrew it. If you're buying one specifically for this project, the original Hasbro version is widely available used for a few dollars. You'll also want the black paper that goes behind the pegboard — it provides the dark background that makes the LED display readable.

**46 5mm LEDs** in the color of your choice. The build uses green. Clear (water-clear) 5mm LEDs are fine and cheap, but they have a narrow viewing angle and can spill light into adjacent holes when they're this close together. Diffused LEDs (the kind with a frosted plastic body) fix this at the source and can be bought that way. If you have clear LEDs, sanding the outside lightly with 320-grit sandpaper diffuses them adequately — more on that in a later episode. Either way, 5mm diameter is the spec that matters for fitting the Lite Brite holes.

## The resistors

Two types of resistors are in this build, for two different jobs.

**~14 × 100Ω resistors (¼ watt, through-hole)** are the current-limiting resistors on the anode side of the LED matrix. Every column of anodes in the multiplexed display shares one resistor. The 100Ω value limits current through each lit LED to a safe level given the 5V supply and typical 2V forward voltage of green LEDs. Quarter-watt through-hole is the form factor — the small cylindrical resistors with color-coded bands that drop into a breadboard or perfboard. They cost almost nothing in any quantity.

**2 × 2.2kΩ resistors (¼ watt, through-hole)** are pull-up resistors for the two time-setting buttons. When a push button isn't pressed, the pull-up resistor holds the Arduino input pin at a known logic level (HIGH) rather than letting it float. When the button is pressed, it pulls the line LOW, which the Arduino reads as a button press. The exact resistance may need adjustment — 2.2kΩ is the starting value, and if the buttons prove unreliable it's the first thing to change.

## The microcontroller

**Arduino Uno** (or equivalent). The Mega also works and is used in this video because the Uno was tied up in another project at the time. For this build you don't need the Mega's extra pins — the Uno's 14 digital plus 6 analog pins are sufficient, and the Nano is an even better fit for the final version (more on that when we close up the housing). Any ATmega328P-based board will handle the display, buttons, and timekeeping with room to spare.

## The buttons

**2 × momentary push buttons** — the kind that spring back when you release them, not toggle switches. One button increments the hours, one increments the minutes. Momentary buttons are available from any electronics supplier; the small 6mm tactile push buttons common in Arduino kits are exactly right.

## Power

**9V battery and holder with a barrel connector** wired to plug into the Arduino's power jack. The Arduino's onboard voltage regulator brings 9V down to 5V for the board and the LED matrix. You could also use 4× AA batteries (6V), which gives less headroom but still works. USB power from a computer is fine for development and testing — the 5V USB rail powers the Arduino directly without the regulator.

## Wire and tools

- **22 AWG hookup wire** — used for the anode column connections. One note from experience: 22 gauge solid-core is a bit on the thin side for breadboard sockets, which are sized for 20–22 AWG. The wires can sit loosely and intermittently lose contact. The solution is to move connections off the breadboard onto perfboard with soldered joints, which is exactly what the next episode does.
- **Soldering iron** — any iron that holds temperature works, though one with a temperature indicator (or an adjustable station) makes life noticeably easier.
- **Helping hands** — the third-hand tool with two alligator clips and a magnifying glass. Genuinely useful for holding LED leads in position while soldering.
- **Wire strippers, needle-nose pliers, flush cutters**
- **Solder** — rosin-core 60/40 or 63/37, thin gauge

## The full list at a glance

| Item | Qty | Notes |
|------|-----|-------|
| 5mm LEDs | 46 | Diffused or clear (sand if clear) |
| 100Ω ¼W resistor | ~14 | Anode current limiting |
| 2.2kΩ ¼W resistor | 2 | Button pull-ups |
| Arduino Uno (or Nano) | 1 | ATmega328P-based |
| Momentary push button | 2 | 6mm tactile type |
| 9V battery + holder | 1 | Barrel connector for Arduino |
| 22 AWG hookup wire | 1 spool | Various colors helpful |
| Lite Brite toy | 1 | With black paper |
| 320-grit sandpaper | 1 sheet | For diffusing LEDs if needed |
| Soldering iron | 1 | Temperature-adjustable preferred |
| Helping hands | 1 | Highly recommended |

## What's next

With parts in hand, the next steps are fitting the LEDs into the Lite Brite grid, testing each one before committing to solder, and then working through the cathode and anode wiring. The [next episode](/blog/arduino-lite-brite-clock-testing-leds) covers an important pre-installation test — and demonstrates very clearly why you always use a current-limiting resistor.
