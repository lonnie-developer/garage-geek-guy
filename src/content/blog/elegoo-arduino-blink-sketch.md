---
title: 'Arduino Blink Sketch — Elegoo Starter Kit Lesson 2'
description: 'The Blink example does one thing — flash an LED — but its real job is proving your IDE is installed, your board is recognized, and your upload path works. Here is the walkthrough, the delay variable, and what to do when uploads fail.'
pubDate: 'October 26 2019'
youtubeId: 'Kus2liJqhcE'
heroImage: '../../assets/posts/elegoo-arduino-blink-sketch/thumbnail.jpg'
tags: ['arduino', 'elegoo', 'beginner', 'blink', 'tutorial']
---

Blink is the simplest possible Arduino sketch. It flashes the LED on pin 13 on for one second, off for one second, forever. There's nothing useful happening. That's the point.

The Arduino Uno already has a blinking LED by default from the factory sketch — so if yours is already blinking when you plug it in, you haven't actually done anything yet. The exercise is to open the Blink example yourself, upload it, then deliberately break the timing to prove you understand what changed. Once you've done that, you know your IDE is configured, your port is set correctly, and the full compile-and-upload path is working. Every project after this builds on exactly that confidence.

## Loading and uploading the example

In the Arduino IDE: **File → Examples → 01.Basics → Blink**. This opens the sketch in the editor. Don't modify anything yet.

Click the **upload button** (the right-arrow icon, or Ctrl+U / Cmd+U). The IDE compiles first — you'll see the progress bar at the bottom and a message about the compiled size — then transfers the sketch to the board. The TX and RX LEDs near the USB connector will flicker during the transfer. When it's done you'll see "Done uploading."

If the upload succeeds, the LED on the board labeled "L" (near pin 13) should be blinking at one-second intervals. That means the full path works: IDE → compiler → serial port → Arduino.

## What the code does

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // LED on
  delay(1000);                       // wait 1000 ms = 1 second
  digitalWrite(LED_BUILTIN, LOW);   // LED off
  delay(1000);                       // wait 1000 ms = 1 second
}
```

`LED_BUILTIN` is a constant the IDE defines as pin 13 for the Uno — you can also just write `13` and it works the same. `delay()` takes a value in **milliseconds**: `delay(1000)` is one second, `delay(100)` is one tenth of a second, `delay(5000)` is five seconds.

## Changing the blink rate

This is the actual lesson: find the two `delay(1000)` lines and change both to `delay(100)`. Upload again. The LED should blink ten times faster.

Try `delay(30)`. Upload. At this point the LED blinks so fast that the eye can barely track it — it looks more like a dim steady glow than a flash. Somewhere around 20–30ms the flicker rate exceeds what the human visual system resolves cleanly. This is the same principle behind PWM LED dimming: switch fast enough and the eye averages out the on/off cycle into a perceived brightness.

Try `delay(5000)`. Upload. Now it blinks once every five seconds — noticeably slow enough to be useful for status indicators where you don't want a frantic flash.

## When uploads fail

Upload failures with a fresh Elegoo kit on Windows are usually one of two things:

**Wrong port selected:** Tools → Port — if you see multiple COM ports, try a different one. Unplug the Arduino, check which ports disappear from the list, and that tells you which one belongs to the board.

**Driver not installed:** Windows sometimes needs the CH340 USB-to-serial driver that most clone Arduinos use. If the board doesn't appear in Device Manager under "Ports (COM & LPT)" at all after plugging in, download and install the CH340 driver manually. The Elegoo kit usually includes a driver CD, but downloading the latest version from the web is more reliable.

**Mac quirks:** Mac historically required more manual driver installation for CH340-based boards than Windows. If uploads fail on Mac and the port shows up but the upload hangs or errors out, the CH340 driver from a reliable source (Sparkfun's guide is a good reference) usually fixes it.

Once Blink is working reliably, the IDE setup is done. Lesson 3 picks up with actual components on the breadboard.

## References and further reading

- [Arduino Blink tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink) — the canonical walkthrough with notes on `LED_BUILTIN` across different board types
- [Arduino `delay()` reference](https://www.arduino.cc/reference/en/language/functions/time/delay/) — covers milliseconds, blocking behavior, and the `millis()` alternative for non-blocking timing
- [CH340 driver install guide (Sparkfun)](https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all) — the most thorough walkthrough for Mac and Windows CH340 driver issues
- [Arduino IDE 2.x download](https://www.arduino.cc/en/software) — the current IDE version; includes an improved board manager and built-in serial plotter
