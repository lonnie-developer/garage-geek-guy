---
title: 'Build a Breadboard Music Keyboard with Arduino and the switch/case Statement'
description: 'Eight pushbuttons, eight musical notes, one piezo speaker, and one new statement: switch/case. A fun one-hour project that introduces tone(), note frequency lookup, the D0/D1 pin gotcha, and why you need to reset currentTone to zero at the top of every loop.'
pubDate: 'November 08 2018'
youtubeId: 'fPEt0eh4fFE'
heroImage: '../../assets/posts/arduino-music-keyboard-breadboard/thumbnail.jpg'
tags: ['arduino', 'sound', 'tone', 'switch-case', 'beginner', 'project', 'tutorial']
---

This is one of those projects that takes about an hour, makes a satisfying noise when it works, and teaches a handful of things that come up again and again in real Arduino sketches. Eight pushbuttons wired to eight digital inputs, a speaker on a PWM pin, and the `switch/case` statement tying it all together. Press a button, play a note.

The whole thing fits on a single breadboard and uses parts from any basic Arduino kit. The code is short enough to walk through completely, and the one bug that showed up during development — a mysterious erratic pin — turns out to be a useful lesson about the hardware serial interface.

## What you'll need

- Arduino Uno or compatible
- 8 momentary pushbuttons
- 8× 10K resistors (pulldown, one per button)
- 1 piezo speaker or small speaker (the speaker used here is from a Snap Circuits kit and has an internal current-limiting resistor; if yours doesn't, add a 100–220Ω series resistor)
- Breadboard and jumper wire

## The wiring

**Buttons:** Each button bridges across two breadboard rows. One leg goes to the Arduino digital input through a yellow signal wire. The other leg connects to 5V. A 10K pulldown resistor connects the signal leg to GND. When the button is open, the pin reads LOW (pulled down to ground). When pressed, 5V flows through the button to the input, reading HIGH.

This is the standard active-high button circuit. Wire all eight buttons the same way, with signal lines going to digital pins D3 through D10.

**Why D3–D10 and not D0–D7?** The short answer: D0 and D1 are the Arduino's hardware serial RX and TX pins. During development one of the buttons was originally wired to D1, and it was erratic — flickering HIGH even when not pressed, impossible to stabilize with different resistors or different wiring. Moved to D3 and the problem vanished. The likely cause is that D1 is driven by the USB serial interface while a sketch is running with `Serial.begin()` active, causing interference on the pin. D2 is generally safe but this layout skips it to keep the button group contiguous on D3–D10.

**Speaker:** The speaker's positive terminal connects to D11 (a PWM-capable pin — required for `tone()`). The other terminal goes to GND. If your speaker doesn't have an internal resistor, add a 100–220Ω resistor in series on the positive lead to limit current.

## The code

```cpp
const int speakerPin = 11;
const int delayValue = 100;  // ms to hold note after button release

void setup() {
  for (int i = 3; i <= 10; i++) {
    pinMode(i, INPUT);
    digitalWrite(i, LOW);  // explicit LOW — belt-and-suspenders
  }
  pinMode(speakerPin, OUTPUT);
}

void loop() {
  int currentTone = 0;  // reset every loop — critical

  // Read all buttons; last one pressed wins
  for (int i = 3; i <= 10; i++) {
    if (digitalRead(i) == HIGH) {
      currentTone = i;
    }
  }

  switch (currentTone) {
    case 3:  tone(speakerPin, 262); delay(delayValue); break;  // C4
    case 4:  tone(speakerPin, 294); delay(delayValue); break;  // D4
    case 5:  tone(speakerPin, 330); delay(delayValue); break;  // E4
    case 6:  tone(speakerPin, 349); delay(delayValue); break;  // F4
    case 7:  tone(speakerPin, 392); delay(delayValue); break;  // G4
    case 8:  tone(speakerPin, 440); delay(delayValue); break;  // A4
    case 9:  tone(speakerPin, 494); delay(delayValue); break;  // B4
    case 10: tone(speakerPin, 523); delay(delayValue); break;  // C5
    default: noTone(speakerPin); break;
  }
}
```

## How `switch/case` works

`switch` evaluates `currentTone` and jumps to the matching `case`. The `break` at the end of each case exits the switch block — without it, execution would fall through to the next case. The `default` case runs when no button is pressed (`currentTone` stayed at 0), which calls `noTone()` to silence the speaker.

This structure is more readable than a chain of `if/else if` statements when you have multiple discrete values to handle, and it compiles to more efficient machine code on AVR processors.

## Why `currentTone` must reset to 0 at the top of `loop()`

The first draft of this sketch didn't reset `currentTone`. It would work — barely — but had a noticeable bug: after pressing a button and releasing it, the speaker would keep playing the last note instead of going silent. The issue is that `currentTone` is declared inside `loop()`, which means it's recreated on every iteration, but if you move the declaration outside `loop()` for any reason, the bug shows up clearly: the variable retains its previous value across loop iterations, so the last button pressed never stops playing.

Resetting to 0 at the top of every loop guarantees that if no button is currently pressed, `currentTone` hits the `default` case and the speaker stops.

## Note frequencies

The values passed to `tone()` are frequencies in Hz. These are the standard equal-temperament values for one octave starting at middle C:

| Button | Pin | Note | Frequency |
|--------|-----|------|-----------|
| 1 | D3 | C4 | 262 Hz |
| 2 | D4 | D4 | 294 Hz |
| 3 | D5 | E4 | 330 Hz |
| 4 | D6 | F4 | 349 Hz |
| 5 | D7 | G4 | 392 Hz |
| 6 | D8 | A4 | 440 Hz |
| 7 | D9 | B4 | 494 Hz |
| 8 | D10 | C5 | 523 Hz |

A4 at 440 Hz is the standard tuning reference (the A above middle C). The rest follow from equal temperament, where each semitone is a factor of 2^(1/12) ≈ 1.0595 higher than the previous.

## The `delayValue` variable

One hundred milliseconds was added as a hold time after a button is read. Without it, releasing a button and moving to the next one cuts the previous note very abruptly. The 100ms carry-over smooths the transition between notes.

Setting `delayValue` as a named variable at the top rather than hardcoding `100` in all eight `delay()` calls is worth doing even in a short sketch. It's the same argument as using a named constant for any value that appears more than once: change it once at the top, it changes everywhere.

## Where to take it next

The natural extensions from here: add sharp/flat notes by adding more buttons (D2 and D11–D13 are available), play pre-programmed songs by reading frequencies and durations from an array, or replace the polling loop with interrupts so notes respond immediately rather than waiting for `loop()` to come around. The [Arduino `tone()` reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) has the full API including simultaneous tones on multiple pins.

## References and further reading

- [Arduino `tone()` reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) — frequency range, PWM pin requirement, and `noTone()`
- [Arduino `switch/case` reference](https://www.arduino.cc/reference/en/language/structure/control-structure/switchcase/) — syntax, fall-through behavior, and `break` usage
- [Musical note frequencies table](https://pages.mtu.edu/~suits/notefreqs.html) — Michigan Tech's reference for the full piano keyboard in Hz; the source for the values in this sketch
- [Arduino digital pin reference](https://www.arduino.cc/en/Tutorial/Foundations/DigitalPins) — covers D0/D1 serial pin caveats, pull-up/pull-down considerations
- [Arduino `digitalRead()` reference](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/) — including the floating-pin behavior that makes pulldown resistors necessary
- [Piezo speaker vs. passive buzzer](https://www.electronics-tutorials.ws/blog/buzzer.html) — explains why `tone()` works with a passive buzzer/speaker but not an active buzzer
