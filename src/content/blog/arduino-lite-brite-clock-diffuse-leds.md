---
title: 'Arduino Lite Brite Clock — Diffusing the LEDs'
description: 'Why you need to diffuse the LEDs in a hand-built LED matrix clock, and how to do it with sandpaper. Short time-lapse of sanding 46 LEDs for the Lite Brite Clock build.'
pubDate: 'July 26 2012'
youtubeId: 'x9oFzZA6WeY'
heroImage: '../../assets/posts/arduino-lite-brite-clock-diffuse-leds/thumbnail.jpg'
tags: ['arduino', 'leds', 'lite-brite-clock', 'tutorial', 'led-matrix']
---

*This is part of the Arduino Lite Brite Clock build series — a hand-wired LED matrix clock that was later featured in Make Magazine. This entry covers the prep step: diffusing the LEDs before they go into the matrix.*

The difference between a bare clear LED and a diffused one is the difference between a flashlight and a frosted bulb. The flashlight puts a tight cone of intense light in one direction; the frosted bulb glows all over and doesn't blind you when you look at it. For a clock face where 46 LEDs sit close together in a tight matrix, that distinction matters quite a bit.

This video is a time-lapse of the diffusion process — sanding 46 clear LEDs by hand before they go into the matrix. It's meditative work that's also genuinely necessary to make the finished clock look good rather than just functional.

## Why bare LEDs look bad in a matrix

A standard clear LED has a narrow beam angle — typically 15 to 30 degrees. Most of the light shoots straight forward out of the dome. When you have multiple LEDs packed tightly together, two problems emerge.

The first is *bleed*: the bright cone from an illuminated LED angles slightly sideways and lights up the surface of adjacent unlit LEDs, making them glow faintly even when they're supposed to be off. In a digit display where the contrast between on and off segments matters, that bleed washes out the image.

The second is *directionality*: the clock face looks dramatically different depending on the viewing angle. Straight-on, it's bright. Slightly to the side, the LEDs go dim. For something that sits on a shelf and gets viewed from multiple angles, that's annoying.

Diffusing the LED dome scatters the light into a much wider angle — typically 120 degrees or more — and makes the LED look like it's glowing from the inside rather than firing a beam at you. Adjacent LEDs stop bleeding into each other, contrast between on and off improves noticeably, and the display looks good from anywhere in the room.

## The sanding approach

The dome of a standard LED is clear epoxy. Scuff the surface with sandpaper and it becomes translucent — the same optical effect as frosted glass. The technique:

Start with 200 or 220 grit sandpaper. Wet the paper lightly (wet sanding generates less heat and finer scratches than dry). Hold the LED by its leads and sand the dome in small circular motions against the paper. It takes maybe 15 to 30 seconds per LED to go from clear to uniformly hazy. You'll see the change immediately — the dome goes from transparent to milky white.

You don't need to progress to finer grit for this application. The goal is a consistent haze across the whole dome, not a polished surface. Once it's uniformly cloudy with no clear spots, it's done.

For 46 LEDs, expect to spend 20 to 30 minutes. It's the kind of task that's just time, not skill — which is why the video shows it as a time-lapse.

## The gotcha: don't sand too aggressively

There's a point of diminishing returns. Light diffusion happens quickly once you break the surface; grinding away more epoxy past that point doesn't improve the diffusion but does reduce brightness, since you're removing material that was helping refract and transmit light. Sand until the dome is uniformly hazy, then stop.

Also worth noting: the leads get slippery when wet. If you're going fast, it's easy to fling a tiny LED across the workbench. Keep a bowl or tray nearby to collect them, and maybe do a count before and after.

## The smarter option: buy pre-diffused

Diffused LEDs — sometimes listed as "frosted" or "milky white" LEDs — are widely available and cost essentially the same as clear ones. The frosted epoxy dome is molded in from the factory. For a project where you're buying 46 or 60 LEDs anyway, just ordering the diffused version saves 20 to 30 minutes of sanding.

The reason this build uses clear LEDs that then get sanded is almost certainly that they came out of a component drawer that already had them — the kind of decision that gets made at the start of a build when you're just trying to get going. If you're sourcing parts fresh, order diffused. The build notes even say so explicitly.

## Where this fits in the Lite Brite Clock build

This is the prep step that comes before the matrix assembly. The sequence:

1. Sand and diffuse all LEDs (this video)
2. Solder the cathode rows — tie all cathode leads horizontally across each row
3. Solder the anode columns — tie anode leads vertically down each column
4. Build the resistor perfboard — 100-ohm current-limiting resistors for each column
5. Wire the colon segment
6. Connect everything to the Arduino

The sanding happens first because once the LEDs are soldered into the matrix, you can't get sandpaper near the domes without risking damage to the joints. Do the surface prep before any assembly starts.

## References and further reading

- [Diffused vs. clear LEDs — Adafruit](https://learn.adafruit.com/all-about-leds/the-led) — good explanation of LED optics and why diffusion affects viewing angle
- [How to diffuse an LED | Instructables](https://www.instructables.com/Diffuse-an-LED/) — step-by-step with photos of the wet-sanding approach
- [LED viewing angle and intensity | SparkFun](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds/all) — technical background on how dome geometry affects beam pattern
- [Lite Brite Clock series overview | Garage Geek Guy](/blog/arduino-lite-brite-clock-solder-led-cathode-rows) — the next step in the build: soldering the cathode rows
