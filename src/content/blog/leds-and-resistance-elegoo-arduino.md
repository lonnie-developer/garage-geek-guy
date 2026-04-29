---
title: 'LEDs and Resistance — Elegoo Arduino Lesson 3'
description: 'Why LEDs need resistors, how to read resistor color codes (or just look at the label), how the breadboard connects everything, and what happens when you use a 220Ω, 1kΩ, and 10kΩ resistor side by side. The most fundamental circuit in the kit.'
pubDate: 'October 27 2019'
youtubeId: 'ShZQNGtrPEQ'
heroImage: '../../assets/posts/leds-and-resistance-elegoo-arduino/thumbnail.jpg'
tags: ['arduino', 'led', 'resistors', 'elegoo', 'beginner', 'tutorial']
---

Every beginner electronics kit comes with LEDs. Every beginner electronics kit also comes with resistors. They always go together, and there's a good reason for that — an LED without a current-limiting resistor is a LED you're about to destroy.

This is lesson 3 in the Elegoo Arduino kit series. It's intentionally simple: no code, no microcontroller, just 5V from the Arduino's power pin, a few resistors with different values, and LEDs that demonstrate exactly why the resistance value you pick matters.

## Why resistors are necessary

An LED is a diode. When it's forward biased — positive voltage on the anode, negative on the cathode — it conducts. The problem is that LEDs don't naturally limit the current that flows through them. As voltage increases, current increases rapidly, and the LED can only handle so much before the magic smoke leaves.

A 5mm red LED is typically rated for 20 mA continuous. The Arduino's 5V output doesn't inherently know or care about that limit. Put a direct wire between 5V and GND through an LED, and you're asking the LED to handle whatever current the voltage and the LED's forward voltage work out to — usually enough to kill it almost immediately. (Or as described in the video: connect one to a 9V battery and it pops.)

A series resistor limits the current. Ohm's law: `I = V / R`. The voltage across the resistor is the supply voltage minus the LED's forward voltage drop (around 2V for a red LED, so ~3V across the resistor from a 5V supply). With a 220 Ω resistor: `3V / 220Ω ≈ 14 mA` — safely under the 20 mA limit. With a 1 kΩ resistor: `3V / 1000Ω = 3 mA` — dimmer. With a 10 kΩ resistor: `3V / 10000Ω = 0.3 mA` — barely visible.

## The breadboard basics

The breadboard in the Elegoo kit is an MB-102 style board. Before wiring anything, it's worth understanding how the connections work:

The two long rails on each side — marked with red (+) and blue (–) — run the full length of the board. Every hole in the red rail is connected to every other hole in the red rail. Same for the blue. These are your power and ground distribution rails. Connect 5V from the Arduino to the red rail and GND to the blue rail, and you have power and ground available anywhere along the board's edge.

The short rows in the middle — the ones with five holes per row — are connected horizontally. All five holes in one row share a connection, but they're isolated from the row above and the row below. There's also a gap down the center of the board (the "channel") that breaks the connection between the left half and right half of each row. This is so you can straddle an IC chip across the gap and have each pin connect to a separate row.

## LED polarity

LEDs are diodes, so direction matters. The two legs are different lengths:

- **Long leg = anode = positive (+)**
- **Short leg = cathode = negative (–)**

Current flows from anode to cathode. Wire the long leg toward your 5V supply and the short leg toward ground. Reverse them and the LED simply won't light — no damage, just darkness.

## The three-resistor comparison

The demo wires three LEDs side by side, each with a different resistor value:

**Left LED: 220 Ω** — the standard value for a 5V/Arduino circuit. Gives around 14 mA, which is close to a red LED's rated brightness. This is the one to use in most circuits.

**Middle LED: 1 kΩ** — noticeably dimmer than the 220 Ω LED. About 3 mA through the LED. Still clearly on, but you'd notice the difference in a room with normal lighting.

**Right LED: 10 kΩ** — barely on. You have to look closely to see it. At 0.3 mA, it's well below the threshold for practical indicator use, though it would still register on a photodiode or light sensor.

When all three are powered simultaneously, the brightness gradient is obvious: bright → medium → barely there, left to right. That's the whole lesson made visible.

## Wiring it up

```
Arduino 5V  →  breadboard red rail (+)
Arduino GND →  breadboard blue rail (–)

Red rail (+) →  220Ω resistor → LED1 anode (long leg)
Red rail (+) →  1kΩ resistor  → LED2 anode (long leg)
Red rail (+) →  10kΩ resistor → LED3 anode (long leg)

Each LED's cathode (short leg) → blue rail (–)
```

The resistors connect from the power rail to the LED's positive leg. Current flows through the resistor, through the LED, and out to ground. The LEDs are all in parallel between 5V and GND, each with its own current-limiting resistor — they don't interact with each other.

## Reading resistor color codes

The resistors in the Elegoo kit have their values printed on the paper tape they're stored on, which is the easiest way to identify them. They're also color-coded with bands you can read directly.

For a 220 Ω resistor: **Red – Red – Brown – Gold** (2 – 2 – ×10 – ±5%). For 1 kΩ: **Brown – Black – Red – Gold** (1 – 0 – ×100 – ±5%). For 10 kΩ: **Brown – Black – Orange – Gold** (1 – 0 – ×1000 – ±5%).

If the color code approach isn't clicking, use a multimeter in resistance mode — probe both legs of the resistor and read the value directly. It's slower but unambiguous.

## What to take from this

The practical upshot: always put a resistor in series with an LED when driving from Arduino's 5V or 3.3V pins. 220 Ω is the go-to value for a red LED at 5V if you want reasonable brightness. If brightness doesn't matter (indicator LEDs you just need to be *on*) or you're battery-constrained, 1 kΩ or higher is fine. Never connect an LED directly to a supply rail without any resistor.

This is the foundational circuit that appears in almost every project on this channel — sensors with status LEDs, motor driver status indicators, debugging lights. Getting comfortable with the breadboard layout and the resistor math here pays off in every project that follows.

## References and further reading

- [LED current limiting resistor calculator (Digi-Key)](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-led-series-resistor) — enter your supply voltage, forward voltage, and desired current; get the resistor value
- [Resistor color code guide (SparkFun)](https://learn.sparkfun.com/tutorials/resistors/decoding-resistor-markings) — the 4-band and 5-band color code systems explained with examples
- [Arduino voltage and current limits](https://store.arduino.cc/products/arduino-uno-rev3) — the 5V pin and digital I/O pin current limits (I/O pins: 40 mA max per pin, 200 mA total)
- [LED forward voltage reference (Adafruit)](https://learn.adafruit.com/all-about-leds/forward-voltage-and-current) — typical forward voltages for different LED colors; important for accurate resistor calculations
- [Ohm's Law and power explained (Khan Academy)](https://www.khanacademy.org/science/ap-physics-1/ap-circuits-topic/current-ap/a/ee-current) — the underlying physics behind V = IR and current limiting
