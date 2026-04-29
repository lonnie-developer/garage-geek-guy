---
title: 'Arduino Lite Brite Clock: Why the Black Paper Background Matters'
description: 'A short but important build step — cutting the black paper insert to fit behind the Lite Brite pegboard and why without it the LED display reads as a muddy wash of ambient light.'
pubDate: 'July 26 2012'
youtubeId: 'xRRrOd9mH1I'
heroImage: '../../assets/posts/arduino-lite-brite-clock-black-paper-background/thumbnail.jpg'
tags: ['arduino', 'led', 'lite-brite', 'clock', 'project', 'assembly']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [concept and multiplexing post](/blog/arduino-lite-brite-clock-led-multiplexing) is the right place to start if you're following from the beginning.

---

Not every step in a build is technically complex. Some are just necessary. The black paper background is one of those — it takes about five minutes, it's easy to overlook, and skipping it makes the display noticeably worse.

## What the black paper does

A lit LED inside a Lite Brite hole produces a point of colored light. The key word is "point" — ideally, that glow is contained to its own hole and stands out sharply against a dark background. Without the black paper insert behind the pegboard, ambient room light floods through every hole — lit and unlit alike. The contrast between an active LED and the surrounding grid collapses. From a few feet away the display looks like a dim, undifferentiated wash rather than a readable set of bright digits.

The black paper creates the dark background that makes the difference. It sits between the pegboard and the back panel of the housing, blocking light from passing through unoccupied holes while letting the LED glow through from the front. The darker and more opaque the paper, the better the contrast.

The original Lite Brite toy came with sheets of black construction paper pre-punched with patterns — you'd lay the paper over the board and push pegs through. For this build, the paper serves the same optical function but in reverse: it goes behind the board, not on top, and no pre-punching is needed. The LEDs are already in position; the paper just needs to cover the back face of the pegboard.

## Cutting it to fit

Standard construction paper or black cardstock works fine. The Lite Brite pegboard isn't a particularly large surface — the sheet of paper doesn't need to be precise, just big enough to cover the grid area without gaps.

Fitting it involves one small annoyance: the pegboard area isn't a perfect rectangle on every Lite Brite model, and the paper needs to sit behind the board without buckling or overlapping into the housing in a way that prevents closure. A paper trimmer would make this cleaner; most workshops don't have one handy. A straight edge and scissors gets close enough. The corners don't have to be perfect — once the housing is closed, no one will see them.

The fit in this build turns out fine on the first cut: the paper covers the grid area, lies flat against the back of the pegboard, and doesn't interfere with the housing reassembly. A bit of selective perfectionism crept in during the trimming process, which is noted for the record. Acceptable is acceptable.

## The display difference

The contrast improvement from adding the black paper is immediate and visible. Lit LEDs pop. Unlit positions recede into dark holes rather than glowing with reflected ambient light. The clock reads as a clock rather than as a backlit smear.

This is worth doing before any wiring begins — it's a lot easier to lay the paper in place before the interior is full of wires and perfboard. Once the electronics are in and the housing is crowded, fitting a flat sheet of paper cleanly becomes a more awkward job.

## The broader takeaway

The original Lite Brite was designed to use its black paper inserts for exactly this reason — the toy's designers understood that contrast is what makes the light display readable. Reusing that design intent in an electronics project is one of the things that makes the Lite Brite a genuinely good enclosure choice for a clock display. The form factor does some of the work for you.

The [parts list post](/blog/arduino-lite-brite-clock-parts) has more on why the Lite Brite was chosen for this build and what else you'll need to put it together.
