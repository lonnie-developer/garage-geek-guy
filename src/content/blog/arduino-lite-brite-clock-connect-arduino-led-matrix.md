---
title: 'Arduino Lite Brite Clock — Connecting the Arduino to the LED Matrix'
description: 'Wiring the Arduino Uno digital I/O pins to a hand-built 5×12 LED matrix clock. Covers pin assignment, the 100Ω resistor perfboard, current budgeting, and the final physical assembly step before software.'
pubDate: 'July 30 2012'
youtubeId: 'T2Dmp-ae-cI'
heroImage: '../../assets/posts/arduino-lite-brite-clock-connect-arduino-led-matrix/thumbnail.jpg'
tags: ['arduino', 'leds', 'led-matrix', 'lite-brite-clock', 'tutorial', 'wiring']
---

*Part of the Arduino Lite Brite Clock build series — a hand-wired LED matrix clock later featured in Make Magazine. This is the final physical assembly step: wiring the Arduino Uno to the completed matrix.*

Everything before this point in the build has been matrix construction — diffusing LEDs, soldering cathode rows and anode columns into a 5×12 grid, adding the colon segment. The matrix is a finished physical object at this point. But it's also completely inert: a grid of LEDs with no path for current to flow, waiting for something to drive it.

This episode is where the Arduino enters the picture. Twelve column pins and five row pins get connected to the Arduino's digital I/O, with a perfboard carrying 100-ohm current-limiting resistors sitting in between on the column side. After this, the hardware is done and the build moves into software.

## Pin count reality check

The 5×12 matrix needs 17 digital I/O pins: 12 for columns, 5 for rows. The Arduino Uno has 14 digital pins (D0–D13) plus 6 analog pins (A0–A5) that can function as digital I/O with `pinMode()`. That's 20 total usable I/O pins, which just barely covers the 17-pin requirement with three to spare — enough for a serial connection for debugging (D0 and D1) and an indicator LED if you want one.

The layout typically assigns the analog pins to either the row drivers or the lower-frequency column drivers, keeping PWM-capable digital pins available if you want brightness control down the road. For a basic clock with no dimming, pin assignment is more about routing convenience than electrical requirements.

## The resistor perfboard

The 12 column pins each go through a 100Ω resistor before reaching the matrix anode columns. Rather than placing individual resistors inline in point-to-point wiring (which gets tangled fast), the build uses a small perfboard with 12 resistors in a row — one per column — with a header on one side connecting to the Arduino column pins and bare wire leads on the other side going to the matrix.

The resistor math: with the Arduino's 5V supply and typical red/green LEDs with a forward voltage around 2V, the resistor limits current to (5 − 2) / 100 = 30mA per LED. That's within the LED's rated range (typically 20–30mA for standard 5mm LEDs) and close to the Arduino Uno's 40mA absolute maximum per I/O pin. It works, but it's running closer to the limit than ideal.

A 220Ω resistor would give you a safer 13.6mA per LED with acceptable brightness — still plenty visible for a bedside clock. If you're rebuilding this and want more comfortable margins, bump the resistors to 220Ω.

## The current budgeting problem

Here's the constraint that doesn't show up in simple wiring diagrams: the Arduino Uno's ATmega328P has a 200mA maximum current limit for the entire chip, and a 40mA limit per individual I/O pin. During any given scan window, you're driving one row (sinking current through the row cathode pin) and some subset of the 12 column anode pins simultaneously.

In the worst case — all 12 column LEDs active simultaneously — you have 12 × 30mA = 360mA flowing into the row pin. That's nearly 10 times the pin's rated limit, which would cook the ATmega instantly. The reason this doesn't happen is that the LEDs themselves aren't all on at once: the column pins supply current through their own 100Ω resistors, each capped at 30mA. The row pin just sinks the sum of whatever columns are actually driven in that scan window.

The practical solution is two-fold: first, use `digitalWrite()` for the row pins and keep scan windows short (200µs or less per row at 100Hz refresh). Second, if you're lighting many LEDs simultaneously, consider buffering the row pins through NPN transistors (2N2222 or similar) to offload the current sinking from the Arduino pin to the transistor's collector. This build drives the matrix directly from Arduino pins, which works fine for a clock where no more than 7 segments are ever lit simultaneously in any digit column, but a transistor buffer is the robust solution for higher-current configurations.

## Wiring it up

The column connections run from the Arduino digital pins (or analog pins in digital mode) through the resistor perfboard to the anode column wires on the matrix. The row connections run directly from Arduino pins to the cathode row wires — no resistors on the row side, since the row pins are sinking, not sourcing.

The physical routing matters: keep the column wires organized so you know which Arduino pin drives which matrix column. Label the wires with tape flags before you solder, or map them out on paper first. Debugging crossed column connections in a software display driver is tedious; getting the wiring organized once and checking it against your schematic is faster.

## What comes next

With the Arduino wired to the matrix, the hardware is complete. The next phase is the display driver software: a tight loop that scans each of the five rows in sequence, setting the appropriate column pins high based on what character or segment should be displayed in that row scan. On top of that goes the timekeeping logic — tracking hours, minutes, and seconds, converting them to the segment patterns the display driver needs.

For timekeeping, the options in 2012 were a software counter using `millis()` (simple, drifts over time), a DS1307 RTC module (accurate, requires I2C and two more pins), or the Arduino's internal Timer1 for more precise software timing. A software clock with occasional drift is fine for a demo build; a DS1307 is the right answer for something that's supposed to stay accurate for months on a shelf.

## The build is a Make Magazine project

It's worth noting here: this Lite Brite Clock build was later featured in Make Magazine. The hand-wiring approach — 60 LEDs individually soldered into a matrix with no driver ICs — is the kind of labor-intensive craftsmanship that Make Magazine appreciated. The clock works because the fundamentals are right: correct resistor values, sensible pin assignment, clean solder joints, and multiplexing logic that keeps the scan rate fast enough to fool the eye.

## Build series navigation

1. [Diffuse the LEDs](/blog/arduino-lite-brite-clock-diffuse-leds)
2. [Solder cathode rows](/blog/arduino-lite-brite-clock-solder-led-cathode-rows)
3. [Wire the colon segment](/blog/arduino-lite-brite-clock-colon-segment)
4. Connect the Arduino to the matrix **(this episode)**

## References and further reading

- [ATmega328P datasheet | Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf) — I/O pin current limits on page 312
- [Arduino current limitations | Arduino Forum](https://forum.arduino.cc/t/how-much-current-can-i-take-from-the-arduinos-pins/35823) — community discussion of per-pin and total chip current limits
- [How LED matrix multiplexing works | Mika Tuupola](https://www.appelsiini.net/2011/how-does-led-matrix-work/) — visual explainer of the scanning approach the display driver implements
- [DS1307 real-time clock breakout | Adafruit](https://learn.adafruit.com/ds1307-real-time-clock-breakout-board-kit/overview) — the RTC option if you want the clock to stay accurate for months
- [BlinkWithoutDelay | Arduino documentation](https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/) — the millis()-based timing pattern used in the display scan loop
