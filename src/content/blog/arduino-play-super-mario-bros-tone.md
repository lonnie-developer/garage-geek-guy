---
title: 'Arduino: Play the Super Mario Bros Theme with tone()'
description: "Arduino's built-in tone() function is all you need to play melodies — no libraries, no shield, just a speaker and a few lines of code. This post covers the basics and gets the Mario Bros theme running on your board."
pubDate: 'November 06 2018'
youtubeId: 'BsepLU5xlsc'
heroImage: '../../assets/posts/arduino-play-super-mario-bros-tone/thumbnail.jpg'
tags: ['arduino', 'audio', 'tone', 'tutorial', 'beginner']
---

There's a particular satisfaction in hearing a microcontroller play a recognizable melody. Not because it's a practical project — it usually isn't — but because it proves you understand how to sequence time-sensitive outputs, which is a foundational skill that shows up in everything from debouncing buttons to driving stepper motors. The Super Mario Bros theme is the "Hello, World" of Arduino audio.

This post covers the `tone()` and `noTone()` functions, the hardware you need to get sound out of an Arduino, and how to wire it up so the full overworld theme plays on your board.

## The hardware: speaker vs. piezo buzzer

You can use either a small speaker or a piezo buzzer, but they're not equally pleasant to listen to. A piezo buzzer is cheap and easy, but its sound is physically painful at higher frequencies — think the cry of a smoke alarm — and it can't reproduce low frequencies at all. If you only have a piezo, it'll work; you'll just want to turn it down or close a drawer.

A small 8 Ω, 0.5 W speaker sounds dramatically better. The one used in the video came from a Snap Circuits kit — the snaps were cut off and the bare leads plugged into a breadboard. That's $0 if you have an old Snap Circuits set, or roughly $2–3 for a small hobby speaker from eBay or Amazon.

**Resistor:** If your speaker doesn't have a built-in resistor (the Snap Circuits version does — there's a small component embedded in the lead), add a 330 Ω resistor in series between the Arduino pin and the positive speaker lead. Skipping it won't immediately destroy anything, but it shorts the PWM output harder than the datasheet prefers.

**Connection:** one lead to digital pin 3 (PWM, marked with `~`), the other lead through the resistor to GND. The tone function needs a PWM-capable pin — pins 3, 5, 6, 9, 10, and 11 all work on the Uno.

## tone() and noTone()

The `tone()` function is part of the Arduino standard library. No `#include` needed — it's there automatically.

```cpp
tone(pin, frequency);          // play indefinitely
tone(pin, frequency, duration); // play for `duration` milliseconds, then stop
noTone(pin);                   // stop playback
```

Frequency is in hertz. The human hearing range is roughly 20 Hz to 20 kHz, but small speakers reproduce the middle of that range much better than the extremes. This quick sketch runs through a few reference frequencies so you can hear how they compare:

```cpp
void setup() {}

void loop() {
  tone(3, 200);   delay(1000);
  tone(3, 400);   delay(1000);
  tone(3, 1000);  delay(1000);
  tone(3, 2000);  delay(1000);
  tone(3, 4000);  delay(1000);
  tone(3, 10000); delay(1000);
  noTone(3);      delay(1000);
}
```

The 200 Hz tone is a low rumble that small speakers struggle to reproduce well. By 10,000 Hz it's a high-pitched whine; 20,000 Hz is essentially inaudible on most speakers and at the edge of most people's hearing. The sweet spot for a melody is 200–4000 Hz — comfortably in the range where notes are recognizable.

## Playing a melody: how it works

To play a song you need two things: a list of pitches (frequencies, in Hz) and a list of durations (how long each note plays). Arduino sketches for the Mario theme typically use a `pitches.h` header file that defines human-readable note names — `NOTE_E5`, `NOTE_C5`, `NOTE_G4`, etc. — as their corresponding frequencies. You include that header, define your melody and durations as arrays, then loop through both arrays calling `tone()` with a small pause between notes.

The standard Arduino [Tone melody example](https://www.arduino.cc/en/Tutorial/BuiltInExamples/toneMelody) in the IDE (File → Examples → 02.Digital → toneMelody) shows the pattern clearly. The full Mario overworld theme follows the same structure, just with a much longer melody array.

A well-maintained version of the full overworld theme — and the underworld theme — is available at [PrinceTronics](https://www.princetronics.com/supermariothemesong/). It's public domain, the code is clean, and it works directly on an Uno with a speaker on pin 3.

The key lines from the melody-playing loop look like this:

```cpp
for (int thisNote = 0; thisNote < notes; thisNote++) {
  int noteDuration = 1000 / tempo[thisNote];
  tone(melodyPin, melody[thisNote], noteDuration);
  // add ~30% gap between notes so they're audible as distinct pitches
  int pauseBetweenNotes = noteDuration * 1.30;
  delay(pauseBetweenNotes);
  noTone(melodyPin);
}
```

That 30% pause is the detail that makes the melody intelligible. Without it, adjacent notes of the same pitch blur together into a single long tone.

## The gotcha: tone() blocks while playing (sort of)

When you call `tone(pin, freq, duration)` with a duration, the tone plays out and then stops — but your code keeps running immediately. The delay after it is what makes everything line up. If you skip the delay between notes, you're firing off the next `tone()` call before the speaker has finished the previous one, and the melody turns into noise.

The `tone()` function also uses Timer 2 on the Uno. This means it conflicts with `analogWrite()` on pins 3 and 11 — those pins share Timer 2. If you're also trying to PWM an LED on pin 3 or 11 while playing audio, use a different pin for the LED. Pins 5, 6, 9, and 10 use different timers and won't interfere.

## Where to go from here

Once you've got the Mario theme playing, the natural next step is building a rudimentary keyboard — a few pushbuttons, each wired to a different pitch, so you can play notes on demand. From there the `tone()` function is powerful enough to drive a simple alarm system, a countdown beep sequence, or any project where audio feedback beats blinking an LED.

The full frequency table in `pitches.h` covers notes from B0 (31 Hz) all the way up to D#8 (4978 Hz) — enough range for almost any melody you'd want to reproduce.

## References

- [PrinceTronics — Super Mario Bros theme for Arduino](https://www.princetronics.com/supermariothemesong/) — the cleanest version of the full overworld + underworld code
- [Arduino tone() reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/)
- [Arduino noTone() reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/notone/)
- [Arduino built-in example: toneMelody](https://www.arduino.cc/en/Tutorial/BuiltInExamples/toneMelody) — includes the `pitches.h` file and explains the note-duration pattern
- [Instructables: Arduino Mario Bros Theme Song](https://www.instructables.com/Arduino-Mario-Bros-Theme-Song/) — step-by-step with wiring photos
- [Hackster.io: Super Mario Theme with Piezo Buzzer](https://www.hackster.io/techarea98/super-mario-theme-song-with-piezo-buzzer-and-arduino-2cc461)
