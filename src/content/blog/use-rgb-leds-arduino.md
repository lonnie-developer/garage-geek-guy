---
title: 'How to Use RGB LEDs with Arduino'
description: 'RGB LEDs pack three LEDs into one package and unlock the full color spectrum with PWM. This post covers the hardware, wiring, and three progressively interesting sketches to get you mixing colors.'
pubDate: 'November 09 2018'
youtubeId: '5kgv9SC6Qjg'
heroImage: '../../assets/posts/use-rgb-leds-arduino/thumbnail.jpg'
tags: ['arduino', 'led', 'pwm', 'tutorial', 'beginner']
---

A standard LED is either on or off, and it's one color. That's useful for indicator lights but not for much else. An RGB LED is three LEDs in a single package — red, green, and blue — sharing a common ground leg. Mix those three primaries with PWM and you can hit any color in the visible spectrum, from a clean white to a deep purple to that muddy yellow-green that happens when you accidentally leave all three pots turned up halfway.

This post walks through what an RGB LED actually is, how to wire it up with and without a breakout module, and three sketches that go from "light up one color" to "random color strobe" to "control with potentiometers."

## What's inside the package

If you look closely at an RGB LED — the kind in a 5mm clear housing — you can see there are actually three tiny emitters in there sharing a lens. The four legs are labeled R, G, B, and a common cathode (the minus sign, the longest leg). All three emitters share that one ground connection. To light just red, you apply voltage to the R leg and leave G and B at zero. To get white, you drive all three to maximum.

The physics of what makes different LED colors are worth knowing: red LEDs have the lowest forward voltage (around 2.0–2.2 V), green sits around 2.0–3.5 V depending on the exact emitter, and blue and violet LEDs have the highest forward voltage at 2.8–3.5 V. This is why blue often appears slightly dimmer than the others at the same PWM value — it needs more voltage to reach full brightness, and you're working against that with a fixed 5 V supply. If your white looks slightly bluish or yellowish, this is why.

## Module vs. standalone

The video uses a RGB LED module from the Elegoo 37-sensor kit, which has three built-in 150 Ω SMD resistors — one per channel. That means you wire it directly to the Arduino without adding your own resistors. Convenient.

If you're using a standalone RGB LED from a bag of parts, you need three current-limiting resistors, one in series with each anode. The standard choice is 220 Ω, though anywhere from 150–330 Ω works. Going lower gives you more brightness; going higher drops intensity and reduces your color accuracy (the channels respond less evenly).

## Wiring

For either version, the connections are:
- Red anode → digital pin 9 (through 220 Ω resistor if standalone)
- Green anode → digital pin 10 (through 220 Ω resistor if standalone)
- Blue anode → digital pin 11 (through 220 Ω resistor if standalone)
- Common cathode → GND

Pins 9, 10, and 11 on the Arduino Uno are all PWM-capable (marked with a `~` on the board). This matters — if you use non-PWM pins you can only turn each channel fully on or off, which gives you eight colors instead of a continuous spectrum. The PWM pins let you set any value from 0 to 255 on each channel, which is how you mix.

## Sketch 1: solid colors

The simplest demonstration. Define the pin numbers as global variables, then `analogWrite` a value to each channel. Zero is off, 255 is full brightness.

```cpp
int redPin   = 9;
int greenPin = 10;
int bluePin  = 11;

void setup() {
  // nothing needed — analogWrite doesn't require pinMode on Uno
}

void loop() {
  // Just red
  analogWrite(redPin,   255);
  analogWrite(greenPin,   0);
  analogWrite(bluePin,    0);
}
```

Swap in different values to get other colors. A few useful references:
- `255, 0, 0` → red
- `0, 255, 0` → green
- `0, 0, 255` → blue
- `255, 255, 255` → white (or close to it)
- `255, 0, 255` → purple
- `255, 255, 0` → yellow-green (it won't look quite like you expect)

The color mixing isn't perceptually linear — human eyes are more sensitive to green than red or blue, so equal PWM values don't look equally bright. If you want a precise color, look up its RGB values and plug those in directly.

## Sketch 2: random colors

Seed the random number generator off an unconnected analog pin (a common trick — the floating pin reads electrical noise, which gives you a different seed each reset), then cycle through random RGB combinations every 300 milliseconds.

```cpp
int redPin   = 9;
int greenPin = 10;
int bluePin  = 11;

void setup() {
  randomSeed(analogRead(A3));  // floating analog pin for entropy
}

void loop() {
  analogWrite(redPin,   random(256));
  analogWrite(greenPin, random(256));
  analogWrite(bluePin,  random(256));
  delay(300);
}
```

The 300 ms delay is a reasonable starting point. Shorten it to 100 ms for a frantic strobe effect; stretch it to 1000 ms or more for a slow ambient mood lamp. This sketch is a good sanity check that all three channels are working — if one color never appears or always stays dim, that channel has a wiring issue.

## Sketch 3: potentiometer control

Three 10 kΩ potentiometers, one per channel, let you dial in any color by hand. The pots' outer legs go to +5 V and GND; the center wiper goes to analog pins A0, A1, and A2. `analogRead` returns a value from 0 to 1023, so you use `map()` to scale it down to 0–255 for `analogWrite`.

```cpp
int redPot   = A0;
int greenPot = A1;
int bluePot  = A2;

int redPin   = 9;
int greenPin = 10;
int bluePin  = 11;

void loop() {
  analogWrite(redPin,   map(analogRead(redPot),   0, 1023, 0, 255));
  analogWrite(greenPin, map(analogRead(greenPot), 0, 1023, 0, 255));
  analogWrite(bluePin,  map(analogRead(bluePot),  0, 1023, 0, 255));
}
```

This is a satisfying way to explore the color space by hand. If you add an LCD or print the values to the Serial Monitor, you can record what dial positions produce a color you like — useful if you're trying to reproduce a specific hue in code later.

## The gotcha: common cathode vs. common anode

RGB LEDs come in two varieties. Common cathode (what this post covers) has all three cathodes tied together to GND, and you drive each anode HIGH to turn that color on. Common anode is the mirror image — all anodes share a positive rail (usually 5 V or 3.3 V), and you pull each cathode LOW to turn that color on.

If you wire a common-anode LED as if it were common cathode, everything will appear inverted: 255 will turn a channel off and 0 will turn it on. The quick test is to put 255 on one channel and leave the others at 0. If the other two colors light up instead of the one you specified, you have a common-anode LED and need to invert your logic (or use `255 - value` in every `analogWrite` call).

## Where this goes next

The potentiometer sketch is a practical prototype for anything that needs dynamic color control: status indicators, mood lighting, a visual signal that maps to a sensor reading. The next natural steps from here are driving the RGB LED from sensor data instead of pots, or moving to an addressable LED strip like the WS2812B (commonly sold as NeoPixels) which packs the control logic directly into each LED and lets you drive long chains of them from a single Arduino pin.

## References

- [Arduino `analogWrite()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)
- [Arduino `map()` reference](https://www.arduino.cc/reference/en/language/functions/math/map/)
- [Arduino `random()` and `randomSeed()` reference](https://www.arduino.cc/reference/en/language/functions/random-numbers/random/)
- [Elegoo 37-sensor kit (Amazon)](https://www.amazon.com/s?k=elegoo+37+sensor+kit) — the module used in the video
- [PWM tutorial — Arduino documentation](https://docs.arduino.cc/learn/microcontrollers/analog-output/)
