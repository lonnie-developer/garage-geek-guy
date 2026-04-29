---
title: 'How to Use a Real Time Clock with Arduino — DS1307 RTC Tutorial'
description: 'The Arduino loses track of time the moment you unplug it. The DS1307 RTC module fixes that with a coin-cell backup and an I2C interface simple enough to share a bus with your LCD. Full walkthrough from address scan to LCD display.'
pubDate: 'August 22 2021'
youtubeId: 'KgqMOPErWjk'
heroImage: '../../assets/posts/arduino-real-time-clock-ds1307-rtc/thumbnail.jpg'
tags: ['arduino', 'rtc', 'ds1307', 'i2c', 'tutorial']
---

The Arduino Uno runs on a crystal oscillator that's accurate to maybe a few seconds per day under ideal conditions. That would be fine if you could just leave it powered on forever, but you can't — the moment you unplug it, the sketch stops, the counter resets, and any time value you set in software is gone. Next power-on, you're back to zero.

This is why real-time clock modules exist. The DS1307 is the approachable, widely-available option that shows up on virtually every beginner-parts list: it talks I2C, it comes with a CR2032 coin-cell backup that keeps it ticking through power loss, and it doesn't ask you to do anything complicated. Set the time once, unplug everything, plug it back in a week later, and the clock is still right.

This post walks through wiring the DS1307 to an Arduino, finding its I2C address with a scanner sketch, installing the right libraries, setting the time, reading it back, and then extending the project to display the live time on an I2C LCD — with both devices sharing the same two-wire bus.

## What an RTC actually is

The CR2032 on the back of the DS1307 module isn't cosmetic. It's the same coin cell format you'd find in a PC motherboard's BIOS — which keeps time the exact same way. A tiny low-power oscillator running off the battery keeps incrementing the clock registers inside the DS1307 chip regardless of whether anything else on the board is powered. When your Arduino wakes up and asks the DS1307 "what time is it?", the DS1307 has a real answer.

Without the RTC, you'd have two options: accept that your Arduino clock resets every power cycle, or use millis() and pray that your USB cable never gets unplugged. Neither is satisfying if you actually need to know the time.

## What the DS1307 connects to

The DS1307 is an I2C device. I2C uses two signal lines — SDA (data) and SCL (clock) — plus power and ground. On an Arduino Uno, SDA is analog pin A4 and SCL is analog pin A5. The module itself breaks them out as labeled pins, so the wiring is four wires total:

| DS1307 pin | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |

The square-wave output pin on some DS1307 modules can be left disconnected for basic timekeeping. We're not using it here.

## Step 1: Find the I2C address

Before writing any RTC-specific code, run the I2C scanner sketch from [arduino.cc](https://playground.arduino.cc/Main/I2cScanner/) to confirm the module is wired up and responding. Upload the sketch, open the Serial Monitor at 9600 baud, and look for something like:

```
I2C device found at address 0x68
```

`0x68` is the default address for the DS1307 — and for the DS3231 as well, which is why you can sometimes swap one for the other without changing your code. If you see no device found, check power, check SDA/SCL wiring, and make sure you don't have two I2C devices at the same address fighting each other.

## Step 2: Install the libraries

Two libraries are needed and neither is included by default in the Arduino IDE.

**DS1307RTC** — the hardware driver for the chip. Find it in Library Manager (`Sketch → Include Library → Manage Libraries`) and search for `DS1307RTC`. Install it.

**Time** (by Paul Stoffregen) — the DS1307RTC library depends on this for its time-manipulation functions. Search for `TimeLib` or `Time` and install it. The IDE should offer to install it automatically when you install the first library, but if it doesn't, go find it manually. The error `time library.h: No such file or directory` means this one is missing.

Once both are installed, navigate to `File → Examples → DS1307RTC` to find two ready-made sketches: `SetTime` and `ReadTest`.

## Step 3: Set the time

Upload `SetTime`. This sketch does something clever: it reads the current time from your computer (via the compilation timestamp embedded in the sketch) and writes it to the RTC. The first time you run it, the DS1307's registers get populated with actual time.

One practical note: there's a small window between compiling and uploading where the sketch's embedded time drifts from actual time — usually a few seconds to a minute depending on how fast your computer and cable are. For most projects this is fine. For anything that needs sub-minute accuracy, you'll want to tweak the approach.

After uploading `SetTime`, power-cycle the Arduino or swap back to a reading sketch. The RTC now has a running clock.

## Step 4: Read it back

Upload `ReadTest`. Open Serial Monitor at 9600 baud. You should see the current time printing once per second:

```
2021/08/22 14:35:07
2021/08/22 14:35:08
2021/08/22 14:35:09
```

Now the real test: pull power, wait a moment, plug it back in, open the Serial Monitor again. The time should pick up where it left off, not reset to midnight. If it does, the coin cell is working.

## Step 5: Adding an I2C LCD

Here's where I2C starts paying dividends. A standard 16×2 LCD in parallel mode needs six Arduino pins. An I2C backpack adapter on the same LCD needs two — SDA and SCL. The same two pins the RTC is already using.

That's the beauty of I2C: it's a bus, not a point-to-point connection. Both devices can share the same SDA and SCL lines simultaneously, because each one has a unique address. You can extend them both off a small breadboard that connects to the Arduino's A4 and A5 headers. Same lines, no conflict.

Wire the LCD's SDA and SCL to the same rails as the DS1307. Give both modules their own VCC and GND connections. That's the hardware done.

For the software, install the `LiquidCrystal_I2C` library if you haven't already. Then adapt the ReadTest sketch to send its output to the LCD instead of the Serial Monitor. The cleanest way is a find-and-replace: swap every `Serial.print` for `lcd.print`, add the LCD initialization in `setup()`, and add a `lcd.clear()` at the start of each loop iteration to prevent old digits from persisting.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DS1307RTC.h>
#include <TimeLib.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
}

void loop() {
  tmElements_t tm;
  if (RTC.read(tm)) {
    lcd.setCursor(0, 0);
    lcd.print(tm.Hour);
    lcd.print(':');
    if (tm.Minute < 10) lcd.print('0');
    lcd.print(tm.Minute);
    lcd.print(':');
    if (tm.Second < 10) lcd.print('0');
    lcd.print(tm.Second);
  }
  delay(1000);
}
```

The leading-zero check (`if (tm.Minute < 10) lcd.print('0')`) is the detail that makes the display look right. Without it, 9 minutes past the hour displays as "14:9:07" instead of "14:09:07". Nobody wants that.

## The result

Pull power. Plug it back in. The LCD comes up showing the correct time immediately. The coin cell on the DS1307 handled the gap.

For a project that runs unattended — a clock, a data logger with timestamps, anything that needs to know when "now" is — this is the minimum useful hardware: one RTC, one coin cell, two wires shared with whatever display or output you've already got. The DS1307 isn't the most accurate RTC available (the DS3231 drifts less and doesn't need external pull-up resistors), but for most Arduino projects it's more than good enough and considerably cheaper.

## References and further reading

- [DS1307 datasheet](https://datasheets.maximintegrated.com/en/ds/DS1307.pdf) — Maxim Integrated; full register map and electrical specs
- [Arduino I2C Scanner sketch](https://playground.arduino.cc/Main/I2cScanner/) — useful for debugging any I2C device
- [DS1307RTC library documentation](https://www.pjrc.com/teensy/td_libs_DS1307RTC.html) — PJRC; explains the library's API in detail
- [Time library by Paul Stoffregen](https://github.com/PaulStoffregen/Time) — the dependency the DS1307RTC library relies on
- [LiquidCrystal_I2C library](https://github.com/johnrickman/LiquidCrystal_I2C) — the I2C backpack driver used in this project
- [I2C tutorial — how the protocol works](https://learn.sparkfun.com/tutorials/i2c/all) — SparkFun; good conceptual background before wiring multiple devices on the same bus
