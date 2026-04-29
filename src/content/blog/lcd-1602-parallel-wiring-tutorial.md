---
title: 'Wiring a 1602 Character LCD the Parallel Way — Arduino, MSP430, and Standalone'
description: 'The HD44780-driven 1602 LCD is the universal $2 display that works with everything. Here is the complete parallel wiring across three platforms: Arduino Uno, TI MSP430 Launchpad, and a standalone MSP430G2553 chip with voltage regulators on a bare breadboard.'
pubDate: 'September 25 2012'
youtubeId: 'QRlVQWmIGgM'
heroImage: '../../assets/posts/lcd-1602-parallel-wiring-tutorial/thumbnail.jpg'
tags: ['arduino', 'lcd', 'hd44780', 'msp430', 'display', 'tutorial']
---

There are two ways to wire a 1602 LCD to a microcontroller: the parallel interface (the original, covered here) and the I²C interface through a small PCF8574 backpack module (covered in [this earlier post](/blog/arduino-i2c-lcd-1602)). The parallel version uses more pins — six versus two — but needs no extra hardware, works with any microcontroller that has spare I/O, and is the one that comes up in most datasheets and reference designs. If you've ever wondered what all those 16 pins on the LCD header actually do, this is the walkthrough.

This post covers the full parallel wiring three ways: to an Arduino Uno, to a TI MSP430 Launchpad running Energia, and to a standalone MSP430G2553 chip on a breadboard with a 7805 and LM1117 providing 5V and 3.3V from a higher-voltage supply. Each section ends with a working "Hello World."

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The display itself

The 1602 LCD is a 16-character × 2-row character display driven by a Hitachi HD44780 controller (or one of the many compatible clones). You can find these for around $2 shipped on eBay — they've been at roughly that price for over a decade, which reflects how long they've been in production and how commoditized the HD44780 has become. Adafruit sells them for closer to $12; the only functional difference is peace of mind about the sourcing.

The display has 16 pins. In 4-bit parallel mode you only need to connect 11 of them; the other 5 are either tied to a fixed voltage or left unconnected.

## The 16-pin header

| Pin | Name | Function |
|-----|------|---------|
| 1 | GND | LCD logic ground |
| 2 | VCC | LCD logic power (+5V) |
| 3 | V0 | Contrast adjust (wiper of a 10K pot) |
| 4 | RS | Register Select: HIGH = data, LOW = command |
| 5 | RW | Read/Write: tie to GND to write-only |
| 6 | EN | Enable: pulse HIGH to latch data |
| 7–10 | DB0–DB3 | Data bus lower nibble — leave unconnected in 4-bit mode |
| 11–14 | DB4–DB7 | Data bus upper nibble — the four you actually wire |
| 15 | LED+ | Backlight anode (+5V, through a current-limiting resistor) |
| 16 | LED– | Backlight cathode (GND) |

In 4-bit mode, the LiquidCrystal library sends data in two nibbles across just DB4–DB7. This halves the required pins at a small speed cost that's imperceptible on a character display.

## Part 1: Wiring to Arduino Uno

**Power and backlight first.** Before touching the data lines, get the backlight and logic power sorted — this lets you verify the display is alive before dealing with the signal wiring.

Connect 5V and GND from the Arduino to your breadboard's power rails. Then:

- Pin 1 (GND) → ground rail
- Pin 2 (VCC) → 5V rail
- Pin 15 (LED+) → 5V rail (backlight anode; some displays include an onboard resistor, others require an external ~100Ω series resistor — check the datasheet for your specific module)
- Pin 16 (LED–) → ground rail

Plug in power. The backlight should illuminate. If it doesn't, stop here — double-check the power connections before proceeding.

**Contrast potentiometer.** The V0 pin sets the display contrast. Without it connected to something in the right range, you'll either see nothing or a row of black blocks.

Wire a 10K potentiometer: one outer leg to 5V, the other outer leg to GND, and the center wiper to pin 3 (V0). Once the sketch is uploaded, adjust the pot until the characters are clear.

**RW pin.** Connect pin 5 (RW) directly to GND. This hard-codes the display in write-only mode. Floating RW is a common cause of garbage on the display.

**Data and control lines.** The pin assignments used with the Arduino LiquidCrystal library in this build:

| LCD pin | Name | Arduino pin |
|---------|------|-------------|
| 4 | RS | D7 |
| 6 | EN | D8 |
| 11 | DB4 | D9 |
| 12 | DB5 | D10 |
| 13 | DB6 | D11 |
| 14 | DB7 | D12 |

**The sketch.** Open the LiquidCrystal Hello World example from the Arduino IDE (File → Examples → LiquidCrystal → HelloWorld) and update the `LiquidCrystal` constructor to match your pin assignments:

```cpp
#include <LiquidCrystal.h>

// RS, EN, DB4, DB5, DB6, DB7
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  lcd.begin(16, 2);
  lcd.print("Hello World!");
}

void loop() {
  // nothing
}
```

Upload and adjust the contrast pot. "Hello World!" should appear on the top row.

## Part 2: Wiring to the MSP430 Launchpad (Energia)

The wiring to the MSP430 Launchpad is essentially identical — same LCD pins, same resistor and potentiometer, same contrast adjustment. The differences are on the microcontroller side: pin names follow MSP430 port notation (P1.x, P2.x), Energia maps these to its own pin numbering scheme, and the library calls use the same Arduino-compatible syntax.

The Launchpad runs at 3.3V, and the 1602 LCD's HD44780 controller will typically operate at 3.3V even though it's specified for 5V. The backlight may be slightly dimmer and contrast adjustment will sit at a different pot position, but the display functions correctly at 3.3V — which is genuinely useful given that many modern sensors are also 3.3V parts.

In Energia, the LiquidCrystal library is included the same way. Assign your Launchpad's available digital pins to RS, EN, and DB4–DB7, update the constructor, and the same Hello World sketch compiles and runs unchanged.

## Part 3: Standalone MSP430G2553 with voltage regulators

This section moves the MSP430 chip off the Launchpad entirely onto a bare breadboard, powered by a 7805 (5V linear regulator) and an LM1117 3.3V (3.3V linear regulator) from a higher-voltage supply.

**Why two regulators?** The LCD backlight and HD44780 logic want 5V. The MSP430G2553 runs on 3.3V. Using separate regulators lets each get its proper voltage from a common higher-voltage input (9V wall wart, or a 6×AA pack).

**7805 wiring (5V for LCD):**
- Input: 9V supply positive
- GND: common ground
- Output: 5V to breadboard power rail

The 7805 needs a 0.1µF bypass capacitor on the input and output to suppress oscillation. Without them, the regulator may be stable — or it may not be. Add them.

**LM1117 3.3V wiring (for MSP430):**
- Input: 5V rail (from the 7805 output)
- GND: common ground
- Output: 3.3V to a separate rail for the MSP430's VCC

**MSP430G2553 standalone.** Reset pin to VCC via a 4.7K pull-up resistor (this is required — floating RST causes continuous resets). VCC to 3.3V rail. GND to common ground. Connect the data/control lines from the MSP430 port pins to the LCD exactly as in the Launchpad section.

One note from the video: the MSP430G2553 chip can tolerate 5V on its I/O pins even though it runs on 3.3V — the pin structures are rated for it. This means you can run the LCD from 5V and still directly wire it to the MSP430 without a level shifter. It works, though it's not the textbook-correct approach.

## The one thing to do before any of this

Get the backlight and contrast working before you connect a single data line. "Is it wired right?" and "is the contrast set right?" look identical on the screen — both give you nothing. Establishing that the backlight is on and the contrast is in range eliminates half the possible failure modes before you touch the signal wiring.

## References and further reading

- [HD44780 datasheet (Hitachi)](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) — the original spec; initialization sequence, timing, and register commands are all in here
- [Adafruit character LCD wiring guide](https://learn.adafruit.com/character-lcds/wiring-a-character-lcd) — the tutorial referenced in this video; the most clearly illustrated parallel-wiring guide available
- [Arduino LiquidCrystal library reference](https://www.arduino.cc/reference/en/libraries/liquidcrystal/) — all methods: `begin()`, `print()`, `setCursor()`, `clear()`, `scrollDisplayLeft()`, etc.
- [7805 voltage regulator datasheet](https://www.ti.com/lit/ds/symlink/lm7805.pdf) — TI's version; the bypass capacitor values and thermal calculations are here
- [LM1117 3.3V regulator datasheet](https://www.ti.com/lit/ds/symlink/lm1117.pdf) — TI's LM1117 spec; low-dropout so it can be driven from 5V cleanly
- [MSP430G2553 datasheet](https://www.ti.com/lit/ds/symlink/msp430g2553.pdf) — includes the I/O voltage tolerances that allow 5V signals on a 3.3V part
- [Energia LiquidCrystal library](https://energia.nu/reference/en/libraries/liquidcrystal/) — the MSP430-compatible version used in Part 2 and Part 3
