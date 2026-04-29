---
title: 'Arduino Random LED Flasher — Teaching Your Arduino to Be Unpredictable'
description: 'A quick intro to Arduino random number generation via a simple multi-LED flasher. Covers random(), randomSeed(), and why seeding from analog noise matters for true unpredictability.'
pubDate: 'January 8 2012'
youtubeId: 'bmwnppmdFwY'
heroImage: '../../assets/posts/arduino-random-led-flasher/thumbnail.jpg'
tags: ['arduino', 'leds', 'tutorial', 'beginner', 'random']
---

*This project is from early 2012, back when the channel was still MeanPC.com — same workbench, same Arduino, just a different name on the channel.*

There's something almost philosophically interesting about asking a deterministic machine to behave randomly. The Arduino's processor executes instructions in a perfectly predictable sequence, yet a handful of lines of code can make a row of LEDs flash in a pattern that looks — and for most practical purposes, *is* — genuinely unpredictable. The random LED flasher is one of the first projects where the software does something visually interesting without any physical input, and it's a great excuse to understand how `random()` and `randomSeed()` actually work.

This post covers the build behind the video: eight LEDs wired to Arduino digital pins, flashing in a random sequence that's different every time the board powers up.

## What you'll need

- Arduino Uno (or any Arduino with enough digital pins)
- 8 LEDs — color doesn't matter for the concept, but a mix makes it more visually interesting
- 8 resistors, 220Ω each
- Half-size breadboard
- Jumper wires

Total cost is under $5 if you're pulling from a component drawer. The resistor math: with a 5V supply and a typical LED forward voltage of about 2V, you need (5 − 2) / 0.02 = 150Ω minimum. 220Ω gives you a slightly dimmer LED but plenty of headroom and good protection for the Arduino's I/O pins.

## The circuit

Wire each LED's anode (long leg) through a 220Ω resistor to one of Arduino pins 3 through 10. Connect all cathodes (short legs) to GND. That's the whole circuit — eight independent LEDs, each controllable from a single digital output pin. Pins 3 and up keep you away from the hardware serial pins (0 and 1), which saves headaches if you want to add `Serial.println()` for debugging later.

## The code

```cpp
int leds[] = {3, 4, 5, 6, 7, 8, 9, 10};
int numLeds = 8;

void setup() {
  randomSeed(analogRead(A0));  // seed from analog noise
  for (int i = 0; i < numLeds; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  int pin = leds[random(numLeds)];  // pick a random LED
  digitalWrite(pin, HIGH);
  delay(random(50, 300));           // on for a random duration
  digitalWrite(pin, LOW);
  delay(random(20, 150));           // off for a random gap
}
```

Two things here are worth understanding properly, because they show up constantly in Arduino projects.

### `random()` — pseudo-random, not truly random

`random(max)` returns a number from 0 up to (but not including) `max`. `random(min, max)` gives you a number from `min` up to (but not including) `max`. The Arduino documentation is clear that this is a *pseudo-random* number generator — it produces a sequence that statistically looks random but is entirely deterministic. Given the same starting state, it will produce the same sequence every single time.

That starting state is called the seed. And here's the trap beginners run into: if you don't call `randomSeed()` before your first `random()` call, the seed defaults to 1 every power-up. Same seed, same sequence. Your "random" flasher will flash in exactly the same order every time you plug in the Arduino — not random at all, just predictably weird.

### `randomSeed(analogRead(A0))` — pulling entropy from noise

The standard fix is to seed the PRNG with something that varies from run to run. `analogRead(A0)` reads the voltage on analog pin A0 — and if nothing is connected to A0, that pin is floating. A floating analog pin picks up electrical noise from the environment: capacitive coupling from nearby traces, RF interference, thermal noise in the input circuitry. The reading jumps around unpredictably between power cycles, giving you a different seed each time.

It's not cryptographically secure entropy, but for making LEDs flash differently every time you plug the board in, it works perfectly. Just make sure A0 is actually disconnected — if something is tied to A0, you'll get a consistent reading and lose the randomness.

## The result

With this code running, the eight LEDs flash in a pattern that varies both in which LED lights up and how long each on/off cycle lasts. There's no obvious repetition, no rhythmic pattern the eye can latch onto. It looks alive in a way that a deterministic blink pattern never quite does.

## Where this goes next

The random flasher is a building block. The same `random()` / `randomSeed()` pattern shows up in:

- **Generative sound** — randomly selecting notes from a scale to produce ambient music (combine with a piezo buzzer or audio shield)
- **Games** — dice rolls, card draws, procedural level generation
- **Simulations** — randomized sensor data for testing, Brownian motion displays
- **Decorative lighting** — candle flicker effects, firefly simulations, randomly pulsing ambient lights

The key insight from this project is that "random" in a microcontroller context almost always means "seeded pseudo-random," and the quality of your seed determines whether your randomness holds up across power cycles. For most maker projects, analog noise is a perfectly adequate seed. For anything security-sensitive, you'd want a dedicated hardware RNG — but that's a different class of problem than blinking LEDs.

If you want to dig deeper into how Arduino's PRNG works, it uses a Lehmer linear congruential generator — simple, fast, and predictable enough that the sequence can be fully reproduced from the seed. Which is occasionally useful: if you seed two Arduino boards with the same value, they'll produce identical "random" sequences, which opens up some interesting synchronized-lighting possibilities.

## References and further reading

- [Arduino `random()` documentation](https://www.arduino.cc/reference/en/language/functions/random-numbers/random/) — the official reference, including the note about `randomSeed()` being required for true unpredictability
- [Arduino `randomSeed()` documentation](https://www.arduino.cc/reference/en/language/functions/random-numbers/randomseed/) — covers the analog noise seeding approach
- [Linear congruential generator | Wikipedia](https://en.wikipedia.org/wiki/Linear_congruential_generator) — the math behind the PRNG Arduino uses
- [Secrets of Arduino PWM | Ken Shirriff](https://www.righto.com/2009/07/secrets-of-arduino-pwm.html) — not directly about random(), but excellent background on how Arduino timer-based functions work
- [Arduino Forum: random LED blink code](https://forum.arduino.cc/t/random-led-blink-code-check/106834) — community discussion of common variations and gotchas
