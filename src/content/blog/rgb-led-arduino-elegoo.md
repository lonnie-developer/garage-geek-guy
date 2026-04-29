---
title: 'How to Use an RGB LED with Arduino — Elegoo Kit Lesson 4'
description: 'An RGB LED is three LEDs in one package sharing a common cathode. PWM on three separate pins controls the color mix. Here is the pin layout, the 220Ω resistors, the PWM-only pin requirement, and the Elegoo sketch that cycles through colors.'
pubDate: 'October 27 2019'
youtubeId: 'vxIJ59XR6r8'
heroImage: '../../assets/posts/rgb-led-arduino-elegoo/thumbnail.jpg'
tags: ['arduino', 'led', 'rgb', 'pwm', 'elegoo', 'beginner', 'tutorial']
---

A standard LED has two legs: anode and cathode. An RGB LED has four: one cathode shared by all three colors, and three separate anodes — one each for red, green, and blue. Each color channel behaves exactly like an individual LED, which means each needs its own current-limiting resistor and its own Arduino pin. The payoff is that by mixing those three channels at different intensities, you can produce a wide palette of colors from a single component.

This is lesson 4 in the Elegoo Arduino kit series. The circuit is simple — three PWM outputs, three 220 Ω resistors, and one RGB LED — but it introduces `analogWrite()` and pulse-width modulation, which show up constantly in more complex projects.

## The RGB LED pinout

The four legs are easy to identify. The **longest leg is the common cathode** — it goes to GND. The other three, arranged around the cathode, are the color anodes. In the most common through-hole RGB LEDs:

- Leg to the left of the cathode: **Red**
- Leg second-left: **Green** (with cathode between them)
- Leg to the right of the cathode: **Blue**

When in doubt, check the datasheet for your specific LED — pin ordering can vary between manufacturers. A quick test: put 3.3V through a 220 Ω resistor to each leg in turn and the color it lights tells you which is which.

## The wiring

Each anode leg gets its own 220 Ω resistor in series, then connects to a PWM-capable Arduino pin. The cathode goes directly to GND.

| RGB LED leg | Resistor | Arduino pin |
|-------------|----------|-------------|
| Red | 220 Ω | D6 |
| Green | 220 Ω | D5 |
| Blue | 220 Ω | D3 |
| Cathode (longest) | — | GND |

**Why D3, D5, D6 — and why skip D4?** PWM on the Arduino Uno is only available on certain pins: D3, D5, D6, D9, D10, and D11. These are marked with a tilde (~) on the board silkscreen. D4 doesn't have a tilde — it's a plain digital pin that can only output HIGH or LOW, not a PWM signal. Using a non-PWM pin for a color channel means that color is either fully on or fully off, with no brightness control in between.

## How PWM controls brightness and color

`analogWrite(pin, value)` doesn't output a true analog voltage. Instead it rapidly switches the pin between HIGH and LOW at about 490–980 Hz, with the duty cycle — the fraction of each cycle spent HIGH — proportional to the value: 0 is always off, 255 is always on, 128 is 50% duty cycle. The LED can't respond fast enough to see the flicker, so it appears as a dimmer version of full brightness.

To mix colors, you set each channel's duty cycle independently. Red at 255, green and blue at 0 gives pure red. Red at 0, green at 255, blue at 0 gives pure green. Red at 255, green at 255, blue at 0 gives yellow. All three at the same value gives white (or warm gray at lower intensities). The full 24-bit RGB color space works this way.

## The Elegoo sketch

The kit's lesson 4 sketch fades through colors by incrementing and decrementing the red, green, and blue values in a loop:

```cpp
const int redPin   = 6;
const int greenPin = 5;
const int bluePin  = 3;

int redVal   = 255;
int greenVal = 0;
int blueVal  = 0;

int fadeDelay = 5;  // ms between each step

void setup() {
  pinMode(redPin,   OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin,  OUTPUT);
}

void loop() {
  // Red → Yellow (increase green)
  for (int i = 0; i < 255; i++) {
    greenVal++;
    analogWrite(redPin,   redVal);
    analogWrite(greenPin, greenVal);
    analogWrite(bluePin,  blueVal);
    delay(fadeDelay);
  }

  // Yellow → Green (decrease red)
  for (int i = 0; i < 255; i++) {
    redVal--;
    analogWrite(redPin,   redVal);
    analogWrite(greenPin, greenVal);
    analogWrite(bluePin,  blueVal);
    delay(fadeDelay);
  }

  // Green → Cyan (increase blue)
  for (int i = 0; i < 255; i++) {
    blueVal++;
    analogWrite(redPin,   redVal);
    analogWrite(greenPin, greenVal);
    analogWrite(bluePin,  blueVal);
    delay(fadeDelay);
  }

  // Continue cycling...
}
```

The colors cycle through red → yellow → green → cyan → blue → magenta → red. Each transition takes 255 steps × 5 ms = about 1.3 seconds. Reducing `fadeDelay` speeds up the cycle; increasing it slows it down.

## What to try next

Once the basic cycle is working, the interesting variations are easy to explore. Set all three channels to the same value (`analogWrite(redPin, x); analogWrite(greenPin, x); analogWrite(bluePin, x)`) and increase x from 0 to 255 — the LED fades from off to white. Try fixed color recipes: `(255, 165, 0)` is orange, `(128, 0, 128)` is purple, `(0, 255, 127)` is spring green. The Elegoo documentation PDF includes a color chart with a full set of values worth bookmarking.

PWM shows up again in motor speed control (`analogWrite` to a motor driver's enable pin), display dimming, buzzer frequency modulation, and more. Learning to think about `analogWrite` as "set duty cycle to N/255" rather than "output voltage X" is the mental model that makes the rest of those applications click.

## References and further reading

- [Arduino `analogWrite()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/) — covers the 0–255 range, PWM frequency, and which pins support it on each board
- [Arduino PWM tutorial](https://www.arduino.cc/en/Tutorial/Foundations/PWM) — explains the duty cycle / effective voltage relationship with diagrams
- [RGB color chart (W3Schools)](https://www.w3schools.com/colors/colors_rgb.asp) — interactive RGB value picker; useful for finding target colors to reproduce
- [Arduino Uno PWM pins reference](https://docs.arduino.cc/hardware/uno-rev3) — the full pin map showing which pins carry the ~ PWM marker
