---
title: 'Sainsmart LCD Keypad Shield for Arduino — What It Does and What It Costs You'
description: 'The Sainsmart LCD keypad shield stacks a 16×2 LCD and five navigation buttons onto an Arduino Uno in one click-together unit. The tradeoff: it consumes 8 pins and blocks access to D11–D13. Here is what you get, what you give up, and when it makes sense.'
pubDate: 'February 10 2012'
youtubeId: 'VS3v4T7TNPE'
heroImage: '../../assets/posts/sainsmart-lcd-keypad-arduino-shield/thumbnail.jpg'
tags: ['arduino', 'lcd', 'shield', 'tutorial', 'review']
---

An LCD shield solves one real problem: getting a 16×2 character display and a usable button interface onto an Arduino without dedicating a significant chunk of your project time to wiring. The Sainsmart LCD keypad shield — available on eBay for around $15 shipped — does exactly that. It stacks directly onto an Arduino Uno, the LCD and buttons work out of the box with the standard LiquidCrystal library, and there's nothing to solder.

The catch is the pin count. Shields are convenient but not free, and this one takes a meaningful bite.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## What's on the shield

The shield provides a 16×2 HD44780-compatible LCD display and five pushbuttons: left, right, up, down, and select. It also has a small trimmer potentiometer to adjust display contrast.

The LCD runs in 4-bit parallel mode using the standard LiquidCrystal library — no I²C adapter, no special library required. The five buttons use a resistor ladder, meaning they all share a single analog pin (A0) and produce different voltage readings depending on which button is pressed. The microcontroller reads the analog value and deduces which button is active.

## Pin usage

This is where the math gets uncomfortable:

| Shield function | Arduino pins used |
|-----------------|------------------|
| LCD (RS, EN, DB4–DB7) | D4, D5, D6, D7, D8, D9 |
| LCD backlight control | D10 |
| Buttons (all 5) | A0 |
| **Total** | **7 pins (D4–D10, A0)** |

D10 is used for backlight PWM control, though many applications just leave the backlight fully on. Technically that's 7 pins out of the Uno's 20 usable I/O pins dedicated to the shield.

More importantly: the shield's PCB physically covers D11, D12, and D13 without breaking them out to accessible headers. These pins are still electrically connected underneath, but there's no easy way to wire to them with the shield installed. D11–D13 are exactly the pins used for SPI communication (MOSI, MISO, SCK) and the hardware SPI hardware — so anything requiring SPI (SD cards, SPI sensors, many wireless modules) becomes awkward or impossible alongside this shield without modification.

Some versions of this shield have unpopulated header locations along the edge that can be soldered for access to a subset of pins. But it's not standard, and even then D11–D13 access is limited.

## Using the buttons

Reading the buttons requires `analogRead(A0)` and a comparison against known voltage thresholds. The resistor ladder produces roughly these ranges on a 5V Uno:

| Button | Analog value (approx.) |
|--------|----------------------|
| Right | ~0 |
| Up | ~144 |
| Down | ~329 |
| Left | ~505 |
| Select | ~741 |
| None | ~1023 |

A typical reading function checks ranges rather than exact values to account for ADC noise:

```cpp
int readButton() {
  int val = analogRead(A0);
  if (val < 50)   return 1;  // Right
  if (val < 195)  return 2;  // Up
  if (val < 380)  return 3;  // Down
  if (val < 555)  return 4;  // Left
  if (val < 790)  return 5;  // Select
  return 0;                  // None
}
```

The thresholds vary slightly between shield revisions and individual units. If a button registers as the wrong one, adjust the threshold for that range.

## Sample sketch

```cpp
#include <LiquidCrystal.h>

// RS, EN, DB4, DB5, DB6, DB7
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  lcd.begin(16, 2);
  lcd.print("Press a button:");
}

void loop() {
  int val = analogRead(A0);
  lcd.setCursor(0, 1);

  if (val < 50)        lcd.print("RIGHT  ");
  else if (val < 195)  lcd.print("UP     ");
  else if (val < 380)  lcd.print("DOWN   ");
  else if (val < 555)  lcd.print("LEFT   ");
  else if (val < 790)  lcd.print("SELECT ");
  else                 lcd.print("NONE   ");
}
```

The trailing spaces after each label prevent leftover characters when a longer label is replaced by a shorter one — "SELECT" replaced by "UP" would leave "UPECT" without them.

## When this shield makes sense

The LCD keypad shield is a good fit for a single-purpose control panel: a menu-driven settings interface, a simple data display with navigation, a standalone instrument. If your project is fundamentally about displaying information and responding to a handful of button presses — and doesn't need SPI or more than a few additional digital pins — the shield is a clean solution that ships ready to use.

Where it doesn't make sense: projects that need the SPI pins for SD cards or radio modules, projects that will eventually grow to need more I/O, or any build where space and pin count are at a premium. For those, an I²C LCD (just A4 and A5, leaving everything else free) is a better foundation even though it requires a slightly more involved library setup.

## References and further reading

- [EF Robot LCD keypad shield documentation](https://www.dfrobot.com/wiki/index.php/LCD_KeyPad_Shield_For_Arduino_SKU:_DFR0009) — the original documentation source for pin assignments and button threshold values (DFRobot is the originator; Sainsmart versions are compatible clones)
- [Arduino LiquidCrystal library reference](https://www.arduino.cc/reference/en/libraries/liquidcrystal/) — `begin()`, `print()`, `setCursor()`, `clear()` — all standard and unchanged for this shield
- [Arduino `analogRead()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) — the 0–1023 range and resolution details relevant to button threshold reading
- [I²C LCD alternative](/blog/find-i2c-address-arduino) — the two-pin I²C approach that consumes far fewer resources if you don't need the integrated buttons
