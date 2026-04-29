---
title: 'How to Arduino #2 — Wire a 1602 LCD Display (HD44780 Parallel Wiring + LiquidCrystal Library)'
description: 'A complete walkthrough for wiring a 1602 character LCD to an Arduino Uno in 4-bit parallel mode using the LiquidCrystal library — plus a bonus run on the TI MSP430 Launchpad with Energia.'
pubDate: 'November 15 2013'
youtubeId: 'UiyOTBGn4_U'
heroImage: '../../assets/posts/how-to-arduino-2-1602-lcd-parallel/thumbnail.jpg'
tags: ['arduino', 'lcd', 'hd44780', 'msp430', 'tutorial', 'beginner']
---

There's a particular display that shows up in virtually every starter Arduino kit — a 16-column, 2-row character LCD with a blue or green backlight, 16 pins along the top, and no obvious indication of which pins actually need to go anywhere. That's the 1602, and the chip running it is the HD44780 — a Hitachi controller from 1987 that somehow became the universal standard for character displays on every microcontroller platform ever since.

At $2 shipped from eBay, the 1602 is the cheapest way to add a real display to a project. This post walks through how to wire it to an Arduino Uno in 4-bit parallel mode, get the LiquidCrystal library running with the Hello World example sketch, and avoid the two wiring mistakes that trip up almost everyone the first time. There's also a bonus section: the same display wired up to a TI MSP430 Launchpad running Energia, with the identical code compiled down to about 1.8 KB instead of 2.5 KB.

*This build is from 2013, when the channel was still MeanPC.com — same Lonnie, same garage, same bench.*

## The HD44780: a standard that won by accident

The Hitachi HD44780 wasn't designed to become a 40-year standard — it was just a solid, well-documented LCD controller chip that got into early LCD modules before anyone else did. It speaks a simple parallel bus (8-bit or 4-bit), handles character generation internally via a built-in ROM, and supports a handful of useful commands like cursor positioning, display on/off, and scrolling.

What made it stick is that every microcontroller platform eventually wrote a library for it. Arduino has LiquidCrystal in the standard library. Texas Instruments' Energia (the MSP430 IDE) supports the same library with the same API. Parallax BASIC Stamp has drivers for it. Even early Raspberry Pi projects used HD44780-based displays. The 1602 and its bigger sibling the 2004 (20 columns, 4 rows) are still the default choice when you need a no-frills alphanumeric display and don't want to deal with I2C backpacks or SPI configuration.

The display has 16 pins. In 4-bit mode — which is what the LiquidCrystal library uses by default — you only connect 12 of them. The 8-bit data bus (D0–D7) gets cut in half: you wire D4 through D7 and leave D0–D3 disconnected. That saves four Arduino pins with no meaningful performance hit for typical character display work.

## What you'll need

- A 1602 character LCD (any HD44780-compatible module — Elegoo, SainSmart, Sunfounder, or the no-name eBay variety all work)
- An Arduino Uno (or compatible board)
- A 10 kΩ potentiometer for contrast
- Jumper wires — plan on at least 14
- A breadboard
- The Arduino IDE with the built-in LiquidCrystal library (no installation needed)

The contrast potentiometer is non-negotiable. Without it wired and adjusted, you'll see nothing on the display even if everything else is correct. This is the mistake that makes people think their LCD is dead.

## Wiring it up

The 1602 pin numbering runs left to right (pin 1 at the left edge nearest the PCB corner, pin 16 at the right). Here's the complete connection table for 4-bit mode:

| LCD pin | Function | Connect to |
|---------|----------|------------|
| 1 | VSS (logic ground) | Ground |
| 2 | VDD (logic +5V) | +5V |
| 3 | Contrast (V0) | Potentiometer wiper |
| 4 | RS | Arduino D7 |
| 5 | RW | Ground |
| 6 | Enable (E) | Arduino D8 |
| 7–10 | D0–D3 | Not connected |
| 11 | D4 | Arduino D9 |
| 12 | D5 | Arduino D10 |
| 13 | D6 | Arduino D11 |
| 14 | D7 | Arduino D12 |
| 15 | Backlight + | +5V (through series resistor, or direct) |
| 16 | Backlight − | Ground |

**The contrast circuit:** one end of the 10 kΩ pot goes to +5V, the other to ground, and the wiper (middle pin) connects to pin 3 on the LCD. Adjust it after power-on until you see a row of solid rectangles on the top line — that's the display initializing, and it confirms your wiring is correct before you even run any code.

**RW tied to ground:** the RW pin selects read (1) versus write (0) mode. We're only ever writing to the display, so just ground it. Do not leave it floating — a floating RW pin causes phantom characters and random garbage on the display.

**Backlight:** some modules have a built-in current-limiting resistor on pin 15; others need an external resistor. Check the datasheet for your specific module. For a typical 5V backlight at 20 mA, the resistor value is `(5V − Vf) / 0.02A`. In practice, connecting direct to 5V usually works but slightly shortens the backlight's life. A 33–100 Ω resistor in series is safer.

## The LiquidCrystal sketch

Once the wiring is done, open the Arduino IDE, go to **File → Examples → LiquidCrystal → HelloWorld**, and find this line near the top:

```cpp
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
```

Change it to match the pin assignments above:

```cpp
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
```

The constructor arguments are: RS, Enable, D4, D5, D6, D7 — in that order. The rest of the sketch stays the same. Compile and upload; you should see "hello, world!" on the first line and an incrementing counter on the second.

```cpp
#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  lcd.begin(16, 2);
  lcd.print("hello, world!");
}

void loop() {
  lcd.setCursor(0, 1);
  lcd.print(millis() / 1000);
}
```

If you see nothing, turn the contrast pot. If you see a row of solid rectangles but no text, the code isn't running — check your port and board settings. If you see garbage, suspect a loose wire on one of the data lines (D4–D7).

## The gotcha: contrast nobody sets up first

The single most common beginner mistake is wiring the display, uploading the sketch, and then spending an hour convinced the LCD is broken — because the contrast pot is sitting at the wrong value and the display is invisible. The display is working; you just can't see it.

Before you upload anything, apply power, twist the contrast pot slowly through its full range, and watch for that row of rectangles on the top line. If you get it, your power, backlight, contrast, and logic connections are all good. Only then run the sketch. Doing it in that order saves a lot of troubleshooting.

## Bonus: same display on the TI MSP430 Launchpad

The Energia IDE for the MSP430 Launchpad includes a LiquidCrystal library with the same API as Arduino's. The pin numbering on the Launchpad corresponds directly to Arduino digital pin numbers, so the same pin assignments work unchanged — digital pin 7 on the Launchpad wiring diagram is labeled P1.5, but Energia calls it `7` in code, same as Arduino.

Upload the same sketch via Energia, selecting **LaunchPad with MSP430G2553** as the board, and the LCD works identically. One notable difference: the sketch compiles to about 1,824 bytes on the MSP430 versus roughly 2,500 bytes on the Uno — the MSP430's toolchain squeezes more out of the same code.

One thing worth testing: the 1602 technically runs on 5V logic, but at 3.3V it still works — just dimmer, with noticeably slower refresh. At 3.3V you'll have to wind the contrast pot nearly to one extreme to see anything. It's not a great long-term operating condition for the display, but it's useful to know it won't instantly die if powered from a 3.3V rail.

## The Adafruit guide is still the canonical reference

The walkthrough in this video follows the Adafruit Learning System character LCD guide closely, and for good reason — it's thorough, well-illustrated, and has been accurate for over a decade. If you want a wiring diagram to print out or want the 8-bit mode alternative, that's the place to go. The [LiquidCrystal library reference](https://www.arduino.cc/reference/en/libraries/liquidcrystal/) on arduino.cc covers every available function once you're past the basic hello world.

## References and further reading

- [Adafruit Character LCDs Guide — Wiring a Character LCD](https://learn.adafruit.com/character-lcds/wiring-a-character-lcd) — the guide referenced throughout this video; still accurate
- [Hitachi HD44780 datasheet](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) — the authoritative source for timing, pin functions, and character ROM
- [Arduino LiquidCrystal library reference](https://www.arduino.cc/reference/en/libraries/liquidcrystal/) — full API documentation with examples for cursor, scrolling, custom characters
- [LiquidCrystal library source on GitHub](https://github.com/arduino-libraries/LiquidCrystal) — if you want to see how 4-bit mode is implemented in software
- [Energia for MSP430](https://energia.nu/) — the Wiring/Arduino-compatible IDE for TI LaunchPad boards
- [L7805 voltage regulator datasheet](https://www.st.com/resource/en/datasheet/l78.pdf) — useful context for the breadboard standalone section; input range 7–25V DC, 5V output
