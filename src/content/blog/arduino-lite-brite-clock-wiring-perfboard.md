---
title: 'Arduino Lite Brite Clock: Wiring the Perfboard (100Ω Anode Resistors)'
description: 'Cutting perfboard to size, positioning twelve 100Ω current-limiting resistors for the anode column lines, and soldering the hookup wires that will feed back to the Arduino — the Lite Brite Clock matrix taking shape.'
pubDate: 'July 29 2012'
youtubeId: 'NASbN6c69vA'
heroImage: '../../assets/posts/arduino-lite-brite-clock-wiring-perfboard/thumbnail.jpg'
tags: ['arduino', 'led', 'perfboard', 'soldering', 'lite-brite', 'clock', 'project']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [concept and multiplexing post](/blog/arduino-lite-brite-clock-led-multiplexing) explains the overall design. The [LED wiring post](/blog/arduino-lite-brite-clock-wiring-leds) covers soldering cathode wires to each LED.

---

With cathode wires soldered to all 46 LEDs, the next step is the anode side: a small piece of perfboard that holds twelve 100Ω resistors and routes the per-row anode connections back to the Arduino. This is the point in the build where loose wires start becoming an organized circuit.

## Why perfboard for this step

Breadboards are convenient for prototyping but they're not permanent — connections can be bumped loose, wires can pull out, and if the robot chassis or clock housing gets moved around, things shift. Perfboard (also called protoboard or strip board, depending on the layout) gives you a place to make solder connections that will stay made.

For the Lite Brite Clock, the perfboard holds the current-limiting resistors in a fixed arrangement and gives you proper solder pads to connect the anode wires coming from the LED matrix and the outgoing wires heading toward the Arduino. Everything flows through this board: incoming power on the anode side, resistors to limit current, and then on to the shared anode line for each row.

## Sizing the perfboard

A strip of perfboard big enough to hold twelve resistors in a row — one per anode column plus two for the clock colon — doesn't need to be large. Perfboard is easy to cut to size with a utility knife (score-and-snap along the hole grid) or a small hacksaw. Score several times along the same row of holes before snapping; trying to snap it with a single light score tends to crack the board in the wrong place.

Cut the piece to fit in whatever space you've allocated inside the build. Because the Lite Brite Clock housing has fixed dimensions, space is a consideration.

## The resistor math

Every LED in the matrix needs a current-limiting resistor. In the common-anode multiplexing scheme used here, the resistors go on the anode side (the positive side of each LED row). Using a 5V supply and LEDs with a typical forward voltage of about 2V and a target current of around 20 mA:

```
R = (Vsupply − Vforward) / Itarget
R = (5V − 2V) / 0.020A
R = 150Ω
```

100Ω is slightly lower than the calculated value — it pushes the LEDs a bit brighter and the current a bit higher, but still within safe operating range for standard 5mm LEDs at the duty cycles used in multiplexed operation (each LED is only on a fraction of the scan period). The exact resistor value is a tradeoff between brightness and LED longevity; 100Ω to 150Ω is reasonable for this application.

One resistor per anode line — twelve total for the twelve columns (ten display columns plus two for the colon). Since all the LEDs in each anode row share that resistor, it limits the current for the entire row at once.

## Pre-positioning before soldering

The workflow that works well here: insert all twelve resistors into the perfboard holes, bend their leads slightly to hold them in place (the standard technique for through-hole components on perf), then solder them all before attaching any wires. Once the resistors are fixed, you can add the anode hookup wires at each resistor's input and the outgoing wires at its output, with clear solder pads to work from.

Pre-positioning the resistors before soldering means you can look at the whole layout and verify the spacing makes sense before committing to anything. Resistors are cheap and desoldering them is not fun — taking an extra minute to dry-fit everything is worth it.

## Wire gauge matters for breadboard connections

The outgoing wires from this perfboard connect back to the breadboard and eventually to the Arduino's analog and digital pins. Standard hookup wire for this kind of job is 22 AWG solid-core wire — the "hookup wire" sold in small rolls at any electronics supplier or hardware store.

The issue with going smaller (24 AWG or thinner) is that breadboard socket contacts are sized for 20–22 AWG wire. Thinner wire makes poor contact in a breadboard socket and tends to pull out or shift. 22 AWG solid-core sits firmly in the socket and stays there. If you're running wires that will only connect to solder pads (not breadboard holes), thinner and more flexible wire is fine.

## Twelve connections, patience required

This is another session where systematic work pays off. Solder all the resistors first, verify them, then do the incoming wires one row at a time, then the outgoing wires. A methodical approach with checkpoints beats trying to do everything at once and losing track of which wire goes where.

When all twelve connections are done and verified with a continuity check, the perfboard is ready to integrate with the LED matrix and the Arduino wiring.

## What's next

With the anode resistor board complete and the cathode wires already on the LEDs, the next phase is making the actual connections to the Arduino and writing the display driver code. Subsequent episodes in the Lite Brite Clock series cover the full wiring integration and the software.

## References and further reading

- [Lite Brite Clock concept and multiplexing](/blog/arduino-lite-brite-clock-led-multiplexing) — the full pin count, design rationale, and multiplexing scheme
- [Perfboard techniques — Adafruit](https://learn.adafruit.com/collins-lab-breadboards-and-perfboards/overview) — through-hole soldering on perf, from strain relief to component layout
- [LED current limiting resistor calculator — Digikey](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-led-series-resistor) — plug in your supply voltage, LED specs, and target current
- [22 AWG solid-core hookup wire — SparkFun](https://www.sparkfun.com/products/8023) — the right gauge for breadboard connections
