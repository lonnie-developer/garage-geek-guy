---
title: 'MSP430 Launchpad as an I2C Slave with an Arduino Mega Master'
description: 'An Arduino Mega 2560 commands an Arduino Uno and a TI MSP430 Launchpad on the same I2C bus. Here is the voltage caveat, the Launchpad I2C pin locations, the Energia tone() fix, and a power trick for running the Launchpad off the Mega when you only have one USB port.'
pubDate: 'October 18 2012'
youtubeId: 'tHqBwFY2z5w'
heroImage: '../../assets/posts/msp430-i2c-arduino-mega-multi-slave/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'arduino', 'i2c', 'energia', 'tutorial']
---

Most I²C tutorials stay inside one ecosystem — all Arduinos, or a known Arduino-compatible sensor. Adding a Texas Instruments MSP430 Launchpad to the mix introduces a few wrinkles that aren't covered by the standard Wire library documentation: the MSP430 is a 3.3V device, its I²C pin locations aren't labeled the same way as Arduino pins, the Energia IDE has a few compiler quirks when porting Arduino sketch code, and you need somewhere to put the Launchpad when you've run out of USB ports.

This post walks through all of it. The result: an Arduino Mega 2560 as I²C master, an Arduino Uno as slave address 5 (turns an LED on and off), and an MSP430 Launchpad as slave address 6 (plays a 1900 Hz tone on a piezo speaker). Master sends "H" to both, then "L" to both, on a three-second cycle.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The voltage issue first

The MSP430 G2 series runs on 3.3V. The Arduino ecosystem, by default, runs on 5V. Putting a 3.3V device's I²C pins on a 5V I²C bus is a recipe for a damaged MSP430 — the input pins aren't rated for 5V signals from a 5V pull-up.

The fix used here: move the Mega's I²C power jumper from the 5V rail to the 3.3V rail, dropping the entire bus voltage to 3.3V. The Arduino Uno and the MSP430 Launchpad are both happy at 3.3V. The Uno's I²C pins, while specified for 5V logic, tolerate 3.3V signals cleanly.

This is the simplest solution when mixing 3.3V and 5V I²C devices on the same bus. The alternative — bi-directional level shifters on SDA and SCL — is more correct but significantly more complex for a bench demonstration. For anything going into a real product, use level shifters or source 3.3V-native I²C devices throughout.

## Launchpad I²C pin locations (Energia)

The MSP430 Launchpad's I²C interface lives on Port 1:

- **SDA → P1.7** (left side of Launchpad, near the USB connector)
- **SCL → P1.6** (immediately next to SDA)

In Energia code, these are referenced as Energia pin numbers (not P1.x notation), but the physical wiring uses the Launchpad header. Connect Launchpad P1.7 to the SDA rail on the breadboard and P1.6 to the SCL rail.

The piezo speaker goes to **P1.4**, which is **Energia pin 6**. One speaker terminal to pin P1.4, the other to GND.

## The Mega master sketch

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();  // no address = master
  delay(2000);   // give slaves time to initialize
}

void loop() {
  // Tell the Uno (address 5) to turn LED on
  Wire.beginTransmission(5);
  Wire.write('H');
  Wire.endTransmission();

  // Tell the Launchpad (address 6) to play tone
  Wire.beginTransmission(6);
  Wire.write('H');
  Wire.endTransmission();

  delay(3000);

  // Turn off LED
  Wire.beginTransmission(5);
  Wire.write('L');
  Wire.endTransmission();

  // Silence tone
  Wire.beginTransmission(6);
  Wire.write('L');
  Wire.endTransmission();

  delay(3000);
}
```

The `delay(2000)` in `setup()` is worth keeping: it gives the slaves — particularly the Launchpad, which may initialize slightly slower than an Arduino — time to complete their `Wire.begin()` calls before the master starts sending. Without it, the first transmission or two may be lost.

## The Arduino Uno slave sketch (address 5)

```cpp
#include <Wire.h>

const int ledPin = 13;

void setup() {
  Wire.begin(5);  // slave address 5
  Wire.onReceive(receiveEvent);
  pinMode(ledPin, OUTPUT);
}

void receiveEvent(int bytes) {
  char c = Wire.read();
  if (c == 'H') digitalWrite(ledPin, HIGH);
  if (c == 'L') digitalWrite(ledPin, LOW);
}

void loop() {}
```

## The MSP430 Launchpad slave sketch (address 6, in Energia)

This starts as a port of the Uno slave sketch. Most of it transfers directly — Energia is designed to be Arduino-compatible — but there are a few gotchas:

```cpp
#include <Wire.h>

const int speakerPin = 6;  // P1.4 = Energia pin 6

void setup() {
  Wire.begin(6);  // slave address 6
  Wire.onReceive(receiveEvent);
  pinMode(speakerPin, OUTPUT);
}

void receiveEvent(int bytes) {
  char c = Wire.read();
  if (c == 'H') tone(speakerPin, 1900);
  if (c == 'L') noTone(speakerPin);
}

void loop() {}
```

**Compile errors you'll likely hit:**

1. **`noTone` not declared** — Energia's compiler is case-sensitive in ways that sometimes differ from the Arduino IDE. If you type `NoTone` or `NOTONE` it won't compile. Make sure it's exactly `noTone`.

2. **"too few arguments" on `tone()`** — In some Energia versions, `tone()` requires a duration argument: `tone(pin, frequency, duration)`. If the two-argument form fails to compile, add a large duration (e.g., `tone(speakerPin, 1900, 10000)`) or handle the stop in the `'L'` branch with `noTone()`.

These are minor but they'll stop a compile cold. Once they're sorted, the sketch uploads and the tone fires on command.

## Powering the Launchpad from the Mega

The Mega 2560 and the Launchpad both want USB connections for programming — but if your computer has only two USB ports and one is already occupied by the Mega, you need another option for the Launchpad.

The Launchpad has two exposed test points near the USB connector that are the input power rails: one is 5V, one is GND. These are the same points the USB cable would power. Running wires from the Mega's 5V and GND pins to these test points powers the Launchpad as if it were plugged in over USB — without needing an actual USB connection.

This only works for running already-programmed sketches, not for programming. You'll need to upload your Launchpad sketch first (while the Launchpad is connected to USB for programming), then switch to the stolen-power arrangement for the combined demo.

## What the demo looks like

With everything connected and both sketches uploaded: the Mega powers up, waits two seconds, then sends "H" to address 5 and address 6. The Uno's LED lights up. The Launchpad's speaker plays a 1900 Hz tone. After three seconds, the Mega sends "L" to both — LED off, tone stops. Then silence for three seconds, and the cycle repeats.

It's not a complicated demo, but it confirms that cross-platform I²C works, that the voltage question has been handled correctly, and that Energia's Wire library speaks the same protocol as Arduino's. The same pattern scales to any mix of I²C devices: add another slave at address 7, send it a different command, and the bus handles it without any changes to the existing slave sketches.

## References and further reading

- [MSP430G2 Launchpad user guide (SLAU318)](https://www.ti.com/lit/ug/slau318g/slau318g.pdf) — the Launchpad hardware schematic including the P1.x pin locations and the USB test points
- [Energia IDE](https://energia.nu/) — the Arduino-compatible development environment for MSP430 and other TI microcontrollers
- [Energia Wire library](https://energia.nu/reference/en/libraries/wire/) — Wire.begin(), onReceive(), and the MSP430-specific behavior
- [Energia pin maps — MSP430 Launchpad G2](https://energia.nu/guide/pinmaps/launchpad-msp430g2/) — maps Energia pin numbers to physical MSP430 port pins
- [Arduino Wire library reference](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — the master-side API used in the Mega sketch
- [I²C level shifting for mixed-voltage buses](https://learn.sparkfun.com/tutorials/bi-directional-logic-level-converter-hookup-guide) — SparkFun's guide on proper level shifting when you can't drop the whole bus voltage to 3.3V
- [Adafruit I²C FAQ](https://learn.adafruit.com/i2c-addresses/overview) — covers addresses, pull-ups, and bus voltage considerations in accessible terms
