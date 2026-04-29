---
title: 'Arduino Lite Brite Clock: Inserting 46 LEDs Into the Pegboard (Front-Load Only)'
description: 'Forty-six LEDs, one at a time — why the Lite Brite pegboard only accepts LEDs from the front, how to keep polarity straight across the whole grid, and the family workshop session where it all gets done.'
pubDate: 'July 27 2012'
youtubeId: 'wxuGRmdnCpc'
heroImage: '../../assets/posts/arduino-lite-brite-clock-positioning-leds/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'assembly']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [testing LEDs post](/blog/arduino-lite-brite-clock-testing-leds) covers individual LED validation before any permanent work begins. The [series overview and multiplexing concept](/blog/arduino-lite-brite-clock-led-multiplexing) has the full pin count and grid layout.

---

With 46 LEDs individually tested, polarity confirmed, and domes sanded for diffusion, it's time to actually put them in the board. This is where the build transitions from prep work to visible progress — and where the first plan runs into a small mechanical reality.

## The front-loading problem

The assumption going in was that LEDs could be inserted from the back of the Lite Brite pegboard — push each LED through from behind, let the dome emerge on the front face, bend the leads down, move on. It would have been cleaner: the back stays orderly while you work and you don't risk disturbing installed LEDs while reaching across the board.

The Lite Brite pegboard didn't cooperate. The holes taper slightly — wider on the front face where the translucent pegs are meant to sit, narrower toward the back. A 5mm LED body fits snugly through the front. It doesn't pass through from the back at all.

So the loading method is front-first: press each LED into its hole from the front side of the board, let the leads poke through to the back, then bend the leads outward to hold the LED in place while you work. The mechanical hold isn't much — bent leads against plastic — but it's enough to keep everything positioned while you work through the full grid before any soldering happens.

## Keeping polarity straight across 46 LEDs

A 5mm LED in a Lite Brite hole can rotate. Once inserted, there's no visual indicator on the dome that tells you which lead is which. The only reliable way to maintain consistent polarity across the entire grid is to establish a rule before the first LED goes in and follow it mechanically for every subsequent one.

The approach: the short lead is always the cathode. That's standard for through-hole LEDs — the shorter lead is the cathode, the longer is the anode. Before inserting each LED, bend the leads slightly to identify which is which, orient the LED so the short lead will come out on a consistent side (or in a consistent direction relative to the row), then push it in.

This matters enormously for a multiplexed display. In the matrix scheme for this clock, the cathode leads in each row are tied together and the anode leads in each column are tied together. A single reversed LED in the middle of the grid won't just fail to light — it creates a path that can affect adjacent cells in ways that are genuinely confusing to debug after the fact. Consistent orientation from the start is cheaper than any amount of reverse-engineering later.

## The time-lapse session

Inserting 46 LEDs by hand is methodical work. Punch each hole with the LED body, confirm it's seated, bend both leads out on the back to lock it, move to the next position. The video covers the setup and first few rows in real time, then cuts to time-lapse for the bulk of the work.

A few things worth noting from the live portions:

The board has more holes than the clock needs. The Lite Brite pegboard is a fixed grid; the clock display — two four-digit groups with a colon between them — doesn't fill every available position. A handful of extra holes got punched accidentally during the process. Those get plugged later; for now they're left empty and noted for cleanup.

The first row of five LEDs goes in, leads bent out, and the pattern is established. From there it's repetition — the cognitive load is low once the polarity convention is locked in, and the main job is just not losing count of which position you're on.

## What the display looks like at this stage

At the end of the LED insertion session, the front face of the Lite Brite shows 46 LED domes in their grid positions, lightly frosted from sanding, sitting flush in the holes. The back of the board is a field of bent wire leads, no connections yet — just potential. The colon position has two LEDs that aren't part of the multiplexed matrix; they'll get wired directly to 5V through a resistor since they're always on.

The next step is the actual soldering — connecting all the cathode leads in each row into common lines, which is where the real wiring work begins.

## What's next

With LEDs positioned and leads bent, the build moves to wiring the cathode rows — and an early encounter with the limits of breadboard connections. The [breadboard fail post](/blog/arduino-lite-brite-clock-breadboard-fail) covers why 22-gauge wire and cheap breadboard sockets don't mix, and why the connections ended up on soldered perfboard instead.
