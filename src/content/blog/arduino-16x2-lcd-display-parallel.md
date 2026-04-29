---
title: 'How to Use a 16x2 LCD Display with Arduino (Parallel Interface)'
description: 'A full wiring walkthrough for the HD44780 character LCD in 4-bit parallel mode — all 16 pins explained, the contrast pot wired up, and the LiquidCrystal HelloWorld sketch running.'
pubDate: 'November 10 2018'
youtubeId: 'YHNeLmUJTlQ'
heroImage: '../../assets/posts/arduino-16x2-lcd-display-parallel/thumbnail.jpg'
tags: ['arduino', 'lcd', 'display', 'hd44780', 'liquidcrystal', 'tutorial']
---

The 16x2 character LCD is one of those components that shows up in roughly every second entry-level Arduino kit, gets glanced at, and then sits in a drawer for six months because the wiring looks intimidating. Sixteen pins. A potentiometer you apparently need. Library calls with a bunch of arguments whose meaning isn't obvious. It all conspires to make this one of the most frequently skipped-over parts of any starter kit, which is a shame — because once it's wired up, it's one of the most satisfying pieces of output you can add to a project.

This post is the parallel wiring version: all 16 pins explained, the contrast potentiometer wired correctly, and the Arduino HelloWorld example running. If you're specifically looking for the I2C backpack version — where you get away with only four wires instead of a dozen — that's a separate walkthrough. Start here first, at least once. Doing it the hard way helps you appreciate the easy way.

## What you're working with

The 1602 display (16 columns, 2 rows) is almost certainly built around a Hitachi HD44780 controller chip or a compatible clone. The HD44780 has been the standard character LCD controller since 1987. Every Sunfounder, Elegoo, SainSmart, and no-name module from AliExpress or eBay uses the same pin order and the same communication protocol. This means the [LiquidCrystal library](https://docs.arduino.cc/libraries/liquidcrystal/) works with all of them, and the wiring you learn here applies to essentially every character LCD you'll ever encounter — including the larger 2004 (20x4) displays that use the same HD44780 interface.

The display has 16 pins in a row. Most tutorials look at those 16 pins and immediately make the wiring seem harder than it is. So let's break it down honestly: five of those pins are just power and contrast control, four of them aren't even connected in 4-bit mode, and you only need six Arduino I/O pins for everything else. The "16 pins" sounds like a lot until you realize the actual work is six connections.

## What you'll need

- Arduino Uno (or any 5V Arduino)
- 16x2 character LCD (HD44780 or compatible)
- 10kΩ potentiometer (for contrast control)
- Breadboard
- Jumper wires

## Wiring: power and contrast first

Start with the power connections and the contrast potentiometer. Getting these right first means you can verify the display is working before you've committed to any of the data connections.

The LCD pinout from left to right:

| Pin | Name | What it does |
|-----|------|-------------|
| 1 | VSS | Ground |
| 2 | VCC | 5V |
| 3 | VO | Contrast — connect to center wiper of pot |
| 4 | RS | Register select — Arduino digital pin 12 |
| 5 | RW | Read/Write — tie to GND (we're always writing) |
| 6 | E | Enable — Arduino digital pin 11 |
| 7–10 | D0–D3 | Data bits 0–3 — not connected in 4-bit mode |
| 11 | D4 | Data bit 4 — Arduino digital pin 5 |
| 12 | D5 | Data bit 5 — Arduino digital pin 4 |
| 13 | D6 | Data bit 6 — Arduino digital pin 3 |
| 14 | D7 | Data bit 7 — Arduino digital pin 2 |
| 15 | A | Backlight anode — 5V |
| 16 | K | Backlight cathode — GND |

The potentiometer wires up with its two outer pins going to 5V and GND, and its center wiper pin going to VO (LCD pin 3). When you first connect power, the backlight will come on immediately — pins 15 and 16 power it independently from the logic. That's your sign that the wiring is at least partially correct. The display won't show readable text yet because the contrast isn't set, but you'll see a row of dark blocks in the top row when you turn the potentiometer to maximum contrast. That's the HD44780 showing every character cell as filled. Back off the pot until the blocks are visible but not fully black, and you're in the right range.

RW is wired to ground because we never read from the display — we only write to it. Connecting it to GND permanently saves one I/O pin on the Arduino. The LiquidCrystal library doesn't need it.

D0 through D3 are left unconnected. The HD44780 can run in 8-bit mode (all eight data pins) or 4-bit mode (only D4–D7). The LiquidCrystal library uses 4-bit mode by default. It just sends each byte as two 4-bit chunks (nibbles), toggling the Enable line between them. You lose nothing except a few microseconds of speed per character, which matters not at all for anything humans can perceive.

## The data connections

```
LCD D4 → Arduino pin 5
LCD D5 → Arduino pin 4
LCD D6 → Arduino pin 3
LCD D7 → Arduino pin 2
LCD RS → Arduino pin 12
LCD E  → Arduino pin 11
```

The note-worthy thing here is that D4 goes to Arduino pin 5 and D5 goes to Arduino pin 4 — they cross. That's not a typo; it's just how the Arduino HelloWorld example is written. The LiquidCrystal library only cares that you tell it which pin is which in code, so the physical mapping doesn't have to be numerically ordered. If the crossed numbers bother you, you can use any digital pins you want as long as you update the `LiquidCrystal` constructor to match.

## The code

Install the LiquidCrystal library if it isn't already (it ships with the Arduino IDE, so it usually is). The HelloWorld example is under File → Examples → LiquidCrystal → HelloWorld.

```cpp
#include <LiquidCrystal.h>

// Initialize: LiquidCrystal(rs, en, d4, d5, d6, d7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2);       // 16 columns, 2 rows
  lcd.print("hello, world!");
}

void loop() {
  lcd.setCursor(0, 1);    // column 0, row 1 (second row)
  lcd.print(millis() / 1000);  // seconds since reset
}
```

Upload it. If the contrast potentiometer is dialed in, you'll see "hello, world!" on the first row and a counting number of seconds on the second. If you get squares instead of characters, adjust the pot — you're either too high or too low on contrast.

The gotcha here is the contrast potentiometer. A display that shows nothing, or shows only black blocks with no text, is almost always a contrast issue rather than a wiring problem. Before assuming something is wrong with your connections, turn the pot slowly through its full range. The readable zone is narrow and it's not necessarily in the middle.

## A word on the wiring volume

Yes, it's a lot of wires. That's the trade-off for parallel. When you see tutorials for the I2C module — the same LCD but with a small PCB backpack that reduces the wiring to four pins — this is the before picture. The I2C version uses an I/O expander chip (usually a PCF8574) that serializes the communication, sending the same data over a two-wire interface instead of six parallel lines. It adds a few dollars to the BOM and a library import to your sketch in exchange for eight fewer wires. For bench prototyping, parallel is fine. For a project where wiring is a headache or you're short on I/O pins, the I2C backpack is worth it.

## Where this fits in your projects

The 16x2 LCD is most useful for status display and live debugging — showing sensor readings, state variables, error codes, whatever you'd otherwise be watching in the serial monitor. The big practical advantage over `Serial.print()` is that it works without a computer attached. A standalone Arduino project can print its own status to a display rather than requiring a serial connection to tell you what it's doing.

It also draws more current than an OLED or I2C display, and it needs that potentiometer (or a fixed resistor in production). But for a breadboard prototype or a project where you have a 5V rail to spare, it's hard to beat the price — these modules cost almost nothing, and the LiquidCrystal library is mature and well-documented.

## References and further reading

- [Arduino HelloWorld example (official)](https://docs.arduino.cc/built-in-examples/displays/LiquidCrystalHelloWorld/) — the sketch used in this walkthrough
- [LiquidCrystal library reference](https://docs.arduino.cc/libraries/liquidcrystal/) — all available methods: `setCursor`, `print`, `clear`, `createChar`, etc.
- [In-depth 16x2 LCD tutorial — Last Minute Engineers](https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/) — thorough reference including custom characters
- [HD44780 datasheet (Hitachi)](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) — the original 1987 controller spec; surprisingly readable
- [LiquidCrystal_I2C library — Arduino Library Reference](https://reference.arduino.cc/reference/en/libraries/liquidcrystal-i2c/) — if you want to step up to the 4-wire version next
