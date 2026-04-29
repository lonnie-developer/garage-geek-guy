---
title: "Arduino OLED Display: Connect the 0.96\" 128×64 SSD1306"
description: "The 0.96\" OLED display gives you 128×64 pixels on an I²C bus for about $6. This post covers wiring, library installation, address scanning, and getting the Adafruit example running."
pubDate: 'November 12 2018'
youtubeId: '7yGAbLp9LnM'
heroImage: '../../assets/posts/arduino-oled-display-096-128x64-ssd1306/thumbnail.jpg'
tags: ['arduino', 'oled', 'display', 'i2c', 'adafruit', 'tutorial']
---

For a long time the go-to display for Arduino projects was the 16×2 LCD — sixteen characters wide, two rows, parallel or I²C interface, perfectly functional, and about as visually interesting as a spreadsheet. Then the 0.96" OLED started showing up from Chinese suppliers at $6–8 shipped, and suddenly you had 128×64 pixels, no backlight to power, high contrast, and a display that looks genuinely good on a prototype. The resolution is roughly half that of an Apple II — in a module smaller than a matchbook.

This post covers everything you need to get from unboxing to a working display: wiring, library installation, I²C address scanning, and loading the built-in example sketch.

## The hardware

The display is an OLED panel driven by an SSD1306 controller, communicating over I²C. Four pins: VCC, GND, SCL, SDA. That's it — no separate backlight pin, no contrast adjustment, no eight-wire parallel bus. The I²C interface is one of the things that makes this display so pleasant to use; you only need two signal wires shared with any other I²C devices on the bus.

Typical specifications:
- **Screen size:** 0.96 inches diagonal
- **Resolution:** 128 × 64 pixels
- **Interface:** I²C (some variants also support SPI)
- **Operating voltage:** 3.3 V or 5 V (most modules accept both)
- **Current draw:** ~20 mA active
- **Price:** ~$6–10 from US sellers; $2–4 from AliExpress

There's no backlight — OLED pixels emit their own light. This makes the contrast excellent and power consumption very low when most pixels are dark. It also means the display has no "off state" for pixels that aren't lit; black areas are genuinely dark, not backlit white being blocked by a liquid crystal.

## Wiring to an Arduino Uno

The Uno's I²C pins are A4 (SDA) and A5 (SCL), accessible from the analog headers. Connect with Dupont cables — no breadboard required:

| OLED pin | Arduino Uno pin |
|----------|-----------------|
| VCC      | 5V              |
| GND      | GND             |
| SCL      | A5              |
| SDA      | A4              |

That's the whole wiring job. The I²C bus handles communication; no additional components needed.

## Installing the libraries

Two Adafruit libraries are required. Open the IDE, go to **Sketch → Include Library → Manage Libraries**, and install both:

**Adafruit SSD1306** — the driver library for the display controller.

**Adafruit GFX** — the graphics primitives library (text, shapes, lines, bitmaps). The SSD1306 library depends on it, and it's where most of the interesting drawing functions live.

After installing, close and reopen the IDE. On macOS especially, newly installed libraries don't appear in the menus until you restart the IDE. This is a known quirk — not a failed install.

## Finding the I²C address

Most 0.96" SSD1306 modules use address `0x3C`. A small number use `0x3D`. You need the correct address to initialize the display in code, and the easiest way to confirm it is to run the I²C scanner sketch.

The scanner is a short piece of code that walks all 127 possible I²C addresses and reports which ones respond. You can find it on the [Arduino Playground I²C scanner page](https://playground.arduino.cc/Main/I2cScanner/), or search "arduino i2c scanner" for any of the many copies online.

Upload the scanner, open the Serial Monitor at 9600 baud, and you'll see something like:

```
I2C Scanner
Scanning...
I2C device found at address 0x3C!
Done
```

Write that address down — you'll need it in the next step.

## Running the example sketch

With the libraries installed, go to **File → Examples → Adafruit SSD1306** and open **ssd1306_128x64_i2c**. This is the built-in demo that draws text, shapes, scrolling, and animations — a good sanity check that everything is working.

There's one line to change before uploading. Near the top of the sketch, find:

```cpp
if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) {
```

Change `0x3D` to match what the scanner reported — usually `0x3C`:

```cpp
if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
```

Upload. The display will run through a sequence of graphics: the Adafruit logo, text rendering, drawing primitives (lines, rectangles, circles), and some animation. If nothing appears, double-check the address and confirm your SDA/SCL wires aren't swapped.

## The library at a glance

The Adafruit GFX library is what makes this display more than a text terminal. A few of the functions you'll reach for most:

```cpp
display.clearDisplay();           // blank the buffer
display.setTextSize(1);           // 1 = 6×8 px, 2 = 12×16 px, etc.
display.setTextColor(SSD1306_WHITE);
display.setCursor(0, 0);          // x, y in pixels
display.println("Hello!");
display.display();                // push buffer to screen

display.drawLine(x0, y0, x1, y1, SSD1306_WHITE);
display.drawRect(x, y, w, h, SSD1306_WHITE);
display.fillCircle(x, y, r, SSD1306_WHITE);
display.drawBitmap(x, y, bitmap_array, w, h, SSD1306_WHITE);
```

The key habit to build: every drawing call writes to an in-memory buffer, not directly to the screen. You call `display.display()` when you're ready to push the buffer. Forgetting that call is the most common reason "nothing shows up."

## The gotcha: 128×32 vs. 128×64

These modules come in two heights. The 128×64 version is the taller one with four rows of text at size 1. The 128×32 is visually similar but half as tall. They look nearly identical in product photos, and the wrong example sketch (loading the 128×32 I²C example for a 128×64 display, or vice versa) will produce garbled output or nothing at all.

Confirm your module dimensions before you open the example. The `SCREEN_HEIGHT` constant at the top of the sketch needs to match. If you're seeing only the top half of text or an image compressed vertically, you have a height mismatch.

## What to do with 128×64 pixels

This display is genuinely useful beyond demos. Common applications:
- A clock face with a sweeping second hand (using an RTC module like the DS3231)
- Sensor readout: temperature, humidity, distance, whatever you're measuring
- A simple menu system with button navigation
- Battery status and project diagnostics for a portable build
- Scrolling text for a name badge or status display

For any of these, the [Random Nerd Tutorials OLED guide](https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/) and the [Adafruit learning guide](https://learn.adafruit.com/monochrome-oled-breakouts) are the two best references once you're past initial setup.

## References

- [Random Nerd Tutorials: Guide for I2C OLED Display with Arduino](https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/)
- [Adafruit: Monochrome OLED Breakouts — Wiring 128×64](https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x64-oleds)
- [Adafruit SSD1306 library — GitHub](https://github.com/adafruit/Adafruit_SSD1306)
- [Adafruit GFX library — Arduino Library & Examples](https://learn.adafruit.com/monochrome-oled-breakouts/arduino-library-and-examples)
- [Last Minute Engineers: In-Depth OLED Display Tutorial](https://lastminuteengineers.com/oled-display-arduino-tutorial/)
- [Arduino Playground I²C Scanner](https://playground.arduino.cc/Main/I2cScanner/)
- [SSD1306 datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
