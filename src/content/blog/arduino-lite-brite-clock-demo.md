---
title: 'Arduino Lite Brite Clock: The Finished Clock Running'
description: 'The Arduino Lite Brite Clock build series ends here — a 53-second clip of the completed clock keeping time in the garage, with the 2012 London Olympics opening ceremonies audible in the background.'
pubDate: 'July 30 2012'
youtubeId: '9KdWdqKzVig'
heroImage: '../../assets/posts/arduino-lite-brite-clock-demo/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'multiplexing']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is the final post in the Arduino Lite Brite Clock series. If you're coming in here first, the [multiplexing concept post](/blog/arduino-lite-brite-clock-led-multiplexing) is the right place to start — it covers the full design rationale, the pin math, and links to all the build episodes in order.

---

After 46 individual LEDs, two colon LEDs, eleven soldering sessions, one battery polarity surprise, and two short circuits found and fixed, the Arduino Lite Brite Clock works. The video is 53 seconds. That's all it needs to be.

## What the demo shows

The clock is running on battery power inside the original Lite Brite housing. The multiplexed 5×10 LED matrix is cycling through its row-scanning routine fast enough that persistence of vision makes all the digits appear to be on simultaneously. The two colon LEDs between the hours and minutes are always on — they're tied to 5V through a resistor, not switched by the Arduino.

The time display format is straightforward: hours, colon, minutes, in a simple segmented-digit layout driven by the multiplexing sketch. The sketch cycles through each of the five rows in sequence, pulling the correct anode row high while pulling the appropriate cathode columns low, then moving to the next row faster than the eye can detect the switching. Fifty times per second is plenty to avoid visible flicker; the sketch runs it faster than that.

If you listen to the video carefully, you can hear crowd noise in the background — that's the opening ceremony for the 2012 London Summer Olympics playing on the TV in the other room. July 27, 2012. The clock was finished just in time to document it while something worth remembering was happening.

## What it took to get here

The full build broke down into about twelve distinct sessions, each captured in a video and a companion post:

The [concept and multiplexing post](/blog/arduino-lite-brite-clock-led-multiplexing) established the approach — a 5-row × 10-column matrix driven by 15 Arduino I/O pins, scanning fast enough to appear as a steady display. The [parts post](/blog/arduino-lite-brite-clock-parts) covered the Lite Brite housing, the LEDs, the perfboard, and the 100Ω current-limiting resistors for each row.

[Testing the LEDs](/blog/arduino-lite-brite-clock-testing-leds) confirmed they all worked before any soldering happened — a step worth the time investment. [Positioning them](/blog/arduino-lite-brite-clock-positioning-leds) in the Lite Brite pegboard and adding [black paper behind the diffuser panel](/blog/arduino-lite-brite-clock-black-paper-background) gave the display the clean, high-contrast look it needed.

After a [breadboard prototype](/blog/arduino-lite-brite-clock-breadboard-fail) showed the concept worked but proved too fragile for a permanent build, the design moved to perfboard. The cathode and anode wiring sessions — [cathode rows](/blog/arduino-lite-brite-clock-wiring-leds), [perfboard resistors](/blog/arduino-lite-brite-clock-wiring-perfboard), and [anode columns](/blog/arduino-lite-brite-clock-solder-anode-columns) — were the long middle stretch of the build where most of the time went.

[Closing it up](/blog/arduino-lite-brite-clock-closing-up) was where the battery polarity issue surfaced and got fixed, and where the clock ran on its own power for the first time.

## The case for this kind of build

A Lite Brite clock is not a practical timekeeping device. A $5 digital clock from any drugstore keeps better time, runs on a pair of AA batteries for two years, and doesn't require soldering. The point was never practicality.

The point was working through a problem that's genuinely interesting — how do you drive more LEDs than you have output pins? The answer (multiplexing, time-division scanning, persistence of vision) is the same technique that makes LED dot matrix displays work in scoreboards, traffic signs, and commercial signage. Understanding it on a small scale with 46 hand-soldered LEDs and a $25 Arduino Uno is a legitimate way to internalize how those larger systems operate.

It also turned a piece of nostalgic plastic into something functional, which is its own kind of satisfying. The Lite Brite housing has exactly the right amount of light diffusion for a clock display — the translucent pegs scatter the LED output just enough that individual die spots aren't visible. You see digits, not point sources.

## What's next with this hardware

The build notes at the end of the [closing-up post](/blog/arduino-lite-brite-clock-closing-up) mention a few things left on the list: swapping the Arduino Uno for a Nano to reclaim interior space, and wiring in the two time-setting buttons that the sketch already accounts for. The sketch has the button-reading code; it just needs the hardware connected to match.

The clock sketch as built keeps time via `millis()` — the Arduino's millisecond counter. This is accurate enough for a few hours but drifts noticeably over days. An RTC module (a DS1307 or DS3231, either under $5 on eBay) would fix that permanently. The DS3231 in particular is accurate to about 2 ppm and keeps time on a backup coin cell when main power is removed — it would be a cleaner solution than button-setting the time every time the clock loses power.

## References and further reading

- [Arduino Lite Brite Clock build series — full index](/blog/arduino-lite-brite-clock-led-multiplexing) — all episodes, in order
- [Lite Brite — Wikipedia](https://en.wikipedia.org/wiki/Lite-Brite) — history of the toy and the Hasbro product line
- [Arduino millis() reference](https://www.arduino.cc/reference/en/language/functions/time/millis/) — the timekeeping function used in the clock sketch
- [DS3231 RTC module — Adafruit](https://www.adafruit.com/product/3013) — the upgrade path for accurate timekeeping
- [Persistence of vision — Wikipedia](https://en.wikipedia.org/wiki/Persistence_of_vision) — the optical phenomenon the multiplexing scheme relies on
- [Instructables build guide](https://www.instructables.com/Lite-Brite-LED-clock/) — the Instructables write-up Lonnie published alongside the YouTube series
