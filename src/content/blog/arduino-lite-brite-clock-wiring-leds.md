---
title: 'Arduino Lite Brite Clock: Soldering Wires to 46 LEDs'
description: 'The unglamorous middle of the Lite Brite Clock build — soldering individual hookup wires to the cathode lead of every LED in the matrix, one at a time, with the trick that makes it not take all day.'
pubDate: 'July 29 2012'
youtubeId: '_HsJcCb3DoE'
heroImage: '../../assets/posts/arduino-lite-brite-clock-wiring-leds/thumbnail.jpg'
tags: ['arduino', 'led', 'soldering', 'lite-brite', 'clock', 'project']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the ongoing Arduino Lite Brite Clock build series. If you're jumping in here, start with the [concept and multiplexing post](/blog/arduino-lite-brite-clock-led-multiplexing) for the background on how the display works.

---

There's a category of build step that isn't exciting to describe or watch, but that you still have to get through. Soldering 46 individual hookup wires — one to the cathode lead of each LED in the Lite Brite Clock matrix — is that step. There's no clever trick that makes it fast. There is one technique that makes it not completely maddening.

## Why the cathodes get individual wires

In the multiplexed LED matrix design for this clock, each LED's cathode (negative lead) connects to a shared column line. The column line determines which column of LEDs is currently active. To make that work, each cathode needs its own wire run back toward the Arduino — at least until the wires are bundled at a common column connection point.

The anodes are handled differently: they'll be tied together per row on a piece of perfboard, with current-limiting resistors in line. That's covered in the next episode. This episode is just about getting the cathode wires onto the LEDs.

## The technique: hook first, then solder

The LED leads are short, and getting hookup wire to stay in contact with a tiny lead while you apply solder with your other hand is the thing that makes this tedious. The trick is simple: strip the end of the hookup wire, form a small hook in the bare conductor with pliers or your fingernail, and loop the hook around the LED lead before touching the iron to anything.

With the hook seated, the wire stays mechanically in position on its own. You can set it down, pick up the iron with one hand and solder with the other, and apply heat without the whole assembly shifting. The joint quality is also better because the physical contact between hook and lead is solid before solder flows in — the solder is filling a gap that's already closed rather than trying to hold two things together simultaneously.

Without the hook, you're either using a third hand (alligator-clip stand), recruiting a second person to hold the wire, or dealing with a string of cold joints and re-dos. With the hook, it's tedious but manageable.

## Keeping track of 46 wires

Forty-six wires is a lot of wires. Color-coding helps. Using different wire colors for different columns — or at minimum for different regions of the matrix — makes it significantly easier to sort them during the next phase when you're connecting everything to the anode resistor matrix and eventually to the Arduino.

Even if you can only source two or three wire colors, a consistent scheme (say, all column-1 wires red, all column-2 wires black, everything else white) will save you time and frustration at connection time. Label or group the bundles as you go rather than trying to sort them all at the end.

## Managing the process

This is a session where it helps to set up well before you start. Good lighting, a comfortable chair, your iron at the right temperature. The Lite Brite LEDs are already seated in the pegboard, which means you're working with a fixed grid rather than trying to hold individual LEDs. That's actually helpful — the pegboard acts as a jig.

Work systematically: complete all the LEDs in one row or column before moving to the next. Checking your work row-by-row is also easier than trying to audit a random set of joints scattered across the matrix.

Don't try to do all 46 in one sitting unless you're in the mood for it. The joints don't care if you take a break.

## Verifying before moving on

Before committing to the next phase, do a quick continuity check on a sample of joints with a multimeter set to continuity mode. Touch one probe to the wire and the other to the LED lead — you should get a beep (or near-zero resistance reading). A cold joint often looks acceptable visually but shows up immediately in a continuity test. Catching a bad joint now is much easier than tracking it down after the wiring matrix is complete and something doesn't light up.

## What's next

With cathode wires on all 46 LEDs, the next step is the perfboard work: cutting a piece of perf to size, positioning the 100Ω current-limiting resistors for the anode columns, and soldering the anode hookup wires. That's covered in the next post in the Lite Brite Clock series.

## References and further reading

- [Lite Brite Clock concept and LED multiplexing](/blog/arduino-lite-brite-clock-led-multiplexing) — series overview, why 46 LEDs, how multiplexing works
- [How to make a good solder joint — Adafruit](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — Adafruit's guide to clean joints, with photos of good vs. cold joints
- [Hookup wire guide — SparkFun](https://learn.sparkfun.com/tutorials/working-with-wire) — wire gauge, stripping, and tinning reference
