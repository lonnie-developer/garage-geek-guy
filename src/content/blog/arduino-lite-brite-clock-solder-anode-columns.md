---
title: 'Arduino Lite Brite Clock: Soldering the LED Anode Columns'
description: 'Tying all the anode leads in each column together with hookup wire, soldering them solid, testing for shorts — and the moment the whole bottom row lights up for the first time.'
pubDate: 'July 29 2012'
youtubeId: 'nFuAnm9MRcs'
heroImage: '../../assets/posts/arduino-lite-brite-clock-solder-anode-columns/thumbnail.jpg'
tags: ['arduino', 'led', 'soldering', 'lite-brite', 'clock', 'project', 'multiplexing']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [breadboard fail post](/blog/arduino-lite-brite-clock-breadboard-fail) explains why the connections moved to soldered perfboard. The [cathode wiring post](/blog/arduino-lite-brite-clock-wiring-leds) covers the individual LED cathode leads done in an earlier episode.

---

With cathode leads wired and the breadboard abandoned in favor of perfboard, this episode tackles the other side of the matrix: running hookup wire across each column of LED anodes and soldering them together into shared anode lines. It's the longest soldering session in the build, and the one where the proximity of anode and cathode leads makes short circuits the main hazard.

## The approach: twist, crimp, solder

The technique for connecting anode leads is to run a continuous piece of hookup wire across each column of LEDs, looping and crimping it around each LED's anode lead as it passes. The wire is not cut between LEDs in the same column — it continues from one LED to the next, picking up each anode in turn. Once the full run is laid across the column, every joint gets soldered.

Using needle-nose pliers to make a small loop in the wire at each LED's anode position before soldering does the same thing for anode joints that the hook trick does for cathode wire joints: it gives the wire mechanical stability on the lead before the iron touches anything. The iron just needs to heat the joint and introduce solder — it doesn't need to hold anything in place.

## The critical hazard: anode-cathode proximity

In the Lite Brite pegboard, each LED sits close to its neighbors. The anode and cathode leads of adjacent LEDs are only a millimeter or two apart — close enough that a blob of solder or a piece of wire that's slightly out of position can bridge them. A bridged anode and cathode is a short circuit.

In a multiplexed display, shorts are particularly insidious because the circuit is still partially functional — some LEDs light correctly, others don't, and the failure pattern doesn't point obviously to a wiring error. A short between an anode column and a cathode row means that whenever either of those lines is driven, both may activate. You'll see LEDs lighting in positions that shouldn't be lit — ghost pixels in the display.

The right approach is to visually check every joint immediately after soldering it, before moving on. Look at the joint itself but also at the surrounding leads. Solder bridges are easier to catch and fix as you go than to diagnose after the matrix is complete.

## Finding the shorts

Two short circuits showed up during the initial test of this build — found by lighting the bottom row with alligator clips from a 5V supply and a resistor, then looking for LEDs that lit in unexpected positions or checking with a multimeter.

The test procedure: connect 5V through the current-limiting resistor to the row's common anode wire, and pull each cathode column low in turn. The LED at that row/column intersection should light; no others should. Any LED that lights outside the expected pattern, or any two adjacent LEDs that both light when only one column is pulled low, suggests a short.

Fixing a solder bridge on a joint this size is usually a matter of touching the iron to the affected area briefly with a bit of fresh solder (the flux helps), then using solder wick or a solder sucker to pull the excess. The key is isolating exactly which joint is bridged before applying heat — adding heat without knowing where you're going can make the bridge flow further rather than removing it.

Both shorts in this build were found and fixed before closing the housing. After the fixes, the bottom row test came back clean: every LED lit on command, none ghosted, all in the right positions. That's the milestone that ends this phase of the build.

## The Arduino connections, previewed

Once all anode columns are wired and tested, what's left is connecting the matrix to the Arduino. The five common anode row wires connect to Arduino output pins (through the 100Ω resistors already on the perfboard). The ten cathode column wires connect to ten more Arduino pins. The two colon LEDs can tie directly to 5V through a resistor — they're always on.

That gives fifteen Arduino I/O pins consumed by the display, leaving three spare beyond the two time-setting buttons, within the Uno's full 20-pin budget as calculated at the start of the series.

## What's next

With the matrix complete and tested, the build moves into final assembly — fitting the LED matrix into the Lite Brite housing, connecting the Arduino, dealing with a battery polarity surprise, and verifying the whole thing works before closing the lid. That's the [closing-up episode](/blog/arduino-lite-brite-clock-closing-up).

## References and further reading

- [Lite Brite Clock — multiplexing concept](/blog/arduino-lite-brite-clock-led-multiplexing) — the full pin count and column/row scheme
- [How to remove solder bridges — Adafruit](https://learn.adafruit.com/adafruit-guide-excellent-soldering/common-problems) — solder wick technique and common joint problems
- [Testing for continuity with a multimeter — SparkFun](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter/continuity) — the fastest way to find unexpected shorts
