---
title: 'Arduino Lite Brite Clock: The Concept and How to Multiplex 46 LEDs on 15 Pins'
description: 'The engineering brainstorm behind the Lite Brite Clock — how a Lite Brite toy becomes the chassis for a 7-segment-style LED clock, and why multiplexing makes 46 LEDs possible with just 15 Arduino I/O pins.'
pubDate: 'July 26 2012'
youtubeId: 'YOf32PWByS4'
heroImage: '../../assets/posts/arduino-lite-brite-clock-led-multiplexing/thumbnail.jpg'
tags: ['arduino', 'led', 'multiplexing', 'clock', 'lite-brite', 'project']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is the first episode of the Arduino Lite Brite Clock build series — a multi-part project building a working digital clock using a Hasbro Lite Brite toy as the display housing and individual LEDs as the segments.

---

Sometimes the best project ideas come from watching a three-year-old play with a toy.

The Lite Brite uses small colored plastic pegs pressed into a backlit pegboard. The pegs are roughly the same diameter as a 5mm LED. That physical coincidence — an LED fitting snugly into a Lite Brite hole — is the whole premise of the build. Replace the plastic pegs with LEDs, connect them to an Arduino, and you have a matrix of individually controllable lights already mounted in a purpose-built enclosure with a grid of uniform holes. Add some code to drive them as a clock display, and you've got something genuinely cool on the shelf.

## The display design

Standard digital clocks use 7-segment displays — seven bar-shaped segments per digit that light up in combinations to show the numbers 0–9. The Lite Brite Clock replaces each bar segment with a cluster of LEDs. In the chosen arrangement, each bar is represented by three LEDs, giving the display a dotted-bar look when viewed from a distance.

A 7-segment digit uses seven bars, and three LEDs per bar gives 21 LEDs per digit. Two digits for the hours, two digits for the minutes — but we're building an HH:MM clock where the first hour digit is always 0 or 1, so it can be simplified. The final count works out to 46 LEDs total when you include two LEDs for the colon separator between hours and minutes.

This is where a naive approach runs out of steam quickly. 46 LEDs, one pin per LED: you need 46 I/O pins. The Arduino Uno has 14 digital pins and 6 analog pins, totaling 20. You're 26 pins short before you start.

## Multiplexing: making 20 pins do the work of 46

Multiplexing is the solution. The idea is to share pins between multiple LEDs by using the rows and columns of a matrix — where each LED sits at the intersection of a row line and a column line, and lighting any particular LED means activating its row and its column simultaneously.

For the Lite Brite Clock, the approach is common-anode multiplexing. The anode (positive) connections of all LEDs in a given row are tied together and connected to a single Arduino pin through a current-limiting resistor. The cathode (negative) connections of all LEDs in a given column are tied together and connected to another Arduino pin, and that pin is driven low to allow current to flow. To light a specific LED, you bring its row's anode pin high and its column's cathode pin low simultaneously.

The math works out like this for the Lite Brite Clock:

- 5 anode row pins (one per row of the LED grid)
- 10 cathode column pins (one per column)
- **Total: 15 pins** for the full 50-LED display budget (46 LEDs used)

Two additional pins handle buttons for setting the time. That's 17 pins — comfortably within the Uno's 20. The remaining three pins can be reserved for a speaker alarm, a real-time clock module, or other expansion.

The colon between hours and minutes is special-cased: since it's always on when the clock is running, its LED can tie directly to the 5V rail through a resistor rather than going through an I/O pin. That saves a pin for nothing.

## Why the Arduino Uno fits

People sometimes assume you need a more powerful microcontroller for a project with this many outputs. You don't, for two reasons.

First, multiplexing makes the pin count manageable. Second, the timing requirements are relaxed. Persistence of vision means the display only needs to scan through each row fast enough that your eye perceives all rows as continuously lit — around 30 complete scans per second is plenty. At 16 MHz, the Uno is executing millions of instructions per second; cycling through five rows and updating the time from an RTC is a tiny fraction of its capacity.

## Approximate cost

At 2012 prices, the bill of materials for this project was roughly:

- Lite Brite toy: ~$15
- Arduino Uno: ~$15
- LEDs (pack of 100+): ~$5 via eBay

Total under $35, and substantially less if the Arduino or LEDs were already on hand. If you already have an Uno in your parts bin, the display hardware alone is inexpensive enough to be an impulse buy.

## What's next in the series

With the concept locked in, the next steps are: ordering LEDs, fitting them into the Lite Brite grid, soldering cathode wires to each LED, building the anode resistor matrix on perfboard, and writing the display driver code. Each of those steps gets its own video — this is a longer build than most.

The rest of the Lite Brite Clock series is documented in subsequent posts on this site.

## References and further reading

- [Multiplexing 7-segment displays — Arduino Project Hub](https://projecthub.arduino.cc/SAnwandter1/programming-4-digit-7-segment-led-display-5c4617) — solid walkthrough of the multiplexing principle
- [7-segment LED clock with multiplexing — Fritzing](https://fritzing.org/projects/7-segment-led-clock-with-multiplexing) — schematic-level view of the wiring approach
- [Arduino Uno pinout reference](https://store.arduino.cc/products/arduino-uno-rev3) — 14 digital + 6 analog = 20 I/O pins
- [Persistence of vision — how multiplexing fools the eye](https://en.wikipedia.org/wiki/Persistence_of_vision) — the perceptual phenomenon that makes multiplexed displays work
