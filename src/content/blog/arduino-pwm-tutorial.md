---
title: 'How to Use PWM on the Arduino — analogWrite() with Two Practical Examples'
description: 'PWM lets the Arduino fake analog output using a fast digital square wave. This post covers how it works, which pins support it, and two hands-on examples: a fading LED and a potentiometer-controlled dimmer.'
pubDate: 'November 05 2018'
youtubeId: 'kBkEGMbSClo'
heroImage: '../../assets/posts/arduino-pwm-tutorial/thumbnail.jpg'
tags: ['arduino', 'pwm', 'analogwrite', 'led', 'tutorial']
---

The Arduino Uno has 14 digital I/O pins. Every one of them can do exactly two things: output 5V or output 0V. That's the constraint — it's a digital device, and digital means on or off. But if all you can output is full-on and full-off, how do you dim an LED, control motor speed, or generate a smooth analog-looking signal?

The answer is pulse-width modulation. PWM doesn't produce a true analog voltage — nothing in the Uno's hardware can do that. What it does instead is switch a pin on and off so fast that the average voltage over time lands wherever you want it. At 50% duty cycle the pin is high half the time and low the other half, and a device attached to it sees something close to 2.5V. At 25% duty cycle it sees something close to 1.25V. Your multimeter in DC mode will read these intermediate values as if they were real analog voltages, because the switching happens far faster than the meter can respond.

## How it works under the hood

The Arduino Uno's PWM runs at approximately 490 Hz on most pins (pins 5 and 6 run at ~980 Hz due to a different timer configuration). At 490 Hz, one complete on/off cycle takes about 2 milliseconds. Within that 2-millisecond window, the pin is held high for some fraction of the time and low for the rest. That fraction is the duty cycle.

The command that controls this is `analogWrite()`, which takes two arguments: the pin number and a value from 0 to 255. Zero means 0% duty cycle (always off, 0V effective). 255 means 100% duty cycle (always on, 5V). 128 lands at roughly 50% — about 2.5V effective.

```cpp
analogWrite(9, 128);   // ~50% duty cycle → ~2.5V effective
analogWrite(9, 64);    // ~25% duty cycle → ~1.25V effective
analogWrite(9, 255);   // 100% duty cycle → 5V effective
analogWrite(9, 0);     // 0% duty cycle → 0V
```

The hardware handles the switching automatically via built-in timers — you don't need to toggle anything in your loop. One call to `analogWrite()` sets it and leaves it running until you call it again with a different value.

## Which pins support PWM

Not every digital pin on the Uno can do PWM. Look at the board and you'll see a tilde (~) printed next to six of them: **3, 5, 6, 9, 10, and 11**. Those six are the ones wired to the internal timer hardware. Any call to `analogWrite()` needs to go to one of those pins — calling it on pin 7 or pin 12 won't produce a PWM signal, it'll just set the pin high or low.

```
Digital pins with PWM (~):  3  5  6  9  10  11
Digital pins without PWM:   0  1  2  4  7   8  12  13
```

## Example 1: fading LED

The simplest thing you can do with PWM is ramp an LED up and down. Wire an LED through a 150Ω resistor from pin 9 to ground, then upload this:

```cpp
void setup() {
  // nothing needed — analogWrite doesn't require pinMode
}

void loop() {
  // ramp up: 0 → 255
  for (int i = 0; i <= 255; i++) {
    analogWrite(9, i);
    delay(8);
  }

  // ramp down: 255 → 0
  for (int i = 255; i >= 0; i--) {
    analogWrite(9, i);
    delay(8);
  }
}
```

The two `for` loops increment and then decrement `i`, passing the current value to `analogWrite()` each time. The `delay(8)` between steps slows the ramp down to something visible — at 8ms per step the full fade takes about 2 seconds. Drop it to 2ms for a faster pulse, raise it to 20ms for a slow, theatrical breath effect.

One note: `analogWrite()` doesn't require a `pinMode()` call to work. The Uno handles the direction setting internally. You *can* call `pinMode(9, OUTPUT)` first and it doesn't hurt anything, but it's not required.

## Example 2: potentiometer-controlled dimmer

The second example connects a potentiometer to the LED so you can manually dial brightness. The potentiometer gives an analog reading from 0 to 1023 (on the Uno's 10-bit ADC), and `analogWrite()` wants a value from 0 to 255. The `map()` function bridges that gap.

Wire the potentiometer with one outer leg to 5V, the other outer leg to GND, and the center wiper leg to analog pin A5. The LED with its 150Ω resistor stays on pin 9.

```cpp
void loop() {
  analogWrite(9, map(analogRead(A5), 0, 1023, 0, 255));
}
```

That single line reads the pot, maps the result, and writes the brightness — all in one statement. Turn the pot one way and the LED brightens; turn it back and it dims. That's a complete single-component dimmer in about eight words of code.

The `map()` function signature is worth memorizing because you'll use it constantly:

```cpp
map(value, fromLow, fromHigh, toLow, toHigh)
```

It does linear interpolation between two ranges. `analogRead()` produces 0–1023, `analogWrite()` wants 0–255, and `map()` converts between them without any math on your part.

## Where PWM shows up beyond LEDs

Dimming is the obvious use case because the effect is immediately visible. But the same principle drives motor speed control — the L298N motor driver covered in another post on this channel takes a PWM signal on its ENA/ENB pins and uses it to regulate current to the motor. Higher duty cycle, faster motor.

Servos use PWM too, but in a different way. Rather than duty cycle controlling analog voltage, servo PWM uses pulse *width* at a fixed frequency (50 Hz) to communicate a position. 1ms pulse = full one direction, 2ms pulse = full other direction, 1.5ms = center. The Arduino `Servo` library handles all the timing so you don't think about it, but that's what's happening underneath.

The important limitation to know is that PWM is not a true DAC (digital-to-analog converter). It works fine for LED brightness and motor speed because those devices respond to average power, not instantaneous voltage. Audio applications need a proper DAC or at minimum a low-pass filter on the PWM output, otherwise the 490 Hz carrier frequency ends up in the signal.

## The gotcha: pins 5 and 6 running at double frequency

Most guides don't mention this. Pins 5 and 6 share Timer 0, which also drives `millis()` and `delay()`. To keep those time functions accurate, Timer 0 runs at double the frequency of Timer 1 and Timer 2 — so pins 5 and 6 output PWM at ~980 Hz instead of ~490 Hz. For most applications (LED dimming, motor speed) this doesn't matter. But if you're using PWM to produce audio or feeding a signal to something that's frequency-sensitive, keep the 980 Hz pins in mind and route to 3, 9, 10, or 11 instead.

## References and further reading

- [Arduino Reference — analogWrite()](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/) — official documentation
- [Arduino Tutorial: PWM Basics](https://www.arduino.cc/en/Tutorial/PWM) — the canonical beginner explainer on arduino.cc
- [Secrets of Arduino PWM](https://www.arduino.cc/en/Tutorial/SecretsOfArduinoPWM) — timer configuration, custom frequencies, the full technical picture
- [SparkFun: PWM Output on Arduino](https://cdn.sparkfun.com/assets/resources/4/4/PWM_output_Arduino.pdf) — condensed reference PDF
- [Arduino Reference — map()](https://www.arduino.cc/reference/en/language/functions/math/map/) — map() function docs, including the note about integer truncation
- [L298N Motor Driver with PWM](https://www.arduino.cc/en/Tutorial/LibraryExamples/MotorKnob) — extending PWM to motor speed control
