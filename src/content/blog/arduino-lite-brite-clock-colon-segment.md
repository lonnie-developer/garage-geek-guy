---
title: 'Arduino Lite Brite Clock — Building the Colon Segment'
description: 'How the blinking colon between hours and minutes is wired into the hand-built LED matrix clock. Covers dedicated column placement, row participation, and 500ms blink timing.'
pubDate: 'July 30 2012'
youtubeId: 'GHr_ggAv0xw'
heroImage: '../../assets/posts/arduino-lite-brite-clock-colon-segment/thumbnail.jpg'
tags: ['arduino', 'leds', 'led-matrix', 'lite-brite-clock', 'tutorial', 'soldering']
---

*Part of the Arduino Lite Brite Clock build series — a hand-wired 5×12 LED matrix clock later featured in Make Magazine. This episode covers the colon segment that separates the hours from the minutes.*

The colon on a digital clock is easy to overlook. It's two dots. It blinks once a second. You stop seeing it within a few seconds of glancing at the display, and your brain quietly registers "that's a clock" without consciously processing what those two LEDs are doing.

But in a hand-wired matrix where every LED needs a defined row and column address, the colon is a design decision. It needs to sit in the matrix in a way that doesn't interfere with the digit columns, participate in row scanning like every other LED, and blink on a half-second cadence without disturbing the display multiplexing. Getting all three right is the thing this episode shows.

## Where the colon lives in the 5×12 matrix

The full matrix layout is 5 rows by 12 columns: 10 columns for the two pairs of digits (hours and minutes, five columns per digit), and 2 columns reserved for the colon. The colon columns sit in the center of the matrix, between the hours digits on the left and the minutes digits on the right.

Two columns for two dots: one column per colon LED. Each colon LED occupies a single position in its column — the upper dot sits in one row, the lower dot sits in another. They share their column wire with nothing else, which keeps their control independent from the digit segments.

This is the simplest possible colon implementation and also the most reliable one. Some builders try to sneak the colon LEDs into unused segment positions of the outer digits, but that creates entanglements in the row-column logic that become painful when you're writing the display driver code. Two dedicated columns costs two Arduino pins; it buys clean, independent colon control.

## Row participation

The colon columns participate in the same row scan as everything else. The matrix has 5 rows; the colon LEDs don't occupy all five row positions — just the two that correspond to the dot positions (say, rows 2 and 4, offset to vertically center the colon on the display). The other three row positions in the colon columns are simply never driven — those column pins stay low whenever those rows are active.

This is no different from a digit column where not all segments are lit for a given character. The multiplexing doesn't know or care that a column is a colon rather than a digit — it just sees a column pin that either goes high or doesn't during each row's scan window.

## Soldering the colon into the matrix

The colon LEDs get wired the same way as the rest of the matrix. Their cathode leads are part of the same row wires soldered in the previous episode — the horizontal cathode rows run all the way across the matrix, including through the colon column positions. The anode leads get their own column wires, just like the digit columns.

The physical placement matters: the colon LEDs should be vertically centered on the display so the dots read as a colon rather than randomly placed indicators. A little time with a ruler before soldering is worth it.

## Making the colon blink

The standard approach for a blinking colon is a 500ms toggle — on for half a second, off for half a second. In software, the most straightforward implementation uses `millis()` to track elapsed time without blocking:

```cpp
unsigned long lastBlink = 0;
bool colonState = false;

void loop() {
  unsigned long now = millis();
  if (now - lastBlink >= 500) {
    colonState = !colonState;
    lastBlink = now;
  }
  // During each row scan, drive the colon columns based on colonState
  // ...
}
```

This avoids `delay()`, which would freeze the multiplexing scan and cause visible flicker on the rest of the display. The rest of the display loop runs continuously; the colon toggle is just a state variable that gets checked on every pass and acted on only when 500ms have elapsed.

In the matrix driver code, when scanning the rows that contain colon LEDs, you simply include or exclude the colon column pins based on `colonState`. The display scanning loop handles everything else the same way it always does.

## The alternative: hardware blink

Some builders use a 555 timer oscillator running at 1Hz to drive the colon LEDs independently of the Arduino, completely outside the multiplexing loop. It's a clean separation of concerns — the colon blinks reliably regardless of what the Arduino sketch is doing. The tradeoff is extra components and a separate power path to the colon LEDs.

For a clock that's already got an Arduino handling all the other display logic, the software `millis()` approach is simpler and uses no additional parts.

## Where this fits in the build

After the colon is in place, the physical matrix is complete: 60 LEDs (10 columns × 5 rows = 50 digit-segment LEDs, plus the 2 colon LEDs across their 2 columns × 1 row each = 2 LEDs, plus remaining row positions unused — exact count depends on layout). The next step is connecting the Arduino's digital I/O pins to the matrix columns and rows, plus the current-limiting resistor perfboard that sits between the column pins and the matrix.

The build sequence so far:

1. [Diffuse the LEDs](/blog/arduino-lite-brite-clock-diffuse-leds) — sand the domes for wide viewing angles
2. [Solder cathode rows](/blog/arduino-lite-brite-clock-solder-led-cathode-rows) — tie cathodes together horizontally
3. Solder anode columns — tie anode leads vertically
4. Wire the colon segment **(this episode)**
5. [Connect the Arduino to the matrix](/blog/arduino-lite-brite-clock-connect-arduino-led-matrix) — wiring the digital I/O pins through the resistor perfboard

## References and further reading

- [Multiplexed LED display timing | EmbeddedRelated](https://www.embeddedrelated.com/showarticle/624.php) — clear explainer of how multiplexing and timing interact
- [Using millis() for timing | Arduino documentation](https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/) — the blink-without-delay pattern used for the colon toggle
- [Seven-segment display | Wikipedia](https://en.wikipedia.org/wiki/Seven-segment_display) — background on the segment layout standard that influenced the matrix digit design
- [Next: connecting the Arduino to the matrix](/blog/arduino-lite-brite-clock-connect-arduino-led-matrix)
