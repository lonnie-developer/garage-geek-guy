---
title: 'How to Use an I2C LCD Display with Arduino — Library Install + Code Examples'
description: 'Wire a 16x2 I2C LCD to Arduino in 4 connections, install the LiquidCrystal_I2C library, and use the key display methods with working code examples.'
pubDate: 'November 11 2018'
youtubeId: 'rB1cFwA1q24'
heroImage: '../../assets/posts/i2c-lcd-arduino/thumbnail.jpg'
tags: ['arduino', 'lcd', 'i2c', 'tutorial', 'display']
---

The standard parallel-wired 16x2 LCD has been a staple of Arduino beginner projects for years, and for good reason — the HD44780 controller is well-documented, the LiquidCrystal library comes pre-installed, and the hardware is dirt cheap. The problem is the wiring: six Arduino pins, an external potentiometer for contrast, and a connector pinout that invites mistakes. For any project where you're using the LCD for feedback while doing something else, you've just burned half your Uno's digital pins on a display.

The I2C version of the same LCD cuts all of that down to four wires. Two for power, two for data. No external potentiometer — the contrast trim pot is built right onto the adapter board that piggybacks on the back of the display. If you're already comfortable with the parallel LCD, making the switch takes about twenty minutes including library install.

## What's actually different about the I2C version

The LCD panel itself is identical to the parallel version — same HD44780 controller IC, same glass, same character set. The difference is a small PCB soldered onto the back that bridges the HD44780's parallel interface to an I2C bus. On most of the common modules you'll find, that bridge chip is a **PCF8574** — an 8-bit I/O expander from NXP that speaks I2C on one side and drives the HD44780's parallel data lines on the other.

This matters because the PCF8574 has a configurable I2C address. There are usually three solder jumpers on the adapter board (labeled A0, A1, A2) that set the low three bits of the address. Most modules ship with all jumpers open, which gives address **0x27**. If you have two of these displays on the same I2C bus, you can bridge one of the jumpers to change the address — typically to 0x3F, though the exact options depend on the specific PCF8574 variant used (PCF8574 defaults to 0x20-based addressing; PCF8574**A** defaults to 0x38-based). If you're not sure what address your module uses, there's a [companion video that walks through I2C address scanning](https://www.youtube.com/watch?v=dVqv3LvJAJY) with a simple Arduino sketch.

The I2C protocol itself was developed by Philips Semiconductors in 1982 specifically to let microcontrollers talk to peripheral ICs using just two wires: SDA (data) and SCL (clock). On the Arduino Uno, those are dedicated pins — **A4 for SDA** and **A5 for SCL** — not interchangeable with other analog pins for this purpose. The Nano uses the same physical pins. Larger boards like the Mega and Due have separate dedicated SDA/SCL pins broken out separately.

## Installing the library

The parallel LCD uses the built-in LiquidCrystal library. The I2C version needs an additional library — the most widely used is the **LiquidCrystal_I2C** library, originally written by fdebrabander and available on GitHub.

To install it:

1. Go to [github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library](https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library) and download the repository as a ZIP file (click the green Code button → Download ZIP).
2. In the Arduino IDE, go to **Sketch → Include Library → Add .ZIP Library…**
3. Navigate to the downloaded ZIP and select it.
4. **Close and reopen the IDE.** The library doesn't become available until you restart.

You can confirm the install worked by looking in your Documents/Arduino/libraries folder — you should see an `Arduino-LiquidCrystal-I2C-library-master` directory with the source files inside.

Newer versions of the Arduino IDE (2.x) can also install it directly from the Library Manager by searching for "LiquidCrystal I2C." Either approach works; the ZIP method just mirrors what's described in the video.

## Wiring

Four connections, that's it:

| LCD module pin | Arduino Uno |
|---|---|
| GND | GND |
| VCC | 5V |
| SDA | A4 |
| SCL | A5 |

The pins are labeled directly on the adapter board, which helps. Once you've made these four connections, the only other adjustment might be the small contrast potentiometer on the adapter board — turn it with a small screwdriver until the characters appear clear without the pixel grid squares being visible.

One thing worth noting: the SDA/SCL pins on the Uno are shared with A4 and A5 in their analog capacity. You can still use A0–A3 as analog inputs while the LCD is connected, but A4 and A5 are now spoken for.

## Getting started: hello world

```cpp
#include <LiquidCrystal_I2C.h>

// (I2C address, columns, rows)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.print("Hello, world!");
}

void loop() {
  // nothing — setup() runs once and holds
}
```

If nothing appears on the screen, the most common culprits are: wrong I2C address (try 0x3F if 0x27 shows nothing), contrast potentiometer too far in one direction, or missing library restart after install. Adjust the contrast pot first — it's often set to an extreme from the factory.

## The display methods worth knowing

**`lcd.clear()`** wipes the display buffer and moves the cursor back to position (0, 0). Use this when you want to replace what's on screen with entirely new content.

**`lcd.display()` and `lcd.noDisplay()`** turn the display on and off without clearing the buffer. This is the cleaner option when you want to flash or hide content temporarily — the text survives the `noDisplay()` call and comes back intact when you call `display()` again. Useful for low-power blink indicators or "is the system alive" signals without the overhead of rewriting text on every cycle.

**`lcd.cursor()` and `lcd.noCursor()`** toggle an underline cursor character at the current cursor position. Mostly useful in menu-style UIs where you want to indicate which field is active.

**`lcd.blink()`** produces a blinking box cursor. Slightly more visible than the underline. Turn it off with `lcd.noCursor()`.

**`lcd.setCursor(col, row)`** positions the cursor before your next `print()`. Columns are 0-indexed, rows are 0-indexed. For a 16×2 display:

```cpp
lcd.setCursor(0, 0);   // top-left
lcd.setCursor(0, 1);   // bottom-left
lcd.setCursor(8, 1);   // bottom row, 9th character in
```

This is how you put different pieces of information in different positions on the display — write a label to the top row once in setup, then use `setCursor` to update only the numeric value on the bottom row in the loop.

## A practical example: potentiometer live readout

A good test that exercises both the wiring and the display update logic: wire a potentiometer to A0 and display the `analogRead` value in real time.

```cpp
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.begin();
  lcd.backlight();
}

void loop() {
  lcd.clear();
  lcd.print(analogRead(A0));
  delay(100);
}
```

The potentiometer wiring: one outer leg to GND, the other outer leg to 5V, the wiper (middle leg) to A0. Turning the pot sweeps the display between 0 and 1023.

You'll notice if you use `lcd.clear()` inside the loop without a delay, the display flickers — the clear and rewrite happen fast enough that the backlight visibly strobes. A 50–100ms delay smooths this out considerably. For most sensor-display applications, 100ms refresh is plenty — it's plenty fast enough to look "live" and slow enough to read comfortably.

For cleaner updates on displays showing values of varying digit counts (like a value jumping from 999 to 1000 or back), using `setCursor` and overwriting specific character positions with spaces before the new value avoids the full-clear flicker entirely.

## The gotcha: I2C address mismatch

If you run the hello world sketch and get nothing — no text, just a lit backline or nothing at all — the most likely cause after contrast adjustment is an I2C address mismatch. The sketch hardcodes 0x27 but your module might be 0x3F or some other value.

The reliable fix: run an I2C scanner sketch before building anything else. It probes every address on the bus and reports what it finds. Once you know your display's actual address, swap that into the `LiquidCrystal_I2C` constructor. There's a simple scanner sketch [in this companion video](https://www.youtube.com/watch?v=dVqv3LvJAJY) that covers finding any I2C device's address in a few minutes.

## Where the I2C LCD makes sense (and where it doesn't)

The I2C LCD wins whenever pin count matters. A Uno running a servo, reading multiple sensors, and driving an LCD simultaneously on the parallel interface runs out of pins fast. The I2C version costs you two analog pins (A4, A5) and leaves everything else free. For prototyping and most hobbyist projects, that's the right tradeoff.

The one place the parallel LCD has an edge is update speed. The parallel interface can refresh a 16×2 display significantly faster than I2C at the default 100kHz clock speed. For displaying a static label or a once-per-second sensor reading, this difference is invisible. For anything that needs to update the full display dozens of times per second, the parallel version or a different display technology (OLED, SPI LCD) is worth considering.

The I2C LCD also plays well with other I2C devices on the same bus — you can run a display, a real-time clock module, a temperature sensor, and an EEPROM all on the same two wires as long as their addresses don't conflict. That expandability is one of the best things about the I2C ecosystem in general.

## References

- [fdebrabander LiquidCrystal_I2C library (GitHub)](https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library) — the library used in this tutorial
- [Arduino LiquidCrystal library reference](https://www.arduino.cc/en/Reference/LiquidCrystal) — most methods mirror the parallel library API
- [PCF8574 datasheet (NXP)](https://www.nxp.com/docs/en/data-sheet/PCF8574_PCF8574A.pdf) — the I/O expander chip on the back of most I2C LCD modules
- [HD44780 datasheet (Hitachi)](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) — the underlying LCD controller IC
- [I2C scanner sketch (Arduino playground)](https://playground.arduino.cc/Main/I2cScanner/) — find the address of any I2C device
- [Arduino Wire library documentation](https://www.arduino.cc/en/reference/wire) — the underlying library that handles I2C communication
- [Companion video: finding I2C device addresses](https://www.youtube.com/watch?v=dVqv3LvJAJY) — Arduino sketch to scan and report all I2C addresses on the bus
