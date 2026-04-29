---
title: 'Arduino Lite Brite Clock: Testing LEDs Before You Solder (and What Happens If You Skip the Resistor)'
description: 'Why you test every LED with a resistor and a 9V battery before making any permanent solder joints — and a live demonstration of what a bare LED touching a 9V terminal looks like. Spoiler: it is not good.'
pubDate: 'July 27 2012'
youtubeId: 'KidBQaoNjPY'
heroImage: '../../assets/posts/arduino-lite-brite-clock-testing-leds/thumbnail.jpg'
tags: ['arduino', 'led', 'soldering', 'lite-brite', 'clock', 'project']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [parts list post](/blog/arduino-lite-brite-clock-parts) has the complete bill of materials.

---

Forty-six LEDs go into the Lite Brite Clock. Once they're wired up with cathode leads soldered together per row, discovering a dead LED means desoldering and rewiring. The fix for this is simple: test every LED individually before committing anything to solder.

## The test setup

A 9V battery, a 2.2kΩ resistor, and two alligator-clip leads is all you need. Wire them in series: battery positive → resistor → LED anode → LED cathode → battery negative. If the LED lights up, it works. Set it aside. If it doesn't, discard it and try another.

The 2.2kΩ resistor is more conservative than the 100Ω that will be used in the final circuit — it limits current more aggressively, so the LED will be dimmer than at full brightness. That's fine. You're not measuring luminous intensity; you're checking that the junction is intact and the LED is oriented correctly.

## Why polarity matters here specifically

The Lite Brite holes hold 5mm LEDs snugly, but "snugly" also means the LED can rotate slightly inside the hole. If the LED spins between the time you insert it and the time you solder its leads, the anode and cathode can swap positions without you noticing.

In a multiplexed matrix, a reversed LED doesn't just fail to light — it can also create unexpected current paths that affect adjacent LEDs. Testing for correct polarity immediately before making each solder joint is the right call. Not once per session, not once after installing a batch — right before each joint. Takes a second, saves a lot of debugging.

## What happens without the resistor

A 9V battery connected directly to an LED with no series resistor will destroy the LED immediately. The forward voltage of a standard 5mm LED is around 2V. At 9V with no current limiting, the current through the junction spikes far beyond the LED's maximum rating (typically 20 mA for continuous operation) in microseconds. The junction burns out, and the LED goes dark — sometimes with a brief flash, sometimes with a faint orange glow before it dies, and always with a slightly acrid smell from the plastic housing warming up.

This is demonstrated in the video. The LED connected bare to 9V flashes briefly, shows a faint orange residual glow, and is done. The smell is distinctive and not pleasant. It's worth experiencing once to understand viscerally why current-limiting resistors exist, but once is enough.

The same failure mode applies at lower voltages too, just more slowly. A 5V supply through a very low resistance — or no resistance at all — will eventually shorten an LED's life. The resistors in this build aren't optional.

## Diffusing the LEDs while you have them out

If you're using clear (water-clear) 5mm LEDs rather than pre-diffused ones, this is also the moment to sand them. Clear LEDs have a narrow viewing angle and can bleed light into adjacent Lite Brite holes, making the display look muddled up close.

A few strokes on a sheet of 320-grit sandpaper — just the dome of the LED, not the leads — frosts the plastic enough to widen the viewing angle and contain the glow within the LED's own hole. Don't overdo it: you want a light haze, not an opaque finish. Test the LED again after sanding to make sure you haven't cracked the housing or affected the leads.

## The workflow

1. Pick up an LED from the pile
2. Sand the dome lightly if using clear LEDs
3. Insert into the Lite Brite hole at the correct grid position
4. Test with 9V + 2.2kΩ before touching the iron — confirm it lights and confirm polarity
5. Make the solder joint
6. Repeat

It's methodical and a little tedious for 46 LEDs. It's much less tedious than desoldering a dead or backwards LED from a completed matrix.

## What's next

With all LEDs tested, installed, and polarity confirmed, the next step is wiring up the cathode leads — and an early encounter with 22-gauge wire's limitations for breadboard connections, covered in the [breadboard fail post](/blog/arduino-lite-brite-clock-breadboard-fail).
