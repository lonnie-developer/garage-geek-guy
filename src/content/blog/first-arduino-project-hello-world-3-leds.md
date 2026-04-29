---
title: "First Arduino Project: Modifying Hello World to Blink 3 LEDs"
description: 'The classic Arduino Hello World blinks one LED. What happens when a first-timer decides to add two more? A quick tour through variables, wiring, and a bug that teaches more than the working version ever would.'
pubDate: 'December 27 2011'
youtubeId: '5iWGrYklgxw'
heroImage: '../../assets/posts/first-arduino-project-hello-world-3-leds/thumbnail.jpg'
tags: ['arduino', 'beginner', 'led', 'tutorial', 'blink']
---

The Hello World program for Arduino blinks an LED. It has been the first sketch almost every Arduino owner runs, and for good reason — the whole chain works or it doesn't, and if it works you know your board is alive, your USB cable isn't garbage, and your IDE is configured correctly. One blinking LED, and everything is verified.

But one LED is a little boring.

This video is from the day after Christmas 2011 — the Arduino arrived as a gift, the book (*Arduino: A Quick Start Guide* by Maik Schmidt) got opened right along with it, and by the afternoon the Hello World project was already done and feeling too easy. So we modified it to blink three LEDs. What followed was a short, instructive trip through the two things that bite every beginner: wiring more than one output, and debugging a logic error you're sure you didn't make.

> *This build is from 2011, when the channel was still MeanPC.com — same garage, same bench, just a different name on the screen.*

## What the original sketch does

The Hello World sketch that ships with the Arduino IDE blinks the onboard LED on pin 13. The book's version does the same thing but with an external LED: one `LED_BUILTIN`-equivalent variable, one `pinMode` call in `setup()`, and then a `loop()` that goes high, waits, goes low, waits, repeat. Clean and minimal.

To add a second and third LED, the logic extends straightforwardly — but you have to touch five different places in the sketch to do it right, and the IDE won't tell you if you miss one.

## What you'll need

- Arduino Uno (or any basic Arduino board)
- 3 LEDs — any color
- Three **1 kΩ resistors** (one per LED; protects them from the Arduino's 5 V output)
- Breadboard
- Jumper wires
- *Arduino: A Quick Start Guide* if you want to follow the same starting point, or just the Arduino IDE's built-in Blink example

## Wiring

Each LED gets its own current-limiting resistor in series with the anode (positive leg — the longer one). The cathode (negative leg, shorter) goes to the breadboard's negative rail, which ties to Arduino GND. The resistor connects the anode side to the Arduino digital pin.

The three pins used in the video are **12, 8, and 10** — chosen partly for breadboard convenience. Any digital output pins work; the resistor math doesn't change.

```
Arduino pin 12  →  1kΩ resistor  →  LED1 anode  →  LED1 cathode  →  GND
Arduino pin  8  →  1kΩ resistor  →  LED2 anode  →  LED2 cathode  →  GND
Arduino pin 10  →  1kΩ resistor  →  LED3 anode  →  LED3 cathode  →  GND
Arduino GND     →  breadboard negative rail
```

The 1 kΩ value is conservative — you'll get dim but safe output from a 5 V Arduino. For brighter LEDs, drop to 470 Ω or 220 Ω, but never go below about 68 Ω on a standard 20 mA LED without checking the math first.

## The code

The Hello World sketch uses a single variable and repeats the same three calls for one LED. For three LEDs, you add two more variables and duplicate the `pinMode` and the `digitalWrite`/`delay` pairs:

```cpp
int ledPin = 12;
int led2Pin = 8;
int led3Pin = 10;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);

  digitalWrite(led2Pin, HIGH);
  delay(500);
  digitalWrite(led2Pin, LOW);
  delay(500);

  digitalWrite(led3Pin, HIGH);
  delay(500);
  digitalWrite(led3Pin, LOW);
  delay(500);
}
```

The IDE will catch missing semicolons. It will not catch a missing `pinMode` call, a wrong pin number, or a swapped `HIGH`/`LOW`. Those you have to find yourself.

## The gotcha: one LED stayed on too long

The first upload didn't quite work right. LED2 appeared to stay on longer than the others — it seemed to be on while LED3 was also trying to come on. The bug was in the ordering of the `HIGH` and `LOW` calls for LED2.

In the copy-paste process, LED2's sequence ended up as:

```cpp
digitalWrite(led2Pin, LOW);   // it starts low (off)
delay(500);
digitalWrite(led2Pin, HIGH);  // turns on
delay(500);
```

...instead of the intended:

```cpp
digitalWrite(led2Pin, HIGH);  // turns on
delay(500);
digitalWrite(led2Pin, LOW);   // turns off
delay(500);
```

The `HIGH` and `LOW` were transposed. LED2 was spending most of its time off, then turning on right as LED3 was starting its cycle — which looked like two LEDs on simultaneously. The fix was a one-word swap. Once corrected, the sequence ran cleanly: LED1 blinks, then LED2, then LED3, in order, one at a time.

After that, the delay got dropped from 500 ms to 100 ms, which sped up the sequence enough to look like a chase effect instead of a slow roll. A good place to leave it.

## Why this matters beyond "blink more LEDs"

This kind of debug — "it almost works, but one thing is slightly off in a way that looks like a wiring problem" — is where most real troubleshooting time goes, at every level. The instinct is to look at the breadboard first. In this case the wiring was fine; the bug was in the code, and specifically in the ordering of two lines that the compiler had no complaint about.

Getting comfortable with that kind of ambiguity early is worth more than any single circuit. The LEDs blinked correctly in the end. More importantly, the debugging process ran to completion: identify what's actually wrong (not what you think is wrong), change the minimum thing needed to fix it, verify the fix works, then optionally go back and optimize.

That's the whole loop, in nine minutes, on day one with an Arduino.

## References and further reading

- [Arduino Blink tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink) — the official starting point, updated for current IDE versions
- [Arduino digital I/O reference](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/) — `digitalWrite`, `pinMode`, `HIGH`/`LOW` explained
- [LED current-limiting resistor calculator](https://www.hobby-hour.com/electronics/ledcalc.php) — for when you want more brightness or different supply voltages
- *Arduino: A Quick Start Guide* by Maik Schmidt — still a solid beginner book, and the source of the Hello World project used here
