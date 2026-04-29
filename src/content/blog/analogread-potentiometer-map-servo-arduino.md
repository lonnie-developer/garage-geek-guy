---
title: 'How to Arduino #4 — analogRead, Potentiometers, and map() to Control a Servo'
description: 'A potentiometer outputs a voltage between 0V and 5V. The Arduino reads it as a number between 0 and 1023. map() converts that to 0–180 for a servo. This post covers the theory, the wiring, and the one-line conversion that ties it all together.'
pubDate: 'November 23 2013'
youtubeId: 'xWjkuYSQcoI'
heroImage: '../../assets/posts/analogread-potentiometer-map-servo-arduino/thumbnail.jpg'
tags: ['arduino', 'analogread', 'potentiometer', 'servo', 'map', 'tutorial']
---

Digital signals are either high or low, on or off, 1 or 0. Analog signals are everything in between. The Arduino's digital pins can toggle an LED, read a button, and communicate over serial — but they can't sense the position of a dial or the temperature of a room. For that, you need the analog input pins and the `analogRead()` command.

This post covers the complete path from physical knob to servo position: how a potentiometer works, what `analogRead()` returns, and how `map()` converts a 0–1023 reading into the 0–180 degrees a servo understands.

## How a potentiometer works

A potentiometer is a variable resistor. Inside is a strip of resistive material arranged in an arc, with a wiper that slides along it as you turn the knob. Three pins come out: two ends of the resistive strip and the wiper.

Connect one end to GND and the other to 5V. The wiper then reads a voltage between 0V and 5V depending on its position — at one extreme, 0V; at the other, 5V; in the middle, 2.5V. This is a resistor divider: the wiper taps a fraction of the voltage proportional to how far it's traveled along the strip.

It doesn't matter which outer pin gets GND and which gets 5V — swapping them just reverses the direction of travel. What does matter is that the **center (wiper) pin** connects to the Arduino analog input. That's the one we're actually reading.

The resistance value of the potentiometer doesn't matter much for this application. A 10 kΩ pot is the standard choice, but a 100 kΩ pot works fine. What you're measuring is a voltage ratio, and the total resistance cancels out of the math. Very high resistance values (1 MΩ+) can introduce noise, so stay below that.

## analogRead() — the 10-bit ADC

The Arduino Uno has six analog input pins: **A0 through A5**. They're labeled with an "A" prefix on the board and shown with tilde (~) marks in some diagrams. These pins have a built-in 10-bit analog-to-digital converter (ADC): they sample the voltage on the pin and return a number from **0 to 1023**.

- 0V → 0
- 2.5V → ~512
- 5V → 1023
- 3V → approximately 614 (3 / 5 × 1023)

The mapping is linear across the 0–5V input range. You don't need to call `pinMode()` for analog pins when using them as inputs — `analogRead()` handles the configuration automatically.

```cpp
int potValue = analogRead(A5);  // returns 0–1023
```

## The map() function

The servo library's `write()` command accepts angles from 0 to 180 degrees. Our ADC gives us 0 to 1023. These ranges don't match, but `map()` handles the conversion:

```cpp
int mapped = map(potValue, 0, 1023, 0, 180);
```

`map(value, fromLow, fromHigh, toLow, toHigh)` performs a linear interpolation: it takes `value` from the input range `[fromLow, fromHigh]` and maps it proportionally to the output range `[toLow, toHigh]`. A pot reading of 511 maps to about 89 degrees. A reading of 1023 maps to exactly 180.

The output range doesn't have to be 0–180. `map(potValue, 0, 1023, 0, 255)` gives you a 0–255 brightness value for PWM. `map(potValue, 0, 1023, 500, 2400)` gives microsecond pulse widths for direct servo control. The function is useful anywhere you need to rescale one numeric range to another.

## Wiring

**Servo** (external power supply required — see [servo external power post](/blog/servo-external-power-supply-arduino) for why):

- Orange (signal) → Arduino D7
- Red (power) → external 5–6V supply
- Brown (GND) → external supply GND, also tied to Arduino GND

**Potentiometer:**

- One outer pin → Arduino 5V
- Other outer pin → Arduino GND
- Center pin (wiper) → Arduino A5

**Common ground:** the external supply's GND and the Arduino GND must be connected. This is what makes the servo's signal line intelligible — without a shared ground reference, the PWM waveform has no meaningful reference point.

## The sketch

```cpp
#include <Servo.h>

Servo servo1;
const int potPin = A5;
const int servoPin = 7;

void setup() {
  servo1.attach(servoPin);
  pinMode(potPin, INPUT);
}

void loop() {
  int pot    = analogRead(potPin);
  int mapped = map(pot, 0, 1023, 4, 176);
  servo1.write(mapped);
  delay(15);
}
```

The range is 4–176 rather than 0–180. Most hobby servos handle the theoretical extremes badly — at 0 and 180 they may buzz, vibrate, or draw extra current while straining against their mechanical limits. Pulling back a few degrees on each end eliminates this without any noticeable loss of range.

The `delay(15)` gives the servo time to physically move to its commanded position before the next reading. Without it, the loop runs so fast that rapid pot movements send commands faster than the servo can follow, causing erratic behavior.

## Beyond the potentiometer

Once `analogRead()` makes sense with a pot, substituting other sensors is straightforward. A thermistor changes resistance with temperature — put it in a voltage divider and `analogRead()` gives you temperature-correlated numbers. A photoresistor (LDR) does the same for light. A flex sensor for bend angle. A force-sensitive resistor for pressure. The Arduino sees all of them the same way: a voltage on an analog pin, a number between 0 and 1023, then `map()` or custom math to extract a meaningful value.

That's the power of `analogRead()` — it turns the entire world of resistive sensors into a common interface.

## References and further reading

- [Arduino `analogRead()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) — the 10-bit resolution, 5V reference, and A0–A5 pin notes
- [Arduino `map()` reference](https://www.arduino.cc/reference/en/language/functions/math/map/) — includes the important caveat that `map()` does not constrain output values; see `constrain()` if the input can go out of range
- [Arduino Servo library reference](https://www.arduino.cc/reference/en/libraries/servo/) — `attach()`, `write()`, and `writeMicroseconds()`
- [Resistor divider networks (All About Circuits)](https://www.allaboutcircuits.com/textbook/direct-current/chpt-6/voltage-divider-circuits/) — the theory behind how a potentiometer (and any resistive sensor in a divider) produces a voltage
- [Arduino analog input tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInput) — the official built-in example using a potentiometer and LED
