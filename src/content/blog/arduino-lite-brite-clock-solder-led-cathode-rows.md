---
title: 'Arduino Lite Brite Clock — Soldering the LED Cathode Rows'
description: 'How to solder the cathode rows of a hand-wired 5×12 LED matrix for the Arduino Lite Brite Clock. Covers matrix layout, hookup-wire loop technique, and what to watch for in dense hand-wiring.'
pubDate: 'July 29 2012'
youtubeId: '5H2KpBWMyUk'
heroImage: '../../assets/posts/arduino-lite-brite-clock-solder-led-cathode-rows/thumbnail.jpg'
tags: ['arduino', 'leds', 'soldering', 'led-matrix', 'lite-brite-clock', 'tutorial']
---

*Part of the Arduino Lite Brite Clock build series — a hand-wired LED matrix clock that was later featured in Make Magazine. This episode covers soldering the cathode rows of the matrix.*

Most Arduino LED matrix projects reach for a MAX7219 driver chip or a pre-built module and skip the hand-wiring entirely. There's nothing wrong with that approach — those chips are inexpensive and handle multiplexing cleanly — but they also abstract away the part that makes you understand what's actually happening electrically. Building the matrix by hand, lead by lead, is slower. It's also the kind of work that makes you genuinely understand row-column addressing in a way that importing a library never quite does.

The Lite Brite Clock is a 5×12 LED matrix driven directly from Arduino digital I/O pins — no driver IC, no shift registers, just Arduino pins, resistors, and wire. This episode covers the first structural step: soldering all the cathode leads together horizontally across each row.

## Understanding the matrix layout

The clock face shows four digits and a colon, arranged to look like a digital display. The matrix is laid out as 5 rows by 12 columns: 10 columns for the digit anodes (two digits per side, five columns each, using seven-segment-style patterns rotated for the LED arrangement), plus 2 additional columns for the two colon LED positions.

In a multiplexed matrix, the cathodes are shared across a row. That's what "row" means electrically: all the LEDs in the same row have their cathodes tied together, so pulling that row's common cathode low activates the path for that entire row. Which LEDs actually light up depends on which column anodes are also driven — that's the column side's job, handled in a separate step.

The scanning works like this: the Arduino activates one row at a time, cycling through all five rows fast enough that persistence of vision makes the display look solid. At 100 Hz refresh rate and 5 rows, each row gets activated every 2ms and stays active for about 200µs. The eye sees a continuous display; the Arduino sees a very tight loop.

## The hookup-wire loop technique

The cathode rows are connected using a length of solid-core hookup wire stripped along its length. Rather than cutting individual jumper segments between each LED, you strip a continuous piece of wire to the appropriate length — leaving insulation only at the ends where it leaves the matrix — and make a small loop or crimp at each LED position.

The technique in detail:

Strip the entire active length of wire down to bare conductor. Lay it alongside the row of LEDs with the wire running horizontally past each cathode lead. At each cathode, bend a small loop in the wire around the lead using needle-nose pliers, then tighten it snug. Once all five cathodes in the row are looped, go back and solder each joint. The loop creates good mechanical contact before solder flows, which gives you clean joints even if your soldering is rushed.

The same approach gets used later for the anode columns — same technique, rotated 90 degrees.

## What the five rows represent

The 5-row layout maps to the horizontal segments of the seven-segment-style display. The top segment, upper-left and upper-right segments, lower-left and lower-right segments, and bottom segment of each digit each occupy one row position. The colon dots also need to be addressable per-row, so they participate in the same row structure even though they're separate columns.

From a wiring standpoint, each row needs one Arduino output pin. Five rows, five pins. The Arduino sinks current from those row pins — they're driven LOW when active, with the row's common cathode pulled to ground. The column drivers supply current through resistors; they're driven HIGH when the LED in that position should be on.

## The density problem and why it matters

At the density of a 5×12 matrix — 60 LEDs in a relatively small footprint — anode and cathode leads end up sitting very close together. A solder bridge between an anode and cathode lead in the middle of the matrix is genuinely hard to find and fix after the fact. The joints are deep in a thicket of wire.

The advice from building this: take your time at each joint. Before soldering any row, verify that the looped wire touches only the cathode leads, not any anode leads nearby. A visual check with a bright light from multiple angles catches most potential bridges before they happen.

After the row is soldered, test it with a continuity meter: probe from one end of the row to the other and verify all five cathodes are connected. Then probe from the row wire to each anode lead and verify there's no continuity — no shorts. Five minutes of continuity checking now saves hours of fault-finding later.

## Build sequence for this series

The full matrix construction follows this order:

1. Diffuse all LEDs by sanding the domes (see [previous episode](/blog/arduino-lite-brite-clock-diffuse-leds))
2. Solder cathode rows — tie cathodes together horizontally **(this episode)**
3. Solder anode columns — tie anode leads together vertically
4. Build the resistor perfboard — 100Ω current-limiting resistors between each column pin and the Arduino
5. Wire the colon segment
6. Connect the Arduino's digital I/O pins to the matrix

The reason cathodes come first is mechanical: the cathode leads are shorter and sit lower in the assembly. Soldering them first while the leads are accessible is easier than trying to work around the anode column wires later.

## The broader why: why hand-wire rather than use a MAX7219?

Using a MAX7219 or similar LED driver IC would make this build faster, use fewer Arduino pins (SPI interface reduces to 3 pins for any size matrix), and handle current limiting internally. So why not?

A few reasons. First, cost and parts availability in 2012 — getting a MAX7219 required either ordering online with shipping time or paying a premium at a local electronics shop. A roll of hookup wire and a bag of resistors were already in the parts drawer.

Second, this is the Lite Brite Clock — a project named after a toy that's all about individual light elements arranged in a grid. Building the matrix by hand, lead by lead, is in keeping with the spirit of the project. You end up with something hand-made in the literal sense.

Third, there's genuine educational value in understanding the raw multiplexing — what rows and columns mean electrically, why the resistors go where they do, what determines scan rate. Once you've hand-wired a matrix, LED driver chips become much more legible because you understand what they're automating.

## References and further reading

- [How does LED matrix work? | Mika Tuupola](https://www.appelsiini.net/2011/how-does-led-matrix-work/) — excellent visual explainer of row-column scanning and multiplexing
- [Row-column scanning tutorial | Arduino Project Hub](https://projecthub.arduino.cc/Heathen_Hacks-v2/9233cef5-1a3c-4535-ba90-ab616a67caa8) — hands-on example with code
- [MAX7219 LED driver datasheet | Maxim](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7219-MAX7221.pdf) — good for understanding what a dedicated driver handles so you appreciate the hand-wiring alternative
- [Multiplexing LEDs with Arduino | Adafruit](https://learn.adafruit.com/adafruit-arduino-lesson-3-rgb-leds) — Adafruit's take on LED control fundamentals
- [Next: soldering the colon segment](/blog/arduino-lite-brite-clock-colon-segment) — the next episode in the Lite Brite Clock build
