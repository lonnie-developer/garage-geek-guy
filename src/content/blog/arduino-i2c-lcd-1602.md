---
title: 'How to Use a 1602 I2C Serial LCD Display with Arduino'
description: 'The parallel 1602 LCD needs 12 wires and a headache. The I2C version needs four. Here is how to wire it, install the library, and get text on screen in under ten minutes.'
pubDate: 'August 03 2021'
youtubeId: 'BJ93XCcD858'
heroImage: '../../assets/posts/arduino-i2c-lcd-1602/thumbnail.jpg'
tags: ['arduino', 'lcd', 'i2c', 'display', 'tutorial', 'beginner']
---

Wiring up a 1602 LCD the traditional way — parallel interface, direct to an Arduino — is a rite of passage that almost everyone goes through exactly once. Twelve connections, a contrast potentiometer to fiddle with, a pinout diagram you'll reference six times, and the nagging feeling that you're using half your Arduino's I/O pins just to print "hello world." The display works, eventually, and then you spend the rest of the project annoyed that you can't easily add anything else.

The I2C version of the same display skips most of that. Four wires — power, ground, SDA, SCL — and the same `LiquidCrystal` commands you already know. If you're just getting into displays, start here and skip the parallel version entirely.

## What the 1602 LCD actually is

The 1602 is a character LCD — it displays text, not arbitrary graphics. The "1602" in the name tells you its size: 16 characters wide, 2 rows, for 32 character positions total. It's based on the HD44780 controller chip (or a compatible clone), which has been the de facto standard for character LCD modules since Hitachi introduced it in the 1980s. Virtually every `LiquidCrystal` library ever written targets this controller.

The display has a backlight — typically blue or green with white characters — and a potentiometer on the back to adjust contrast. Out of the box, the contrast is often set wrong and the display looks blank even when it's working; adjusting that pot is usually the first debugging step.

The I2C module is a small PCB — sometimes called a "serial backpack" or "I2C adapter" — that bolts onto the back of the LCD. It replaces the 12-line parallel connection with a 4-wire I2C interface. The module also contains the contrast potentiometer and a jumper to enable or disable the backlight. You'll pay a dollar or two more for the I2C version versus the bare display, and it is absolutely worth it.

## What you'll need

- 1602 LCD with I2C backpack module (available as a combined unit, or as separate LCD + module to solder together)
- Arduino Uno, Nano, or similar
- Four male-to-female jumper wires (the dupont style)
- USB cable and the Arduino IDE

That's it. No breadboard required for the display itself, though you may want one if you're building out a larger project alongside it.

## Installing the library

The I2C LCD uses a library called `LiquidCrystal_I2C`. Open the Arduino IDE, go to `Tools → Manage Libraries`, and search for `LiquidCrystal_I2C`. Several versions will appear — they all work similarly. Install whichever looks most recently maintained.

Do this before you wire anything. Library installation is fast and it's easier to troubleshoot one thing at a time.

## Wiring it up

The I2C backpack has four pins:

- **GND** → Arduino GND
- **VCC** → Arduino 5V
- **SDA** → Arduino A4 (on Uno) or the dedicated SDA pin
- **SCL** → Arduino A5 (on Uno) or the dedicated SCL pin

That's the whole wiring job. Male-to-female dupont wires are the easiest way to connect a module like this — one end plugs into the backpack's female header, the other pushes into the Arduino's pins. If you have a Nano or a board with dedicated SDA/SCL pins labeled on the board, use those; otherwise A4 and A5 on the Uno are the hardware I2C bus.

## The I2C address

The I2C backpack has a default address of `0x27`. Most modules ship this way — all three address-selection jumpers on the back of the board left open. If you have multiple I2C devices on the same bus and need to run two LCD modules, you can change the address by soldering the jumpers; with all three closed the address becomes `0x3F`. For a single LCD, just use `0x27` and don't worry about it.

If you're unsure what address your module is actually at, upload an [I2C scanner sketch](https://playground.arduino.cc/Main/I2cScanner/) — it'll print every address that responds on the bus and you can go from there.

## The code

Here's a minimal Hello World sketch:

```cpp
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // address, columns, rows

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.print("Hello World");
}

void loop() {
  // nothing here for a static display
}
```

Upload this and you should see "Hello World" on the top row. If the display is blank, try adjusting the contrast potentiometer on the back of the I2C module — turn it slowly until characters appear. A completely blank display on first boot is almost always a contrast issue, not a wiring or code problem.

## Placing text with setCursor

The `lcd.print()` call starts wherever the cursor last was. To put text at a specific position, use `lcd.setCursor(column, row)` first — column and row are both zero-indexed, so the top-left corner is `(0, 0)` and the start of the second row is `(0, 1)`.

Here's a running counter that shows how to update the display dynamically:

```cpp
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Counter:");
}

void loop() {
  static int count = 0;
  lcd.setCursor(0, 1);
  lcd.print(count);
  count++;
  delay(200);
}
```

One thing to watch here: `lcd.print()` doesn't erase old content, it just writes over it. If `count` goes from 9 to 10, the display shows `10` — fine. If it goes from `100` to `99`, the display shows `990` because the old third digit is still there. The clean fix is `lcd.clear()` before each update, but that causes a visible flicker. A better approach for numeric displays is to print with enough padding to always overwrite the previous value, or use `lcd.print("   ")` to blank the field first.

## The gotcha: display is blank even when code is running

The most common first-boot problem is a display that's fully functional but showing nothing visible because the contrast is set too low. The potentiometer on the back of the I2C module controls this. Turn it with a small screwdriver while the Arduino is running and text is printing — you should see characters fade in as you find the right position. This is not a bug and it's not a wiring error. It's just the pot shipped at the wrong setting.

Second most common issue: wrong I2C address. If the library can't find the module at `0x27`, nothing prints. Run the I2C scanner sketch, confirm what address your module is actually at, and update the `LiquidCrystal_I2C lcd(...)` constructor to match.

## Where to go from here

The 1602 is a capable display for status readouts, sensor values, menu systems, and anything else that fits in 32 characters. The `LiquidCrystal_I2C` library also supports custom characters — you can define up to 8 symbols using a 5×8 pixel grid, which is enough for basic icons or progress-bar segments. A Google search for "LiquidCrystal_I2C custom characters" will get you a character builder and the `createChar()` syntax.

If you need more screen real estate, the next logical step is the 2004 LCD (20 characters × 4 rows, also available with an I2C backpack) or a graphical display like the 0.96" OLED. The OLED gives you full pixel control at a comparable price and is worth considering if your project needs anything beyond plain text.

## References and further reading

- [Arduino LiquidCrystal library reference](https://docs.arduino.cc/libraries/liquidcrystal/) — the parallel-interface version; commands are nearly identical
- [HD44780 datasheet (PDF)](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) — the controller chip underneath most 1602 displays
- [I2C scanner sketch (Arduino Playground)](https://playground.arduino.cc/Main/I2cScanner/) — essential debugging tool for any I2C project
- [Adafruit guide: character LCDs](https://learn.adafruit.com/character-lcds) — covers both parallel and I2C wiring in depth
- [Last Minute Engineers: I2C LCD tutorial](https://lastminuteengineers.com/i2c-lcd-arduino-tutorial/) — detailed library reference with address-scanning walkthrough
