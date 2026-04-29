---
title: 'How to Power a Servo Motor from an External Supply with an Arduino'
description: 'An SG90 micro servo can stall at 650 mA — over 30 times what an Arduino I/O pin can safely provide. Here is why you need an external power supply for any servo, how to wire one, and the one connection that makes it work: common ground.'
pubDate: 'August 01 2021'
youtubeId: 'xHXVufb5AkQ'
heroImage: '../../assets/posts/servo-external-power-supply-arduino/thumbnail.jpg'
tags: ['arduino', 'servo', 'power-supply', 'tutorial', 'electronics']
---

The quickest way to understand why servos need their own power supply is to look at the numbers. An Arduino's I/O pin is rated for a maximum of 20 mA continuous output. The SG90 micro servo — the small, cheap, 9-gram servo that ends up in almost every beginner project — can draw up to 650 mA at stall. That's more than 30 times the pin's limit.

A stall happens whenever the servo is resisting movement against a load: when it's at the end of its travel, when something is pushing back against it, or even when it's holding a position against gravity on a heavier-than-expected arm. In a real application, stalls happen regularly. Asking an Arduino I/O pin to supply that current will eventually damage the pin, reset the board, or both.

Even in a no-load condition — servo spinning freely — the SG90 draws more than a pin should handle. The fix is straightforward: power the servo from a separate supply, use the Arduino only for the signal wire, and tie the grounds together.

## What you need

- SG90 servo (or any servo — the principle is the same regardless of size)
- Arduino Uno or compatible
- External power supply capable of 5V at 1A or more — options include:
  - A breadboard power supply module (the kind that plugs into a breadboard and accepts a 9V barrel jack; typically rated 1A per rail)
  - A 4× or 6×AA battery pack (delivers 6V or 9V; use a regulator or pick the right cell count for your servo's voltage range)
  - A bench power supply set to 5V
- Jumper wire

The SG90 is rated for 4.8–6V. Most small servos fall in the 4.8–7.2V range. Check your specific servo's datasheet before applying power.

## The wiring

The SG90 has a three-wire lead. The wire colors vary slightly between brands, but the order — ground, power, signal — is consistent:

- **Brown** (sometimes black) → Ground
- **Red** → Power (4.8–6V from your external supply)
- **Orange** (sometimes yellow or white) → Signal → Arduino digital pin 9

Connect the servo's brown wire to your external supply's GND rail. Connect the red wire to your external supply's 5V (or appropriate voltage) rail. Connect the orange signal wire to Arduino pin 9.

**Then add the critical connection:** a wire from your external supply's GND rail to one of the Arduino's GND pins. This brings both grounds to the same potential.

```
External Supply GND  ──────────┬──── Servo brown (GND)
                               │
                               └──── Arduino GND

External Supply 5V   ──────────────── Servo red (power)

Arduino Pin 9        ──────────────── Servo orange (signal)
```

## Why the common ground matters

The signal wire carries a PWM waveform — a pulse that varies between 0V (LOW) and 5V (HIGH) relative to the Arduino's ground. The servo's control circuit interprets this pulse width to set its position. If the servo's ground and the Arduino's ground are at different potentials — even a fraction of a volt apart — the servo interprets the signal incorrectly and behaves erratically or not at all.

Connecting the grounds makes both references the same. It's the single most common mistake when adding external power to a servo project, and the symptom (servo doesn't respond or twitches randomly) looks exactly like a wiring or code error.

## The sketch

The Arduino IDE's built-in Servo sweep example is the standard test for this setup:

```cpp
#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);
}

void loop() {
  for (int pos = 0; pos <= 180; pos++) {
    myServo.write(pos);
    delay(15);
  }
  for (int pos = 180; pos >= 0; pos--) {
    myServo.write(pos);
    delay(15);
  }
}
```

Upload with the external supply off, then apply power to the external supply. The servo should sweep back and forth continuously. If it doesn't move at all, check the common ground connection first.

## Scaling up

The same principle applies to larger servos, multiple servos, and motor drivers. Any load that exceeds the Arduino's I/O current capacity (20 mA per pin, 200 mA total across all pins) needs external power with a common ground reference.

For multiple servos on the same external supply, connect all their red wires to the 5V rail and all their brown wires to the GND rail, with that GND rail still connected to the Arduino's GND. Each servo gets its signal from a separate Arduino pin.

A dedicated servo power bus — a strip of header pins on a breadboard with 5V and GND rails fed from a single supply — makes multi-servo builds cleaner and easier to debug than running individual wires from each servo back to the supply.

## References and further reading

- [Arduino `Servo` library reference](https://www.arduino.cc/reference/en/libraries/servo/) — `.attach()`, `.write()`, `.read()` and the full API
- [TowerPro SG90 datasheet](http://www.towerpro.com.tw/product/sg90-7/) — the stall current, operating voltage range, and speed specs
- [Arduino current limits (ATmega328P datasheet)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf) — Section 29: Electrical Characteristics; the 40 mA per-pin and 200 mA aggregate limits are defined here
- [Servo power and grounding guide (Adafruit)](https://learn.adafruit.com/adafruit-motor-shield-v2-for-arduino/powering-motors) — Adafruit's general write-up on powering motors and the common-ground requirement
- [Breadboard power supply modules on eBay](https://www.ebay.com/sch/i.html?_nkw=breadboard+power+supply+module) — the kind used in this post; ~$3 shipped, accepts 6.5–12V input, outputs 5V and 3.3V at up to 700mA
