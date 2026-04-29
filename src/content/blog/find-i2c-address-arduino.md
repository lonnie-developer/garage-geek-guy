---
title: 'How to Find the I2C Address of Any Device Using an Arduino'
description: 'Before you can talk to an I2C device, you need its address. An I2C scanner sketch brute-forces all 127 possible addresses and reports what it finds in the serial monitor — two minutes of setup and you have the number you need.'
pubDate: 'October 31 2018'
youtubeId: 'dVqv3LvJAJY'
heroImage: '../../assets/posts/find-i2c-address-arduino/thumbnail.jpg'
tags: ['arduino', 'i2c', 'lcd', 'oled', 'tutorial', 'beginner']
---

Every I²C device has a 7-bit address — a number between 1 and 127 that the master (your Arduino) uses to select which device it's talking to on the shared bus. Without the correct address, your code calls go nowhere. The device sits there, the Arduino sends nothing useful, and your sketch doesn't work.

Finding the address sounds like it should be simple. Sometimes it is — a device's datasheet states the address clearly, or the module's product page lists it. But cheap eBay modules often arrive without documentation, different manufacturers use different default addresses for the same chip, and some modules have solder jumpers that change the address and may have been bridged at the factory. The fastest solution is to stop hunting through specs and just ask the bus what's there.

That's what the I²C scanner sketch does.

## How the scanner works

The scanner loops through all possible 7-bit I²C addresses (1 through 126) and attempts to initiate a transmission to each one. If a device acknowledges — sends back an ACK — the scanner reports that address. If nothing responds, it moves on.

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("I2C scanner — scanning...");

  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("Device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  Serial.println("Done.");
}

void loop() {}
```

Upload this, open the serial monitor at 9600 baud, and press the reset button. The output will look something like:

```
I2C scanner — scanning...
Device found at address 0x27
Done.
```

Or with two devices:

```
Device found at address 0x27
Device found at address 0x3C
```

Write those addresses down. They're what goes into the `LiquidCrystal_I2C(address, cols, rows)` or `display.begin(SSD1306_SWITCHCAPVCC, address)` call in your actual project sketch.

## Wiring

On the Arduino Uno, the I²C pins are **A4 (SDA)** and **A5 (SCL)**. Connect your device's SDA to A4 and SCL to A5, then power it from the Uno's 5V and GND rails.

```
Arduino Uno    →    I2C Device
A4 (SDA)       →    SDA
A5 (SCL)       →    SCL
5V             →    VCC
GND            →    GND
```

Most I²C modules sold as breakout boards or LCD backpacks have their pull-up resistors onboard, so no external resistors are needed for a single device. If you're connecting multiple devices, see the [multiple I²C devices post](/blog/multiple-i2c-devices-arduino) for the pull-up discussion.

## What the common addresses look like

In practice, a handful of addresses cover the vast majority of modules you'll encounter:

- **0x27** — 1602 LCD with PCF8574 I²C backpack (most common default)
- **0x3F** — same PCF8574 backpack, alternate address (solder jumpers set differently)
- **0x3C** — SSD1306 OLED display (128×64 or 128×32)
- **0x3D** — SSD1306 OLED, alternate address
- **0x68** — DS3231 or DS1307 real-time clock module
- **0x48** — ADS1115 ADC, MPU-6050 gyro/accelerometer (also many temperature sensors)
- **0x76 / 0x77** — BME280 / BMP280 pressure and temperature sensors

If your scanner finds one of these, you can cross-reference to confirm which device it is before writing the sketch.

## Two devices, two addresses

The video demonstrates finding addresses for two different devices: a 1602 I²C LCD (0x27) and a 128×96 OLED display (0x3C). Each is wired up separately and scanned individually, then the addresses are noted for use in the next project.

When you're planning a build with multiple I²C devices, scanning them individually first is also a good way to verify they're working at all before integrating them. A device that doesn't show up in the scanner is either wired incorrectly, not powered, or dead — all of which are better to know before you've spent an hour integrating it into a larger sketch.

## When the scanner finds nothing

If the scanner completes and reports nothing:

1. **Check SDA/SCL connections** — A4 and A5, not some other pins. On the Uno these are labeled on the board; on other Arduino variants the I²C pins may be different.
2. **Check power** — is the device getting 5V and GND?
3. **Try resetting after everything is connected** — the scanner runs in `setup()`, so it only scans on power-up or reset. If you wired the device after uploading, hit the reset button.
4. **Check the device voltage** — some modules are 3.3V only. Feeding them 5V will damage the module and produce silence on the scanner. Check the module's spec before powering.
5. **Add pull-up resistors** — on some combinations of device and wiring length, the internal pull-ups aren't strong enough. Try 4.7K resistors from SDA to 5V and SCL to 5V.

## References and further reading

- [Arduino Wire library reference](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — `beginTransmission()`, `endTransmission()`, and the error codes the scanner uses
- [Arduino I²C scanner sketch (Playground)](https://playground.arduino.cc/Main/I2cScanner/) — the original canonical version; includes error-code handling for stuck buses
- [I²C address reference (Adafruit)](https://learn.adafruit.com/i2c-addresses/the-list) — Adafruit's running list of common I²C addresses by device type
- [PCF8574 datasheet (TI)](https://www.ti.com/lit/ds/symlink/pcf8574.pdf) — the I²C expander on most cheap LCD backpacks; Table 3 shows how A0/A1/A2 jumpers affect the address
- [SSD1306 datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf) — Section 8.1.5 covers I²C address selection (D/C# pin sets 0x3C vs 0x3D)
