---
title: 'Arduino Potentiometer Tutorial — Build an LED Volume Bar with analogRead + map()'
description: 'Turn a potentiometer into a 19-LED volume bar indicator — a hands-on intro to analogRead, the map() function, and the for-loop pattern every analog Arduino project needs.'
pubDate: 'November 03 2018'
youtubeId: 'xXFc9G0Ydno'
heroImage: '../../assets/posts/arduino-potentiometer-led-volume-bar/thumbnail.jpg'
tags: ['arduino', 'potentiometer', 'analog', 'led', 'tutorial', 'beginner']
---

There's a function in the Arduino standard library called `map()` that most beginners either ignore or misuse for the first few months. It looks intimidating — five arguments, oddly named, not obvious what it actually does — and a lot of tutorials just show you the one-liner without explaining the underlying math.

The potentiometer LED volume bar is the project that makes `map()` click. You've got a knob that produces a number from 0 to 1023. You've got 19 LEDs. You need to convert the first into the second in a way that feels natural — more knob means more lit LEDs, less knob means fewer. Once you solve that with `map()`, you'll use that pattern in every analog project you build afterward.

This post walks through the wiring, the theory behind `analogRead()`, and the complete code — including the one bug that trips up every first-time builder.

## What a potentiometer actually is

A potentiometer is a three-terminal variable resistor. Two outer pins connect to the voltage rails — one to 5V, one to GND. The center pin (called the wiper) reads somewhere between those two voltages depending on where the shaft is turned. Rotate the knob fully toward the 5V end and the wiper reads close to 5V. Rotate it toward GND and it reads close to 0V. Anywhere in between gives you a proportional value.

Electrically this is a [voltage divider](https://en.wikipedia.org/wiki/Voltage_divider) — the resistive track inside the pot acts as two resistors in series, and the wiper taps off the midpoint. The ratio of the two resistances (which changes as you turn the knob) determines the output voltage. It's simple, robust, and almost impossible to wire wrong once you understand the three-pin layout.

The internal resistance of a typical potentiometer is 10 kΩ end-to-end. When you're doing analog reads, that value doesn't matter much — what matters is the ratio, and the Arduino's ADC just reads voltage.

## How analogRead() turns voltage into a number

The Arduino's analog input pins connect to a 10-bit analog-to-digital converter (ADC). When you call `analogRead(A5)`, the ADC measures the voltage on that pin and converts it to an integer from 0 to 1023 — 0 at 0V, 1023 at 5V, and everything in between scaled linearly. A reading of 512 means the pin is sitting at approximately 2.5V, which means your potentiometer shaft is roughly centered.

So when the wiper is all the way counterclockwise, you get 0. All the way clockwise, you get 1023. The knob translates directly to a number in that range.

The catch: 0–1023 is not a useful range by itself. What you actually want is 0–18, so you can use that value to control 19 LEDs. That's where `map()` earns its keep.

## The map() function

```cpp
int potti = map(analogRead(A5), 0, 1023, 0, 18);
```

`map()` takes five arguments: the input value, the low end of the input range, the high end of the input range, the low end of the output range, and the high end of the output range. It does the proportional math and returns a value scaled into the output range.

In this case: take whatever `analogRead(A5)` returns (0–1023), treat 0 as the low end and 1023 as the high end, and rescale it so that 0 → 0 and 1023 → 18. A reading of 511 comes back as approximately 9. A reading of 200 comes back as approximately 3. The function handles the fractional math and truncates to an integer.

One thing `map()` does *not* do: clamp the output to the target range. If analogRead somehow returns above 1023 (it shouldn't, but noise happens), `map()` will return a value above 18. For this project that's not a real concern — the ADC is internally limited — but it's worth knowing for projects where the input range is less tightly bounded.

## The wiring

The potentiometer gets three connections:

- One outer pin → Arduino 5V
- Other outer pin → Arduino GND
- Center wiper pin → Arduino A5

The 19 LEDs run on digital pins 0–13 and analog pins A0–A4 (used as digital outputs). Pin A5 is reserved for the potentiometer, so it sits out of the LED array. That gives you pins 0 through 18 for LEDs — 19 total, if you count.

There's nothing exotic about wiring an analog pin as a digital output. You just call `pinMode(A0, OUTPUT)` in setup(), same as you would for a digital pin, and then `digitalWrite(A0, HIGH)` to drive it. The Arduino handles the translation internally.

## The code

```cpp
void setup() {
  for (int i = 0; i <= 18; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  int potti = map(analogRead(A5), 0, 1023, 0, 18);

  // Light LEDs up to the current pot value
  for (int i = 0; i <= potti; i++) {
    digitalWrite(i, HIGH);
  }

  // Turn off LEDs above the current pot value
  for (int i = potti + 1; i <= 18; i++) {
    digitalWrite(i, LOW);
  }
}
```

The setup() loop configures all 19 pins as outputs in one shot — a `for` loop instead of 19 individual `pinMode()` calls. In the main loop, the `map()` call converts the pot reading to 0–18 and stores it in `potti`. The first for-loop lights everything from pin 0 up to and including the current value. The second for-loop turns everything above that value off.

## The bug — and why you need that second for-loop

Here's the one that catches everyone on the first pass. If you only write the first for-loop — the one that lights LEDs up to the pot value — the indicator works fine when you turn the knob clockwise. LEDs light up as the knob goes up. 

Turn the knob back down and the LEDs stay lit. All of them.

The reason is that `digitalWrite(i, HIGH)` doesn't do anything to the other pins. If you set pins 0 through 15 high, and then the next loop iteration only sets 0 through 12 high, pins 13–15 are still high from the previous iteration — there was nothing to turn them off.

The second for-loop fixes this. It starts at `potti + 1` (the first LED above the current level) and sets everything from there to pin 18 LOW. Together, the two loops create a complete state update every time through the main loop: up to `potti` is HIGH, above `potti` is LOW. Turn the knob in either direction and the display tracks it correctly.

This two-loop pattern — one to set the active range, one to clear the inactive range — shows up constantly in LED bar and progress indicator code. Worth understanding it once, cleanly.

## Arduino capitalization gotchas

The Arduino IDE's case-sensitivity bites beginners more than almost anything else. A few things to double-check in this sketch:

`pinMode` — lowercase 'p', uppercase 'M'. `OUTPUT`, `HIGH`, and `LOW` — all caps, all three of them. If you write `output` or `high`, the IDE will throw an error that says something like "'output' was not declared in this scope," which is technically accurate but not especially helpful when you're staring at what looks like perfectly correct code.

If a sketch looks right but won't compile, a slow read of every keyword against the [Arduino language reference](https://www.arduino.cc/reference/en/) is usually the fastest path to the bug.

## What this unlocks

The skills in this project — `analogRead()`, `map()`, and the for-loop LED pattern — are the foundation for a long list of more complex builds. Servo control with a potentiometer is the most obvious next step: you substitute a servo write for the LED bank, and the same `map()` pattern converts knob position to servo angle. Motor speed control with an H-bridge is the same idea again. Any time you're converting a physical knob position into a useful range of numbers, you're doing this.

The project in the video uses a 37-in-1 sensor kit potentiometer, which is the little blue trimmer-style pot that comes in most beginner Arduino kits. A panel-mount potentiometer (the kind with a D-shaped shaft meant for a knob) wires exactly the same way — same three pins, same connections — and gives you a more satisfying tactile experience if you want to build this into an enclosure.

## References and further reading

- [Arduino analogRead() reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/)
- [Arduino map() reference](https://www.arduino.cc/reference/en/language/functions/math/map/)
- [SparkFun: Reading a Potentiometer](https://learn.sparkfun.com/tutorials/sik-experiment-guide-for-arduino---v32/experiment-2-reading-a-potentiometer) — good beginner walkthrough with circuit diagrams
- [Wikipedia: Voltage divider](https://en.wikipedia.org/wiki/Voltage_divider) — the math behind why the pot output is linear
- [Arduino Language Reference](https://www.arduino.cc/reference/en/) — bookmark this; it's faster than Stack Overflow for the basics
- [MakeabilityLab: Potentiometers and Physical Computing](https://makeabilitylab.github.io/physcomp/arduino/potentiometers.html) — deeper dive into ADC behavior and sensor noise
