---
title: 'I2C Communication Between an Arduino Uno and an Arduino Mega 2560'
description: 'Two Arduinos, one bus: an Arduino Mega 2560 as I2C master telling an Arduino Uno slave when to light an LED. Covers the Mega pin locations, 4.7K pullup wiring, common ground requirement, and the Wire library code for both sides.'
pubDate: 'October 18 2012'
youtubeId: 'iOran8zx1yQ'
heroImage: '../../assets/posts/i2c-arduino-uno-mega-2560/thumbnail.jpg'
tags: ['arduino', 'i2c', 'tutorial', 'beginner']
---

Most I²C examples in the Arduino ecosystem involve a microcontroller talking to a sensor — one master, one slave, and the slave is a purpose-built module with a fixed address. Talking between two full Arduinos flips the model: one runs master code, one runs slave code, and the Wire library handles both ends.

This is the simplest possible version of that — an Arduino Mega 2560 as master sending a single character to an Arduino Uno slave, which lights or extinguishes an LED based on what it receives. No I²C sensors, no libraries beyond Wire. Just the bus, two boards, and the fundamental master/slave structure that every more complex I²C project is built on.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## What's on the bus

- **Master:** Arduino Mega 2560 — sends "H" (LED on) and "L" (LED off) to slave address 5, cycling on a 3-second interval
- **Slave:** Arduino Uno at address 5 — receives bytes, drives an LED on digital pin 8

That's it. One device on the bus, one command.

## I²C pin locations

On the Mega, I²C is labeled directly on the board header: **pin 20 is SDA, pin 21 is SCL**. Unlike the Uno where I²C lives on the analog header (A4/A5), the Mega broke them out to their own labeled digital pins. This is easy to miss if you're used to the Uno layout.

On the Uno: **A4 is SDA, A5 is SCL**. Standard and consistent across every Uno-class board.

## Wiring

Run both SDA lines and both SCL lines to a shared bus — a pair of breadboard power rails works well here. The I²C bus needs pullup resistors to bring SDA and SCL high between transactions. **4.7 kΩ on each line, from the line to 5V.** Connect one end of each resistor to the respective bus rail, the other to the 5V rail.

```
Arduino Mega pin 20 (SDA) ──┬──────── Arduino Uno A4 (SDA)
                             │
                           4.7K
                             │
                            5V

Arduino Mega pin 21 (SCL) ──┬──────── Arduino Uno A5 (SCL)
                             │
                           4.7K
                             │
                            5V
```

**Common ground — required.** Connect a GND pin from the Mega to a GND pin on the Uno. Without a shared ground reference, the signal voltage levels are meaningless relative to each other and the bus won't work. This is the step that looks redundant if both boards are powered from the same computer's USB ports, but it's still worth wiring explicitly — especially if they're ever powered from separate sources.

**LED on the Uno:** wire a red LED and a 500 Ω resistor in series between digital pin 8 and GND. Long leg to pin 8, short leg through the resistor to GND. (No series resistor on the Arduino side — the 500 Ω does the current limiting.)

## The Mega master sketch

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();  // master — no address argument
  delay(2000);   // give the slave time to initialize
}

void loop() {
  Wire.beginTransmission(5);  // address 5 = the Uno
  Wire.write('H');
  Wire.endTransmission();

  delay(3000);

  Wire.beginTransmission(5);
  Wire.write('L');
  Wire.endTransmission();

  delay(3000);
}
```

The `delay(2000)` in `setup()` is a safe habit: it gives the slave board time to complete its own `Wire.begin()` and register its address before the master starts sending. Skip it and the first few transmissions may be lost.

## The Uno slave sketch

```cpp
#include <Wire.h>

const int ledPin = 8;

void setup() {
  Wire.begin(5);  // register as slave address 5
  Wire.onReceive(receiveEvent);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void receiveEvent(int bytes) {
  char c = Wire.read();
  if (c == 'H') digitalWrite(ledPin, HIGH);
  if (c == 'L') digitalWrite(ledPin, LOW);
}

void loop() {}
```

`Wire.onReceive()` registers a callback that fires automatically whenever the slave receives data. The main `loop()` is empty — all the action happens in the interrupt-like callback. Inside `receiveEvent`, `Wire.read()` pulls the byte off the buffer and the `if` statements decide what to do with it.

## Upload order and the classic mistake

Upload the slave sketch to the **Uno first**, then upload the master sketch to the **Mega**. The Mega will sit in `setup()` for its 2-second delay, then start sending — if the Uno is already running by then, everything works.

The classic mistake here is uploading master code to one board and slave code to the other, but getting the boards mixed up and flashing the wrong sketch to each. The symptom is: nothing happens, no error, complete silence. If it's not working, double-check which port corresponds to which board in the IDE before re-flashing.

## What successful I²C looks like

Once both sketches are running: the Mega powers up, waits 2 seconds, sends 'H' to address 5. The Uno's LED lights up. 3 seconds later the Mega sends 'L'. LED goes off. 3 seconds of silence, then it repeats.

The Mega's Serial Monitor isn't needed — the LED is the only output and it's either on or off. If it's not cycling, the most likely culprits in order: wrong board got the wrong sketch, missing common ground, or pullup resistors not connected to 5V.

## Scaling up from here

Adding a third device is as simple as assigning it a different address — say address 6 — and sending to that address in separate `Wire.beginTransmission(6)` / `Wire.endTransmission()` calls. The bus and the pullup resistors don't change. Each new slave just needs its own `Wire.begin(N)` and `Wire.onReceive()` callback.

This two-Arduino demo is also the logical predecessor to mixing Arduinos with non-Arduino I²C devices. Once the master/slave structure makes sense, adding a sensor at address 0x27 or an MSP430 at address 6 is the same pattern with a different address number.

## References and further reading

- [Arduino Wire library reference](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — `beginTransmission()`, `endTransmission()`, `onReceive()`, and `read()`
- [Arduino Mega 2560 pin diagram](https://store.arduino.cc/products/arduino-mega-2560-rev3) — confirms pins 20/21 as SDA/SCL on the digital header
- [I²C pullup resistor selection guide (TI)](https://www.ti.com/lit/an/slva689/slva689.pdf) — the math behind pullup value selection for different bus speeds and capacitances; 4.7 kΩ at 100 kHz is a safe default
- [Arduino I²C scanner](https://playground.arduino.cc/Main/I2cScanner/) — useful for verifying that a device is showing up at the expected address before writing application code
- [Adafruit I²C FAQ](https://learn.adafruit.com/i2c-addresses/overview) — covers addresses, pull-ups, and multi-device bus behavior accessibly
