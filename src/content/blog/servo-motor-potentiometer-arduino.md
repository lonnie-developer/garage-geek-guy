---
title: 'Control a Servo Motor with a Potentiometer Using Arduino map()'
description: 'Wire a 10K potentiometer and an SG90 servo to an Arduino and write a single line of code that maps knob position to servo angle. A clean demonstration of analogRead, map(), and the Servo library working together.'
pubDate: 'November 03 2018'
youtubeId: 'qgDuHWnDFZI'
heroImage: '../../assets/posts/servo-motor-potentiometer-arduino/thumbnail.jpg'
tags: ['arduino', 'servo', 'potentiometer', 'map', 'tutorial', 'beginner']
---

There's a particular satisfaction to turning a knob and watching something physical respond in real time. It's not a complicated project, but it's the kind of thing that makes the relationship between code and hardware feel immediate — you move your hand, something moves across the room. No delay, no interpretation layer, just an analog signal translated into motor position.

This post wires a 10K potentiometer and a 9-gram micro servo to an Arduino and writes the code to make one control the other. The whole sketch fits in one line of code inside `loop()`, which is either impressive or a little alarming depending on how you feel about nested function calls.

## What you'll need

- Arduino Uno or compatible (~$6-7 for a knockoff from a US eBay seller)
- TowerPro SG90 9-gram micro servo (cheap in bulk on eBay — [a pack of 4 TowerPro SG90s](https://www.ebay.com/sch/i.html?_nkw=sg90+servo+4+pack) runs about $8)
- 10K potentiometer (the trimpot style or panel-mount, either works)
- Mini breadboard
- Jumper wire — male-to-male; the SG90 has a female connector at the end of its lead, so use male-to-male to bridge from the servo to the breadboard or Arduino headers

## Understanding the translation problem

Here's the core of what the code has to do. The potentiometer's output, read with `analogRead()`, returns a value between 0 and 1023 — that's the full 10-bit range of the Arduino's ADC. The servo motor, controlled through the `Servo` library's `.write()` method, takes a value between 0 and 180, representing degrees of rotation.

Those two ranges don't match. You can't feed 1023 to a servo expecting 180. You need something in between that translates one range to the other — scaling 0–1023 down to 0–180 proportionally, so that the midpoint of the pot (511 or so) lands the servo at 90°, and the ends of the pot land it at 0° and 180°.

That translation is exactly what `map()` does.

## Wiring

The Arduino Uno has two 5V pins and two ground pins on the same header, which means you can power both the potentiometer and the servo directly from the board without needing a breadboard for power distribution — though having a mini breadboard makes the potentiometer connections easier to manage.

**Servo connections:**
- Brown wire → GND
- Red wire → 5V
- Orange wire → digital pin 8 (signal)

The SG90's color coding is a little counter-intuitive if you're used to electronics conventions. Brown is ground, not red. Red is power. Orange is signal. Some SG90s have a slightly different color scheme (black/red/yellow is also common), but the order — ground, power, signal — stays the same across the product line.

**Potentiometer connections:**
- One outer leg → 5V
- Other outer leg → GND
- Center wiper → analog pin A4

Which outer leg gets 5V and which gets GND determines which direction "more clockwise" maps to. Either way works; it just sets whether turning the knob clockwise increases or decreases the reading. Pick one, and if the servo moves backward relative to the knob, swap the two outer wires.

## The code

```cpp
#include <Servo.h>

Servo blueServo;

void setup() {
  blueServo.attach(8);
}

void loop() {
  blueServo.write(map(analogRead(A4), 0, 1023, 0, 180));
}
```

That's it. The whole functional sketch — library include, servo declaration, attach, and the complete control loop — is eight lines including blanks.

The `loop()` line works from the inside out:

1. `analogRead(A4)` reads the potentiometer — returns 0 to 1023
2. `map(reading, 0, 1023, 0, 180)` scales that value — returns 0 to 180
3. `blueServo.write(angle)` moves the servo to that angle

The `map()` function is one of the most useful things in the Arduino library. Its signature is `map(value, fromLow, fromHigh, toLow, toHigh)` — give it a value, tell it the input range and the output range, and it does the proportional scaling. It's not limited to servo control; anywhere you're reading a sensor and using the result to set something with a different scale, `map()` is the right tool.

One thing to know: `map()` does integer arithmetic. The output is an integer, not a float. For most applications — including servo control — that's fine. Where it matters is at very small output ranges, where the rounding can cause steps rather than smooth transitions.

## What to expect

When you upload and power everything up, turning the pot knob should move the servo. The range might not be exactly 0° to 180° — the SG90 is specified at approximately 180° total travel, but in practice it varies slightly between units. If your servo physically hits its mechanical limits before the pot reaches its ends, change the output range in `map()` from `0, 180` to something like `5, 175`.

Cheap servos jitter. The SG90 at the lower end of the eBay price range will vibrate slightly even when stationary, especially near the center of its range. This isn't a code problem — it's the controller board hunting around its target position. Higher-quality servos (Hitec, Futaba, genuine TowerPro rather than clones) have tighter tolerances and less jitter. For many applications the SG90 jitter is fine; if you're building something that needs to hold position smoothly, it's worth spending more on the servo.

## Why this pattern shows up everywhere

Pot-to-servo is the "hello world" of analog-to-actuator control, but the pattern it demonstrates — read an analog input, map it to a different range, write it to an output — is the core of a huge category of projects: dimming an LED with a knob, controlling a fan speed from a temperature sensor, adjusting a stepper motor speed from a joystick. Once `map()` clicks, a lot of other projects become straightforward.

The one-line compound statement in `loop()` is also worth understanding on its own terms. Nested function calls like this feel tricky at first, but the IDE helps — in the Arduino IDE, when you close a parenthesis, it briefly highlights the matching open parenthesis so you can see which call you just closed. That visual feedback is how you check that the nesting is correct without counting by hand.

## References and further reading

- [Arduino `map()` reference](https://www.arduino.cc/reference/en/language/functions/math/map/) — official docs, including the integer-arithmetic caveat and examples
- [Arduino `Servo` library reference](https://www.arduino.cc/reference/en/libraries/servo/) — `.attach()`, `.write()`, `.read()`, and the rest of the API
- [TowerPro SG90 datasheet](http://www.towerpro.com.tw/product/sg90-7/) — spec sheet for the servo; torque, speed, and pulse-width range
- [Arduino `analogRead()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) — explains the 10-bit ADC, reference voltage, and how to read analog inputs
- [Arduino potentiometer tutorial](https://docs.arduino.cc/built-in-examples/basics/AnalogReadSerial/) — the official analog input tutorial using a pot and the serial monitor
- [Servo sweep example (Arduino built-in)](https://docs.arduino.cc/learn/electronics/servo-motors/) — the standard auto-sweep example to test a servo with no other hardware
