---
title: 'Arduino Lite Brite Clock: First Display Test and How the Digit Code Works'
description: 'Closing the housing for the first software test, watching all 46 LEDs count through their positions, and a walkthrough of the digit-definition approach that makes placing numbers on a multiplexed grid manageable.'
pubDate: 'July 30 2012'
youtubeId: '5vpL7xbSmZ0'
heroImage: '../../assets/posts/arduino-lite-brite-clock-preliminary-testing/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'programming', 'multiplexing']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [anode wiring post](/blog/arduino-lite-brite-clock-solder-anode-columns) covers the last major soldering phase before this test. If you're starting from the beginning, the [concept post](/blog/arduino-lite-brite-clock-led-multiplexing) explains the multiplexing scheme and pin layout.

---

The soldering is done. The matrix is wired. The Arduino is connected to the display. This episode is the moment you close the housing and find out whether the wiring actually works — and, mostly, it does.

## Closing it up for the first real test

Going into this test, there's a specific concern: 22-gauge wire in Arduino pin headers. Breadboard sockets are unreliable with 22 AWG — they grip loosely and lose contact easily — but the Arduino's header pins are a tighter fit and generally hold adequately. Closing the housing compresses everything slightly and any wire that was only marginally seated can shift enough to disconnect.

The answer is to close the housing carefully, power it up, and see what happens. The sketch already loaded is actually a leftover from an earlier project (ClusterBot, a robot build that used the same Arduino). That gets replaced immediately with the display test sketch.

The test sketch doesn't try to tell time. It just cycles the display through all numbers in all positions — every LED combination in sequence — so you can visually confirm that all 46 LEDs light correctly and that no rows or columns are dead, shorted, or ghosting.

## What the test shows

Result: mostly good. The display runs through its cycle and everything lights. The multiplexed matrix is working — the five row drivers and ten column drivers are all responding correctly, and the persistence-of-vision effect is doing its job. From a few feet away the display looks like a real clock face rather than a flickering grid.

One issue turns up: the bottom LED of the colon isn't lighting. The top one works. This is almost certainly a loose or disconnected wire — the colon LEDs are wired directly to 5V through a resistor rather than through the matrix, so a failed colon LED doesn't affect the row/column diagnostic. It just means one of two wires isn't making contact. The fix is opening the housing again and reseating the connection, which goes on the list for the next session.

## How the digit-display code works

With the display confirmed functional, it's worth stepping through the programming approach, because multiplexed displays require a bit of thought about how you represent numbers in code.

The clock face has four digit positions (plus the colon): left two digits for hours, right two for minutes. Each digit occupies a 3×3 column section of the LED grid — three columns wide, three rows tall, giving nine possible pixel positions per digit.

The approach for defining each digit is to write a function for each numeral (0 through 9) that lists which of those nine pixel positions should be lit. A "4" in this grid, for example, has nine pixels defined — two vertical lines that converge at a horizontal crossbar — and the function simply lights those specific row/column intersections.

The clever part is how positions are handled without writing separate code for each digit location. Rather than hardcoding absolute column numbers for every occurrence of every digit, the functions accept a column offset: to draw a "4" in the leftmost digit position, pass offset 0; to draw it in the second position, pass offset 3 (because digit positions are three columns apart); third position gets offset 6. Inside the function, every column reference is written as `3 + x` or `6 + x` where `x` is the passed offset, so the digit appears at the correct horizontal position on the display.

This means each numeral is defined once. Displaying any digit at any clock position is a single function call with an offset argument. The clock sketch uses four such calls per display cycle — one for each digit — plus whatever logic handles the colon.

## What still needs to happen

At this point in the build, the display works and the digit code is proven. Three items remain on the punch list:

The **time-keeping function** needs to be incorporated. The current sketch just demonstrates the display; the actual timekeeping uses the Arduino's millis() counter (or a real-time clock module if accuracy matters long-term) to track elapsed time and update the displayed hour and minute values accordingly.

The **time-setting buttons** need to go in. Without them, the time is hardcoded in the sketch and can only be changed with a computer. Two momentary push buttons, drilled into the housing and wired to Arduino pins with pull-up resistors, add hour-increment and minute-increment controls.

The **battery connection** is the final step — wiring the 9V battery pack's connector to the Arduino's barrel jack so the clock runs without USB. That step, and a small polarity surprise, are covered in the [closing-up episode](/blog/arduino-lite-brite-clock-closing-up).
