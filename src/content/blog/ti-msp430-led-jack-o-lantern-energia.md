---
title: 'Programmable LED Jack-o-Lantern with the TI MSP-430 Launchpad + Energia IDE'
description: "Replace a fake pumpkin's incandescent bulb with 6 individually-controlled LEDs and program the whole thing with the TI MSP-430 Launchpad and Energia — which is basically the Arduino IDE with a red color scheme and TI chip support."
pubDate: 'October 30 2013'
youtubeId: 'KVq9FPZn4NI'
heroImage: '../../assets/posts/ti-msp430-led-jack-o-lantern-energia/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'energia', 'led', 'halloween', 'tutorial']
---

Every fake Halloween pumpkin comes with the same incandescent bulb inside — a dim orange glow that's completely non-programmable and burns out every few seasons. Replacing it with LEDs is the obvious upgrade. Programming each LED individually, with a microcontroller, so you can make the eyes a different color from the mouth and add a flickering candle effect in software — that's the fun version.

This build uses the Texas Instruments MSP-430 G2553 Launchpad and the Energia IDE, which is worth a few words of explanation because not everyone has heard of either. If you know Arduino, the learning curve here is essentially zero. If you don't, it's still manageable — the Launchpad is a $10 TI dev board, and Energia is an Arduino-compatible IDE that runs the same `pinMode`, `digitalWrite`, `delay` API, just targeting TI's MSP-430 line of ultra-low-power microcontrollers instead of Atmel AVR.

The Energia IDE is literally a fork of the Arduino codebase. Same layout, same buttons, same serial monitor. The only visible difference is the color scheme — it's red instead of blue. Everything else, including the sketch structure and all the standard functions, is identical.

> *This build is from Halloween 2013, back when the channel was still MeanPC.com — same bench, same Siamese cat trying to get inside the pumpkin.*

## The build plan

The pumpkin is a standard fake plastic jack-o-lantern — the kind you find at a craft store for a few dollars. The existing incandescent socket gets removed entirely, and six LEDs go in its place: two green ones for the eyes, one yellow for the nose, and three pink ones for the three segments of the carved mouth.

Each LED gets its own GPIO pin on the Launchpad, so all six can be controlled completely independently — different blink rates, different patterns, whatever the code decides. For a first build, we're starting with a simple sequential flash. The more interesting effect — randomized blink timing to mimic a candle — comes later, once the wiring and code are confirmed working.

## What you'll need

- Texas Instruments MSP-430 G2553 Launchpad (~$10, available directly from TI)
- 6 LEDs: 2 green, 1 yellow, 3 pink (or whatever colors your pumpkin suggests)
- Six **100 Ω resistors** — one per LED on the cathode side
- Breadboard
- Doorbell hookup wire — 22-gauge solid-core, from any hardware store. A $6 spool from Home Depot is more than enough. Much sturdier than thin breadboard jumpers and easier to route inside a pumpkin cavity.
- Heat-shrink tubing (to insulate soldered connections from the foil reflectors)
- Super glue (for mounting LEDs in their cups)
- Aluminum foil + plastic cups (for the reflectors — optional but makes the light output much better)
- Energia IDE (free download from energia.nu)

## Wiring

The circuit is as simple as LED circuits get: each LED's cathode (negative leg) runs through a 100 Ω current-limiting resistor to a GPIO pin on the Launchpad. All six anodes (positive legs) share a common ground connection back to the Launchpad's GND pin.

In code, `HIGH` turns an LED on; `LOW` turns it off. No multiplexing, no shift registers — each LED has its own dedicated pin.

The pin assignments used in the video:

| LED | Color | Launchpad pin |
|---|---|---|
| Left eye | Green | 2 |
| Right eye | Green | 3 |
| Nose | Yellow | 4 |
| Right mouth | Pink | 5 |
| Left mouth | Pink | 6 |
| Middle mouth | Pink | 7 |

The wiring convention worth noting: the LED cathodes go through the resistors to the GPIO pins, and the anodes go to ground. That means the GPIO pins source the LEDs' return current — which is fine for the MSP-430's I/O pins at these currents. The 100 Ω resistors at 3.3V limit current to about 20–25 mA per LED, well within the standard LED rating.

## Why doorbell wire

Standard breadboard jumpers are thin, flexible, and annoying to route inside a hollow plastic pumpkin. Doorbell hookup wire (22-gauge solid copper) is stiff enough to hold its shape when bent, tough enough to tolerate being pulled in and out of tight spaces, and cheap enough to buy in a 30-foot spool and not worry about it. Solder a short length to each LED lead, apply heat-shrink over the joint, and you have a durable connection that won't flex apart when you're repositioning things inside the pumpkin.

## The reflectors

The difference between an LED dumping light in all directions and one that illuminates the pumpkin face properly is a reflector. The solution used here: cut plastic cups to fit the eye, nose, and mouth cutouts, line them with aluminum foil, and mount the LED so it points into the back of the cup. The foil reflects the light forward and out through the pumpkin face. The result looks much more intentional than a bare LED dangling in open air.

For the eyes and nose (round cutouts), the cups are trimmed circular. For the three mouth cutouts, they're trimmed into different shapes. Heat-shrink tubing on the LED leads keeps the wires from shorting against the foil — if you skip this and metal makes contact, you'll get random behavior at best and a damaged LED at worst.

## Installing Energia

The Energia IDE is a 159 MB download from energia.nu. On Windows, installation is drag-and-drop — unzip the archive and move the resulting folder to wherever you put applications. No installer required. The first time you launch it, expect about 10 minutes to unpack everything if your machine is older.

Once it's open, go to `Tools → Board` and select the MSP-430 G2553 — that's the chip included with the standard Launchpad. If you have a different Launchpad or chip, select accordingly; the IDE supports a range of MSP-430 variants.

Pin numbering in Energia matches the physical pin numbers printed on the Launchpad silkscreen. If you're looking at the board and the silkscreen says "P1.3", that maps to a specific Energia pin number on the pin-out reference at energia.nu. For this project, we're using pins 2 through 7, which are straightforward.

## The code

Start by setting all the LED pins as outputs and initializing them low. Leaving pins floating or in an unknown state at power-on can cause LEDs to all turn on at once — not the behavior you want when you're trying to figure out which pin maps to which LED.

```cpp
void setup() {
  for (int i = 2; i < 8; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
}
```

**Testing individual pins** before writing the final code is worth the extra five minutes. Write a pin HIGH, upload, see which LED lights up, note it, move on. The transcript for this video runs through exactly that process: pin 2 = left eye, pin 3 = right eye, pin 4 = nose, pin 5 = right mouth, pin 6 = left mouth, pin 7 = middle mouth.

Once the pin mapping is confirmed, write two helper functions — `allOn()` and `allOff()`:

```cpp
void allOn() {
  for (int i = 2; i < 8; i++) {
    digitalWrite(i, HIGH);
  }
}

void allOff() {
  for (int i = 2; i < 8; i++) {
    digitalWrite(i, LOW);
  }
}

void loop() {
  allOn();
  delay(100);
  allOff();
  delay(100);
}
```

At 100 ms on/off, the whole pumpkin flashes at 5 Hz — clearly visible but not seizure-inducing. Drop it to 50 ms and it starts to feel more like a strobe.

## The flickering candle effect

The allOn/allOff approach is a starting point. The more interesting version — the one that looks like a candle — uses randomized delays and independent control of each LED:

```cpp
void loop() {
  for (int i = 2; i < 8; i++) {
    digitalWrite(i, random(2));   // randomly HIGH or LOW
    delay(random(20, 80));
  }
}
```

This isn't a physically accurate candle simulation, but it reads as one at a glance — the random mix of on/off across the six LEDs and the varied timing between updates produces the right kind of irregular flicker. Adding biased random values (more likely to be HIGH than LOW) keeps the pumpkin mostly lit rather than mostly dark.

## The MSP-430 vs. Arduino question

The MSP-430 G2553 runs at 3.3V and has a significantly lower sleep-mode power draw than the ATmega328P in an Uno. For a battery-powered project like a pumpkin that might need to run for a full Halloween night on AA batteries, that matters. The Launchpad's power consumption in active mode is also lower than an Uno's, which means a battery pack lasts longer.

In terms of what you can do with it in Energia versus Arduino IDE — for a project like this, there's no practical difference. The API is the same, the libraries overlap substantially, and the GPIO behavior is identical for simple digital output. The MSP-430 line becomes distinctly interesting for battery-powered and sleep-mode applications, which is a deeper topic for another post.

For a pumpkin that's going to be plugged in all night, either platform works. The Launchpad's advantage here is that it's a good excuse to try a TI chip in a low-stakes project before reaching for one in something more serious.

## References and further reading

- [TI MSP-430 G2553 datasheet](https://www.ti.com/lit/ds/symlink/msp430g2553.pdf) — Texas Instruments; full peripheral and electrical specs
- [Energia IDE download and documentation](https://energia.nu/) — includes pin reference diagrams for each supported Launchpad
- [Energia on GitHub](https://github.com/energia/Energia) — source code and issue tracker
- [MSP-430 Launchpad getting started guide](https://www.ti.com/lit/ug/slau318g/slau318g.pdf) — TI's official quickstart documentation
- [TI MSP-430 LaunchPad product page](https://www.ti.com/tool/MSP-EXP430G2ET) — current version of the Launchpad; under $10 directly from TI
- [LED current-limiting resistor calculator](https://www.hobby-hour.com/electronics/ledcalc.php) — for adapting this circuit to different LED colors or supply voltages
