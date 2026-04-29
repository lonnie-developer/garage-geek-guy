---
title: 'How to Connect Multiple LCD Displays to One Arduino'
description: 'The PCF8574 I2C backpack on cheap 1602 LCDs has three address jumpers — A0, A1, A2 — giving you 8 unique addresses. That means 8 LCD displays on two Arduino pins. Here is the address chart, the jumper settings, and the sketch to drive all of them.'
pubDate: 'August 21 2021'
youtubeId: 'Jj2KOFw12Kc'
heroImage: '../../assets/posts/multiple-lcd-displays-arduino/thumbnail.jpg'
tags: ['arduino', 'lcd', 'i2c', 'tutorial']
---

One of the nicer properties of I²C is that you can hang a lot of devices on just two wires. A 1602 LCD with an I²C backpack takes SDA, SCL, power, and ground — that's it. Add a second LCD: same SDA, same SCL, just tie it to the same bus. Add eight: still two pins on the Arduino.

The catch is that every device on an I²C bus needs a unique address. Out of the box, all PCF8574-backed LCDs ship with the same default address (0x27). Put two of them on the same bus without changing anything and they'll both respond to every command simultaneously, rendering the setup useless. The fix is built right into the backpack board.

## The address jumpers

Flip any I²C LCD backpack over and you'll find three solder jumpers labeled **A0**, **A1**, and **A2**. These set the lower three bits of the PCF8574's 7-bit I²C address. The base address for the PCF8574 is 0x20; the A0/A1/A2 bits add to it:

| A2 | A1 | A0 | Address |
|----|----|----|---------|
| open | open | open | 0x27 (default) |
| open | open | closed | 0x26 |
| open | closed | open | 0x25 |
| open | closed | closed | 0x24 |
| closed | open | open | 0x23 |
| closed | open | closed | 0x22 |
| closed | closed | open | 0x21 |
| closed | closed | closed | 0x20 |

"Open" means the jumper pad is unsoldered (no connection). "Closed" means you've bridged the pad with a small blob of solder. Eight combinations, eight unique addresses — enough for eight LCD displays on a single Arduino I²C bus.

## Setting up eight displays

Before wiring anything, solder the address jumpers on each LCD according to the table above. Leaving one at 0x27 (default, all open) and setting the remaining seven gives you addresses 0x20 through 0x27. The most time-consuming part of this build is the jumper work — a temperature-controlled iron and fine solder make it much faster.

**Wiring:** connect all eight LCDs to a shared breadboard bus. Power (5V) and GND to a common rail, then SDA and SCL from the Arduino to shared rails that each LCD's SDA and SCL connect to. The Arduino Uno's I²C pins are **A4 (SDA)** and **A5 (SCL)**. No additional pull-up resistors needed — the PCF8574 backboards include onboard pull-ups.

```
Arduino A4 (SDA) ─── shared SDA rail ─── all 8 LCD SDA pins
Arduino A5 (SCL) ─── shared SCL rail ─── all 8 LCD SCL pins
Arduino 5V       ─── shared power rail ─── all 8 LCD VCC pins
Arduino GND      ─── shared ground rail ─── all 8 LCD GND pins
```

## Verify addresses before writing the sketch

Before writing display code, run an I²C scanner to confirm all eight addresses are responding correctly. The [I²C scanner sketch](/blog/find-i2c-address-arduino) loops through all 127 possible addresses and prints any that respond. If you see all eight expected addresses, the wiring and jumper settings are correct. If one is missing, check the jumper solder joints and connections on that LCD.

## The sketch

With eight displays confirmed, the LiquidCrystal_I2C library handles the rest. Install it via the Arduino Library Manager if you don't already have it (search "LiquidCrystal I2C" by Frank de Brabander).

```cpp
#include <LiquidCrystal_I2C.h>

// Create one object per LCD with its address
LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x26, 16, 2);
LiquidCrystal_I2C lcd3(0x25, 16, 2);
LiquidCrystal_I2C lcd4(0x24, 16, 2);
LiquidCrystal_I2C lcd5(0x23, 16, 2);
LiquidCrystal_I2C lcd6(0x22, 16, 2);
LiquidCrystal_I2C lcd7(0x21, 16, 2);
LiquidCrystal_I2C lcd8(0x20, 16, 2);

void setup() {
  lcd1.init(); lcd1.backlight(); lcd1.print("Display 1");
  lcd2.init(); lcd2.backlight(); lcd2.print("Display 2");
  lcd3.init(); lcd3.backlight(); lcd3.print("Display 3");
  lcd4.init(); lcd4.backlight(); lcd4.print("Display 4");
  lcd5.init(); lcd5.backlight(); lcd5.print("Display 5");
  lcd6.init(); lcd6.backlight(); lcd6.print("Display 6");
  lcd7.init(); lcd7.backlight(); lcd7.print("Display 7");
  lcd8.init(); lcd8.backlight(); lcd8.print("Display 8");
}

void loop() {}
```

After uploading, adjust each display's contrast potentiometer (the small trimmer on the back of the backpack) until the text is clearly visible. Eight contrast pots is a bit tedious, but you only do it once.

## The payoff

Eight displays, two pins. The only pins consumed on the Arduino are A4 and A5 — every digital pin and the other analog pins remain free for sensors, buttons, motors, or whatever else the project needs. The same pattern scales to sensors, RTC modules, OLED displays, or any other I²C device: as long as each device has a unique address, they all share the same two-wire bus.

## References and further reading

- [PCF8574 datasheet (TI)](https://www.ti.com/lit/ds/symlink/pcf8574.pdf) — Table 3 shows exactly how A0/A1/A2 map to the 7-bit address
- [LiquidCrystal_I2C library (Arduino Library Manager)](https://www.arduino.cc/reference/en/libraries/liquidcrystal-i2c/) — the library used in this sketch; `init()`, `backlight()`, `print()`, `setCursor()`
- [I²C scanner sketch](/blog/find-i2c-address-arduino) — verify all your LCD addresses before writing application code
- [Arduino Wire library reference](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — the underlying I²C protocol implementation
