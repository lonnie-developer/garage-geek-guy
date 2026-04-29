---
title: 'How to Use a DS3231 Real Time Clock with Arduino — I2C RTC + LCD Display Tutorial'
description: 'The DS3231 is the upgrade from the DS1307: a temperature-compensated RTC that drifts only a few seconds per year and needs no external pull-up resistors. Full walkthrough of wiring, library setup, time-setting, and displaying formatted time on an I2C LCD.'
pubDate: 'November 14 2018'
youtubeId: 'N2Zc_FTrUn8'
heroImage: '../../assets/posts/arduino-ds3231-real-time-clock-lcd-i2c/thumbnail.jpg'
tags: ['arduino', 'rtc', 'ds3231', 'i2c', 'lcd', 'tutorial']
---

Every Arduino has an internal timer. It counts millis from the moment you apply power and resets to zero every time you unplug it. That's fine for measuring intervals — how long since this button was last pressed, how many seconds until the next sensor reading — but it's useless for knowing what time it actually is. For that, you need an external real-time clock.

The DS3231 is the good one. The DS1307 is cheaper and more common in beginner tutorials, but the DS3231 uses a temperature-compensated crystal oscillator — which means it automatically corrects for the frequency drift that temperature changes cause in a plain crystal. The practical difference: the DS1307 might drift by a minute or two per month. The DS3231 typically drifts a few seconds per year. For most Arduino projects, either is overkill. But if you're going to add an RTC, you might as well add the better one, and they cost about the same.

This post covers wiring the DS3231 to an Arduino Uno, installing the Adafruit RTClib library, setting the time, reading it back in `loop()`, and displaying it on an I2C LCD with properly formatted leading zeros. The whole build uses exactly two Arduino I/O pins for both the RTC and the display — because both are I2C devices sharing the same bus.

## The hardware

The DS3231 breakout board used here is the cheap blue-PCB variety sold on eBay and Amazon for a few dollars. It breaks out VCC, GND, SDA, SCL, and a 32KHz square-wave output (which we won't use). It also has a CR2032 coin-cell holder on the back — same size as the battery in an old PC motherboard's BIOS. That battery keeps the clock ticking through power loss. A fresh CR2032 will typically run the RTC for years.

The I2C LCD in this build is a 16×2 character display with an I2C backpack already soldered on. If yours has the backpack, it'll show four pins: VCC, GND, SDA, SCL. No individual register select or enable wires.

Both devices are I2C, which means they share the same two-wire bus.

### Wiring

Connect both modules to the same SDA and SCL lines on the Arduino:

| Module | Pin | Arduino Uno |
|---|---|---|
| DS3231 | VCC | 5V |
| DS3231 | GND | GND |
| DS3231 | SDA | A4 |
| DS3231 | SCL | A5 |
| I2C LCD | VCC | 5V |
| I2C LCD | GND | GND |
| I2C LCD | SDA | A4 |
| I2C LCD | SCL | A5 |

The I2C bus supports multiple devices on the same two lines. The DS3231's default address is `0x68` and the LCD backpack is typically `0x27` (or `0x3F` on some variants). They won't collide.

## Installing the library

The library is Adafruit's fork of the G Labs RTClib. Search for `RTClib` in the Arduino IDE Library Manager (`Sketch → Include Library → Manage Libraries`). Install the one by Adafruit. It supports the DS3231 along with the DS1307, DS1302, and a few others.

If you prefer to install manually: go to [github.com/adafruit/RTClib](https://github.com/adafruit/RTClib), click Code → Download ZIP, then install it through `Sketch → Include Library → Add .ZIP Library`.

You'll also need the `LiquidCrystal_I2C` library for the display. Same process — find it in Library Manager.

The DS3231 compatibility note from the library docs: it works with the Atmega328P (Uno, Nano, Pro Mini) and Atmega 2560 (Mega). If you're on a different platform, check the library's issue tracker.

## Setting the time

```cpp
#include <RTClib.h>

RTC_DS3231 rtc;

void setup() {
  Wire.begin();
  rtc.begin();

  // Set the time — run this once, then comment it out and re-upload
  rtc.adjust(DateTime(2018, 11, 14, 14, 30, 0));
  // year, month, day, hour (24h), minute, second
}
```

The `rtc.adjust()` call writes the date and time to the DS3231's registers. Run this once, verify the clock is running, then comment out the adjust line and re-upload — otherwise every power cycle resets your clock back to the hardcoded time. 

One easy shortcut that avoids hardcoding: `rtc.adjust(DateTime(F(__DATE__), F(__TIME__)))`. This uses the compile-time timestamp from your computer, so whatever time it is when you hit Upload is approximately what gets set. The "approximately" comes from compilation and upload time adding a few seconds of drift, which you can compensate for manually if it matters.

You can also add a guard so the adjust only runs if the RTC lost power:

```cpp
if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}
```

`rtc.lostPower()` returns true if the backup battery ran down or was never connected. Good practice for any deployed project.

## Reading the time in loop()

The `DateTime` object returned by `rtc.now()` exposes individual fields for hour, minute, second, day, month, and year. Call it in `loop()`, not `setup()` — you need a fresh reading every iteration.

```cpp
void loop() {
  DateTime now = rtc.now();

  Serial.print(now.hour());
  Serial.print(':');
  Serial.print(now.minute());
  Serial.print(':');
  Serial.println(now.second());

  delay(1000);
}
```

This works, but produces ugly output when any value is under 10 — `9:3:7` instead of `09:03:07`. Fix that before moving to the LCD display.

## The leading-zero fix

This is the gotcha that makes every first-time RTC clock display look wrong. `now.minute()` returns an integer — 3, not "03". The LCD (or Serial Monitor) will faithfully print just the one digit.

The fix is a conditional print before each field:

```cpp
if (now.hour() < 10) lcd.print('0');
lcd.print(now.hour());
lcd.print(':');
if (now.minute() < 10) lcd.print('0');
lcd.print(now.minute());
lcd.print(':');
if (now.second() < 10) lcd.print('0');
lcd.print(now.second());
```

Not elegant, but clear. An alternative is `sprintf()` with `%02d` formatting if you want a one-liner — though on small Arduinos you'll want to check that `sprintf` is available in your build.

## Putting it together on the LCD

The full sketch, combining both I2C devices:

```cpp
#include <Wire.h>
#include <RTClib.h>
#include <LiquidCrystal_I2C.h>

RTC_DS3231 rtc;
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Wire.begin();
  rtc.begin();
  lcd.init();
  lcd.backlight();

  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  DateTime now = rtc.now();

  lcd.setCursor(0, 0);

  if (now.hour() < 10) lcd.print('0');
  lcd.print(now.hour());
  lcd.print(':');
  if (now.minute() < 10) lcd.print('0');
  lcd.print(now.minute());
  lcd.print(':');
  if (now.second() < 10) lcd.print('0');
  lcd.print(now.second());

  delay(1000);
}
```

`lcd.setCursor(0, 0)` anchors the output to the top-left corner on every loop iteration, so the display updates in place rather than scrolling. The `lcd.init()` and `lcd.backlight()` calls in `setup()` wake the display and turn on the backlight.

Once this is working, the video recommends refactoring the print logic into a helper function — keeps `loop()` readable and makes it easier to add a date display on row 1 later.

## Verifying the backup works

The coin cell is the whole point of having an RTC. Test it before you trust it: upload the sketch, confirm the clock is running on the LCD, then pull USB power completely. Wait 30 seconds. Plug it back in. The clock should pick up exactly where it left off, not reset. If it resets, your coin cell is dead or missing — swap it for a fresh CR2032 and repeat the time-set step.

## When to reach for a DS3231 vs. a DS1307

The DS3231 is better in almost every way: more accurate, built-in pull-up resistors, available temperature reading as a bonus, and the same or lower price. The main reason to use a DS1307 is if you already have one on the bench. For any new project, start with the DS3231.

If even the DS3231's accuracy isn't enough — like if you're building a clock that needs to stay synchronized across multiple devices over weeks or months — that's when you reach for NTP over WiFi and an ESP8266/ESP32. But for the vast majority of projects that just need "what time is it without resetting every power cycle," the DS3231 and a CR2032 will outlast everything else in the enclosure.

## References and further reading

- [DS3231 datasheet](https://datasheets.maximintegrated.com/en/ds/DS3231.pdf) — Maxim Integrated; includes the register map and accuracy specs
- [Adafruit RTClib on GitHub](https://github.com/adafruit/RTClib) — source, installation instructions, and examples
- [Adafruit RTClib API reference](https://adafruit.github.io/RTClib/html/index.html) — full list of available methods on `DateTime` and `RTC_DS3231`
- [CR2032 battery lifespan in RTCs](https://electronics.stackexchange.com/questions/303/cr2032-battery-lifetime) — Stack Exchange discussion on how long a coin cell actually lasts in standby
- [I2C bus basics](https://learn.sparkfun.com/tutorials/i2c/all) — SparkFun; helpful if you're wiring more than two I2C devices on the same bus
- [LiquidCrystal_I2C library](https://github.com/johnrickman/LiquidCrystal_I2C) — the I2C LCD driver used in this project
- [Companion video: connecting multiple I2C devices to one Arduino](https://www.youtube.com/watch?v=nEySekIIxpw)
