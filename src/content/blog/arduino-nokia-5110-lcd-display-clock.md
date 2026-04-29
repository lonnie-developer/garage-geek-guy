---
title: 'How to Use a Nokia 5110 LCD with Arduino — $3 Display + Clock Demo'
description: "The Nokia 5110's 84×48 monochrome LCD is surplus from one of the best-selling phones in history, which is why you can get five of them for $15 shipped. Full wiring guide, Adafruit PCD8544 library setup, and a sweeping clock-face demo."
pubDate: 'May 14 2013'
youtubeId: 'M9XBFomX7JI'
heroImage: '../../assets/posts/arduino-nokia-5110-lcd-display-clock/thumbnail.jpg'
tags: ['arduino', 'lcd', 'nokia-5110', 'pcd8544', 'display', 'tutorial']
---

There's a particular class of electronics surplus that results from one product being wildly, unexpectedly successful. Nokia made hundreds of millions of candy-bar phones in the late 1990s — the 3310, the 5110, the 6110, all running on the same 84×48 Phillips PCD8544 LCD. When smartphones made them obsolete, the displays didn't disappear. They ended up in parts bins, eBay lots, and cheap breakout boards, and they've been a hobbyist favorite ever since.

The reason is simple: there are so many of them that they're nearly free, they're well-documented, and Adafruit wrote a good library for them. You get a readable monochrome display with a backlight, graphics support, and a Phillips datasheet that's actually written like a tutorial instead of a spec sheet — for about $3 each if you buy them in a batch from a Chinese supplier.

This post covers everything you need to get one running on an Arduino Uno: the full pinout, the 3.3V voltage caveat, wiring (with and without level shifting), the Adafruit PCD8544 and GFX libraries, and a clock-face demo with a sweeping second hand.

> *This build is from 2013, when the channel was still MeanPC.com — same workbench, same approach, different name on the channel art.*

## The display itself

The Nokia 5110 LCD is 84 pixels wide and 48 pixels tall — not a lot of screen real estate, but enough for two or three lines of text, basic graphics, or small bitmaps. It's monochrome: each pixel is either on or off, no grayscale. The backlight is four white LEDs, one in each corner of the display, driven through a single transistor that you can PWM for brightness control.

The chip on the back is the Phillips PCD8544, and the datasheet for it is worth reading even if you never plan to write your own driver. It's unusually detailed for a chip datasheet — includes a full functional description of each subsystem, timing diagrams, RAM addressing, and enough information to write a working driver from scratch. Adafruit did exactly that, so you don't have to.

**Sourcing:** On eBay from Chinese sellers, five of these come to around $15 shipped — roughly $3 each. SparkFun and Adafruit both carry them for about $10 each. The $10 version comes with Adafruit's support, proper headers, and optionally level-shifting hardware. The $3 version comes with nothing but the display module. Either works for this project.

## The voltage caveat

This is the thing most beginner tutorials skip over.

The Nokia 5110 LCD is officially a **3.3V device**. The Phillips datasheet lists the absolute maximum input voltage for logic signals at 7V — which means an Arduino Uno's 5V logic won't instantly fry it, but it *can* shorten the display's lifespan. For a bench demo or a one-time project, it's probably fine. For anything that's going to run for months, use current-limiting resistors (10 kΩ per signal line is the common choice) or a proper level shifter on the logic lines.

SparkFun's quickstart guide for the 5110 shows both approaches:

1. **Resistor method**: 10 kΩ resistor on each logic input line (LED, CLK, MOSI, DC, RESET, SCE). Simple, cheap, slightly lossy.
2. **Level shifter**: A dedicated 5V↔3.3V converter like the TXB0104. Cleaner for production builds.

If you buy from Adafruit, the kit includes level-shifting hardware. The video demo runs the display directly at 5V for clarity — but the recommendation is to add the resistors if you're leaving it running long-term.

## Pinout

The Nokia 5110 module has 8 pins:

| Module pin | Function | Arduino Uno |
|---|---|---|
| RST | Reset | Pin 5 |
| CE / SCE | Chip enable (active low) | Pin 6 |
| DC | Data/command select | Pin 4 |
| DIN / MOSI | Serial data in | Pin 3 |
| CLK | Serial clock | Pin 7 |
| VCC | Power | 3.3V |
| BL / LED | Backlight | Pin 11 (PWM) |
| GND | Ground | GND |

Two notes on that pinout: first, VCC should be 3.3V from the Arduino's 3.3V header, not 5V. Second, the DIN and CLK lines are swapped relative to Arduino pins 3 and 4 — pin 3 on the Uno goes to DIN, pin 4 goes to DC, but in the Adafruit library initialization you'll see the constructor lists them in a specific order. Match the library's expected order, not what feels intuitive from the pin numbering.

Pin 11 for the backlight is a PWM-capable pin, which lets you set brightness with `analogWrite(11, value)` rather than just full-on or full-off. Setting it to 20 (out of 255) runs the backlight at roughly 8% duty cycle — dim enough to see clearly indoors without the display washing out.

## Library installation

Two libraries are required:

**Adafruit PCD8544** — the hardware driver for the Phillips chip. Download it from [github.com/adafruit/Adafruit-PCD8544-Nokia-5110-LCD-library](https://github.com/adafruit/Adafruit-PCD8544-Nokia-5110-LCD-library) as a ZIP and install via `Sketch → Include Library → Add .ZIP Library`. You'll need to rename the extracted folder to something clean (no special characters) before the IDE will accept it.

**Adafruit GFX** — the generic graphics layer that provides `drawLine()`, `drawCircle()`, `fillRect()`, and text rendering, shared across all Adafruit displays. Same installation process, from [github.com/adafruit/Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library).

Once both are installed, `File → Examples → Adafruit PCD8544 → PCD8544test` gives you a working demo to verify everything is wired correctly before writing your own code.

## The display buffer

Before writing code, the most important concept to understand is the display buffer.

When you call `display.print("hello")` or `display.drawLine(...)`, nothing appears on the screen immediately. The library writes to an internal 504-byte buffer in your Arduino's RAM (84 × 48 pixels ÷ 8 bits per byte). The actual pixels only update when you call `display.display()`, which dumps the buffer to the LCD's own RAM over SPI.

This means you can build up a complete frame — clock numbers, graphics, whatever — and push it all to the screen in one call. It also means you can add new elements to an existing display without clearing the whole screen first, by writing to the buffer and calling `display.display()` without clearing first.

The downside is that the buffer takes up RAM. On an Uno with 2 KB, 504 bytes is a meaningful chunk. On a Mega it's nothing. Something to keep in mind if your sketch starts running out of memory.

## The clock demo

The video's demo code draws a minimal analog clock face: the numbers 12, 6, 3, and 9 at their approximate positions, and a line sweeping from the center of the screen outward — like a second hand.

The 84×48 display puts the center at approximately (42, 24). The second hand is a line from that center point out to a moving endpoint. To get the sweeping motion without trigonometry, the code uses four `for` loops — one for each quadrant of the clock face — each incrementing the endpoint along one edge of the screen:

```cpp
// Top-left to top-right (12 o'clock sweep)
for (int m = 0; m <= 84; m += 3) {
  display.clearDisplay();
  display.drawLine(42, 24, m, 0, BLACK);
  drawClock();
  display.display();
  delay(250);
}
// Top-right to bottom-right
for (int m = 0; m <= 48; m += 3) {
  display.clearDisplay();
  display.drawLine(42, 24, 84, m, BLACK);
  drawClock();
  display.display();
  delay(250);
}
// ... and so on for the other two quadrants
```

The `drawClock()` helper function places the 12, 6, 3, and 9 digits at fixed cursor positions using `display.setCursor()` and `display.print()`. It also draws a filled circle at the center using `display.fillCircle(42, 24, 2, BLACK)`.

One refinement the video mentions but doesn't implement: instead of clearing the whole display and redrawing everything on each frame, you can erase only the previous second-hand line by redrawing it in WHITE (which turns pixels off on this monochrome display). That way the clock numbers don't need to be redrawn every frame, which makes the animation smoother and more efficient.

## The result

The display is surprisingly readable for something this old and this cheap. The backlight at 8% duty cycle is comfortable in a dim room; at full brightness it's viewable in direct sunlight. The animation on the clock hand is smooth enough to demonstrate the display's response time without any obvious flickering.

The flexibility of the Adafruit GFX layer is the other payoff — once you understand how the buffer works, every display Adafruit supports uses the same drawing commands. The same code that draws a filled circle here will draw one on an SSD1306 OLED or an HX8357 TFT with minimal changes.

## Where this display still makes sense

The Nokia 5110 is good for: small projects where a character LCD would feel clunky, builds where you want bitmap graphics or custom fonts, and any situation where cost is the primary constraint. At $3 it's hard to argue with.

It's not the right choice for color displays, large text, or anything that needs fast updates — the SPI interface is relatively slow and the 504-byte buffer overhead means you're doing a full frame transfer on every `display.display()` call. For those use cases, look at SSD1306 OLEDs (similar size, faster, same $3–5 price range) or a small TFT.

But as an introduction to Arduino graphics and the Adafruit display ecosystem, the Nokia 5110 is still one of the better $3 you can spend on parts.

## References and further reading

- [Phillips PCD8544 datasheet (1999)](https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf) — the original chip spec; unusually readable for a semiconductor datasheet
- [Adafruit PCD8544 library on GitHub](https://github.com/adafruit/Adafruit-PCD8544-Nokia-5110-LCD-library)
- [Adafruit GFX graphics library on GitHub](https://github.com/adafruit/Adafruit-GFX-Library)
- [SparkFun Nokia 5110 hookup guide](https://learn.sparkfun.com/tutorials/graphic-lcd-hookup-guide) — includes level-shifting wiring diagrams
- [Adafruit Nokia 5110 guide](https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd) — step-by-step with the Adafruit version of the breakout board
- [Nokia 5110 eBay search](https://www.ebay.com/sch/i.html?_nkw=nokia+5110+lcd+arduino) — current pricing and availability; five for under $15 is still the norm
