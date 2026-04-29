---
title: 'Arduino Lite Brite Clock: Closing It Up (and a Battery Polarity Surprise)'
description: 'Fitting the completed LED matrix into the Lite Brite housing, connecting the Arduino, discovering the battery connector is backwards, fixing it, and watching the clock finally run on battery power.'
pubDate: 'July 30 2012'
youtubeId: 'nvuK3KnvaXo'
heroImage: '../../assets/posts/arduino-lite-brite-clock-closing-up/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'assembly']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [anode columns post](/blog/arduino-lite-brite-clock-solder-anode-columns) covers the last major soldering phase. If you're following from the start, the [concept post](/blog/arduino-lite-brite-clock-led-multiplexing) has the series overview.

---

The soldering is done. The shorts are fixed. All 46 LEDs are wired into the multiplexed matrix, anode and cathode wiring complete, and a row test confirmed everything lights correctly. This episode is about closing the Lite Brite housing and doing the first battery-powered run — which doesn't go quite right on the first attempt.

## Fitting everything into the housing

The Lite Brite is not a large enclosure. Getting the LED matrix, the Arduino, the perfboard resistor assembly, the battery pack, and eventual time-setting buttons to all coexist inside it requires some spatial negotiation. The Arduino Uno in particular is large for this application — and this is the episode where the plan to eventually switch to an Arduino Nano gets explicitly called out.

The Nano runs the same ATmega328P as the Uno, accepts the same sketches, and fits in a fraction of the space. For a completed project that's going to live in a housing permanently, the Nano is almost always the right choice where an Uno was used for development. The approach used here — develop and test with the Uno, switch to a Nano for final assembly — is a reasonable workflow. The sketch transfers without modification.

For the initial test, the Uno stays in because that's what's currently programmed. The Nano swap comes when the buttons go in, which is the remaining item on the build list.

## Testing on battery vs. USB

Up to this point the clock has only run with the Arduino connected to a computer via USB. The USB connection supplies 5V directly to the Arduino's 5V rail, bypassing the onboard voltage regulator. A 9V battery going through the Arduino's barrel jack passes through the regulator first, which drops it to 5V before anything sees it. In practice, the regulated output and the USB rail are the same voltage, and the display code and LEDs don't know the difference.

The exception is if the battery is partially discharged. A 9V battery below about 7V may not give the regulator enough headroom to maintain a stable 5V output. If the display starts flickering or behaving erratically on battery power after working fine on USB, the battery is the first thing to check.

## The polarity surprise

On the first battery-powered test: nothing. The Arduino doesn't light up, the LEDs don't light, nothing happens.

The diagnosis: the barrel connector wired to the battery holder was installed with reversed polarity. The Arduino's barrel jack expects center-positive — the inner pin is positive, the outer ring is negative. The makeshift battery connector had it backwards. The Arduino has a protection diode for exactly this situation, so no damage occurred — but it also means no power gets through until the polarity is corrected.

Reversing the polarity is a matter of rewiring the connector or physically flipping the wires in the barrel plug. Once corrected: the Arduino powers on, the sketch runs, and the LED matrix lights up for the first time on battery power. The clock works.

## What still needs to happen

Closing the housing in this episode is a "close it for now" rather than a final closure — two items remain on the punch list:

**The time-setting buttons.** Two momentary push buttons need to be drilled into the housing and wired to the Arduino with pull-up resistors. Without them, the time is set in code and the clock can't be adjusted without a computer. The buttons are the difference between a demo and a usable clock.

**The Arduino Nano swap.** Replacing the Uno with a Nano frees up significant space inside the housing, makes routing the wiring more manageable, and is the right choice for a permanently installed project.

Both of those get done in a later session once the housing is reopened for button installation.

## The build at this point

The Lite Brite Clock is functional: a working multiplexed LED clock display, running on a 9V battery, inside a Lite Brite housing. The build went from a "the pegs are the same diameter as LEDs" observation to a working clock over the course of a series of sessions across the summer of 2012 — 46 LEDs, about 60 solder joints, two short circuits found and fixed, one breadboard abandoned in favor of perfboard, and one reversed battery connector. Not a bad result.

The [full series index is on this blog](/blog) — search for "Lite Brite Clock" to see all the episodes.
