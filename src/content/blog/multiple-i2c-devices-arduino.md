---
title: 'How to Connect Multiple I2C Devices to One Arduino'
description: 'I2C lets you run up to 127 devices on two wires. Here is how the bus works, why pull-up resistors matter when daisy-chaining, and a working example with a 1602 LCD and an SSD1306 OLED on the same Arduino.'
pubDate: 'November 12 2018'
youtubeId: 'nEySekIIxpw'
heroImage: '../../assets/posts/multiple-i2c-devices-arduino/thumbnail.jpg'
tags: ['arduino', 'i2c', 'lcd', 'oled', 'tutorial', 'electronics']
---

I²C is what makes the "two wires can talk to a lot of things" claim in microcontroller specs actually true. The protocol — designed by Philips Semiconductor (now NXP) in 1982 — is built around a shared bus architecture: every device on the bus shares the same two wires, and the master (your Arduino) addresses each one individually by its unique 7-bit address. At any given moment, only one device is talking, but all of them are listening. With 127 possible addresses, you can theoretically hang 127 devices off a single Arduino's SDA/SCL pins.

In practice you'll have address conflicts well before 127, and long bus runs get noisy, but the point stands: two wires go a long way.

This post demonstrates the multi-device setup with a 16×2 I²C LCD and a 128×64 OLED (SSD1306) running simultaneously on the same Arduino, explains why pull-up resistors are necessary when you start daisy-chaining devices, and walks through the combined sketch.

## Why this comes up

The immediate use case here was a real-time clock module (DS3231 or DS1307, both I²C) alongside a 16×2 LCD display. Both devices are I²C, both are common Arduino peripherals, and neither has an obvious way to "share" a connection unless you already know the bus supports it. The RTC is at 0x68, the LCD backpack is usually 0x27 — different addresses, no conflict, they can both be on the bus at the same time.

Same situation shows up with any two I²C peripherals: a magnetometer and a barometer, a OLED and an accelerometer, multiple temperature sensors with different addresses. Understanding the multi-device setup once means all of those just work.

## What you'll need

- Arduino Uno (or any Arduino with hardware I²C — SDA on A4, SCL on A5)
- 16×2 I²C LCD (PCF8574 backpack, typically address 0x27)
- 128×64 OLED display (SSD1306-based, typically address 0x3C)
- 2× 10K resistors (for pull-ups on SDA and SCL)
- Breadboard and jumper wire
- [LiquidCrystal\_I2C library](https://github.com/johnrickman/LiquidCrystal_I2C)
- [Adafruit SSD1306 library](https://github.com/adafruit/Adafruit_SSD1306) (and its dependency, Adafruit GFX)

## Finding your device addresses first

Before writing any combined sketch, confirm the addresses of both devices. Load the I²C scanner sketch — it's a standard snippet available at [Arduino Playground](https://playground.arduino.cc/Main/I2cScanner/) — and open the serial monitor. With both devices wired up, it will report something like:

```
I2C device found at address 0x27
I2C device found at address 0x3C
```

If it reports nothing, check wiring. If it shows only one device, check the second device's connections. The scanner is a fast sanity check that saves a lot of confused debugging later.

## Wiring

The I²C bus wires are **SDA** (Serial Data) and **SCL** (Serial Clock). On the Arduino Uno, those are analog pins A4 and A5, doubling as the I²C interface.

Connect both devices to the same SDA and SCL lines — this is the "parallel" nature of the bus. Power each device from the Arduino's 5V and GND rails. A breadboard makes this straightforward: run 5V and GND to the breadboard's power rails, then connect each device's VCC and GND there. SDA from both devices goes to the same node (connected to Arduino A4), and SCL from both devices goes to the same node (connected to Arduino A5).

## The pull-up resistors — why they matter here

I²C uses what's called an open-drain signaling scheme. Devices on the bus can only pull the line *low*; they cannot actively drive it *high*. A pull-up resistor connected from each line to VCC holds the lines high in their default (idle) state. When a device signals, it pulls the line low against the pull-up.

When you're using a single I²C device, the pull-up resistors are often already built onto the module's PCB, and you don't notice them. When you add a second device in parallel, those per-module pull-ups combine — multiple resistors in parallel lower the total pull-up resistance. If it gets too low, the lines can't be pulled low properly and communication breaks. More commonly, people skip external pull-ups entirely when adding devices and then wonder why nothing works.

The safe approach: wire a 10K resistor from SDA to 5V and a 10K resistor from SCL to 5V on the breadboard. This ensures a defined pull-up value regardless of what's built into each module. For typical I²C devices at the default 100 kHz bus speed and short wiring runs on a breadboard, 10K works reliably.

```
5V ──┬── 10K ──┬── SDA (A4) ──┬── LCD SDA
     │         │               └── OLED SDA
     └── 10K ──┴── SCL (A5) ──┬── LCD SCL
                               └── OLED SCL
```

## The sketch

The sketch here combines the Adafruit SSD1306 example (which runs through a built-in graphics demo) with a standard LiquidCrystal\_I2C hello-world, running both on the same bus.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Initialize OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.display();   // show the Adafruit splash screen
  delay(2000);
  display.clearDisplay();

  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Hello World!");
}

void loop() {
  // The SSD1306 example demo runs in a loop here
  // LCD stays static with "Hello World!" from setup()
}
```

The key lines are the two object declarations — `Adafruit_SSD1306` and `LiquidCrystal_I2C` — both pointing to the same `Wire` bus, with different addresses (`0x3C` and `0x27`). The Arduino handles the addressing automatically; you just call the right object's methods and the correct device responds.

When this uploads, the OLED shows the Adafruit splash screen and transitions into the built-in graphics demo, while the LCD simultaneously shows "Hello World!" on the top row. Both are on the same two-wire bus.

Note the sketch uses 64% of the Uno's program storage. The SSD1306 graphics library is heavy — the built-in demo alone accounts for a lot of flash. If you're combining an OLED with other libraries in a real project, watch the memory closely.

## Address conflicts

The one thing that doesn't work: two devices at the same address on the same bus. If you have two identical LCDs with the same PCF8574 address, or two identical OLEDs, you can't distinguish them — the Arduino will address both at once and get garbage.

Most I²C modules have solder-jumper pads labeled A0, A1, A2 that let you change the lower address bits. Closing (or opening, depending on the module) those jumpers shifts the address. Two identical LCDs can coexist at 0x27 and 0x26 with this approach. Check the datasheet for your specific module to see which jumpers map to which address bits.

If you're not sure of your module's address options, the I²C scanner sketch mentioned above is the fastest way to see what's actually there.

## Where this fits next

The immediate next project after verifying this works: swapping out the OLED demo for a real DS3231 or DS1307 real-time clock module. The RTC lives at 0x68, the LCD at 0x27 — no conflict, same wiring approach. The [DS3231 post on this blog](/blog/arduino-ds3231-real-time-clock-lcd-i2c) walks through exactly that combination.

The broader lesson is that I²C is the right bus for "one Arduino, multiple sensors." Any time you find yourself counting available pins and coming up short, check whether the sensors you need have I²C variants. Many do — and they all share the same two wires.

## References and further reading

- [I²C bus specification (NXP)](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) — the definitive spec from the protocol's creator; Sections 3 and 7 are the relevant ones for bus wiring and pull-up resistor selection
- [Arduino Wire library reference](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — the built-in I²C library all these modules depend on
- [I²C scanner sketch](https://playground.arduino.cc/Main/I2cScanner/) — copy-paste this to find device addresses before writing your project code
- [Adafruit SSD1306 library](https://github.com/adafruit/Adafruit_SSD1306) — OLED library used in this post
- [LiquidCrystal\_I2C library](https://github.com/johnrickman/LiquidCrystal_I2C) — LCD library used here
- [PCF8574 I²C expander datasheet](https://www.ti.com/lit/ds/symlink/pcf8574.pdf) — what's on the backpack of most cheap 1602 LCDs; address configuration jumpers are in Table 3
- [Pull-up resistor selection for I²C](https://electronics.stackexchange.com/questions/1346/whats-the-correct-way-to-pullup-i2c-lines) — Stack Exchange thread with a clear explanation of why value matters and how to calculate it
- [Adafruit I²C FAQ](https://learn.adafruit.com/i2c-addresses/overview) — Adafruit's address reference list; useful when planning which devices can share a bus
