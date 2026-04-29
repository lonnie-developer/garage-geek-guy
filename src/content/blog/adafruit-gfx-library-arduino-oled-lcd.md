---
title: 'Adafruit GFX Library for Arduino — Draw Graphics on OLED + LCD Displays'
description: 'How the Adafruit GFX library works — coordinate system, screen buffer, and every drawing primitive from drawPixel to drawTriangle, demonstrated on a 128x64 SSD1306 OLED.'
pubDate: 'November 15 2018'
youtubeId: 'J209od-7Cxc'
heroImage: '../../assets/posts/adafruit-gfx-library-arduino-oled-lcd/thumbnail.jpg'
tags: ['arduino', 'oled', 'adafruit', 'display', 'ssd1306', 'tutorial']
---

There's a specific moment in the OLED learning curve that trips up a lot of people. You've wired the display, installed the Adafruit SSD1306 library, run the example sketch, and the screen lit up with a cascade of demo graphics. Great. Now you close the example, open a blank sketch, and try to draw something yourself — and nothing works. The `display.display()` call you vaguely remember from the example doesn't seem to do anything. The coordinate system is confusing. You can't figure out why your rectangle disappeared when you tried to add a circle.

The gap isn't the SSD1306 driver. That part's fine. The part you're actually missing is the [Adafruit GFX graphics library](https://learn.adafruit.com/adafruit-gfx-graphics-library/overview) — the layer that lives above the display-specific driver and provides all the actual drawing commands.

This post walks through every GFX primitive you'll use day-to-day, demonstrated on a 0.96" 128x64 SSD1306 OLED. The same library — and the same commands — carry over to the Nokia 5110 LCD, Adafruit's ePaper panels, the ST7565 graphical LCD, and most of the color TFT modules Adafruit makes. The display driver changes; the GFX API stays the same.

## The two-library architecture

Every Adafruit display sketch has two `#include` lines at the top for a reason. `Adafruit_GFX.h` is the abstract graphics layer — it knows how to draw lines, circles, text, and so on, but it doesn't know anything about your particular hardware. `Adafruit_SSD1306.h` (or whatever the driver is for your specific display) handles all the hardware communication — I²C addresses, initialization sequences, pushing bytes to the display controller. You need both.

When you call `display.drawCircle(64, 32, 10, WHITE)`, GFX figures out which pixels belong to that circle and hands them to the SSD1306 driver, which puts them into the screen buffer, which eventually gets pushed to the actual panel. That handoff is invisible to you as the programmer, but it's why the GFX command set is identical whether you're drawing on a 0.96" OLED or a Nokia 5110 — only the driver underneath changes.

## The coordinate system

Before any drawing command makes sense, you need the coordinate model firmly in your head. The origin — (0, 0) — is the **upper-left corner** of the display. X increases to the right; Y increases downward. For a 128×64 panel, the bottom-right corner is **(127, 63)**, not (128, 64), because we're counting from zero.

Every GFX primitive takes X before Y, always. If you get shapes appearing in the wrong corner, the most likely explanation is that you swapped your coordinates.

## The screen buffer — why nothing shows until you call display.display()

This is the single most important thing to understand about GFX, and the one the example sketch hides from you.

When you call `display.drawLine(...)` or any other drawing command, you are **not** writing to the screen. You're writing to a memory buffer that lives in the Arduino's RAM — think of it as a scratch pad where your drawing accumulates invisibly. The actual panel doesn't update until you call `display.display()`.

That call is what pushes the entire buffer to the display over I²C. Until you call it, nothing visible happens, no matter how many draw commands you've stacked up.

In practice this means every sketch has the same rhythm: clear the buffer with `display.clearDisplay()`, issue all your draw commands, then call `display.display()` once at the end. If you call `display.display()` after each individual draw command, it works but it's slow — you're sending a full 128×64 frame over I²C for every pixel. Call it once per frame.

## The primitives

### drawPixel — one dot at a time

The most atomic operation:

```cpp
display.drawPixel(64, 32, WHITE);
display.display();
```

X, Y, color. On a monochrome display the "color" argument is just 0 (black, off) or 1 (white, on). At 64,32 on a 128×64 panel that lands roughly in the center of the screen — it's a tiny dot, but it's there.

You'll use `drawPixel` more than you'd expect once you start writing custom drawing routines. Every arc, every custom font character, every animation frame eventually comes down to individual pixels.

### drawLine — connect two points

```cpp
display.drawLine(0, 0, 32, 63, WHITE);
```

Start X, Start Y, End X, End Y, color. GFX handles the Bresenham line-drawing algorithm internally — you just give it two endpoints.

### drawRect and fillRect — rectangles

```cpp
display.drawRect(70, 2, 30, 15, WHITE);   // outline only
display.fillRect(70, 40, 35, 15, WHITE);  // solid fill
```

Arguments are: X (left edge), Y (top edge), width, height, color. `drawRect` gives you a hollow outline; `fillRect` fills it solid. Note that the X and Y arguments are the upper-left corner of the rectangle, not the center.

### drawCircle and fillCircle

```cpp
display.drawCircle(22, 30, 15, WHITE);    // outline
display.fillCircle(22, 30, 15, WHITE);    // solid
```

X and Y here are the **center** of the circle, not the upper-left of its bounding box — that's different from how rectangles work, and it bites people the first time. Third argument is radius. GFX also has `drawRoundRect` and `fillRoundRect` if you want rectangles with softened corners; the extra argument is the corner radius in pixels.

### drawTriangle — three corners

```cpp
display.drawTriangle(5, 5, 127, 3, 64, 60, WHITE);
```

You provide all three corner points: X0,Y0, X1,Y1, X2,Y2. There's a `fillTriangle` version as well. GFX doesn't care which corner is "top" or "left" — just give it three points in any order and it works out the edges.

## Drawing text

Text requires a few extra setup calls before the actual print command.

```cpp
display.setCursor(64, 32);
display.setTextColor(WHITE);
display.setTextSize(1);
display.print("hello");
display.display();
```

`setCursor` sets where the upper-left corner of the first character will land. `setTextColor` is straightforward — WHITE or BLACK. `setTextSize` is a multiplier of the default character size: 1 is the native 6×8 pixel font, 2 is 12×16, 3 is 18×24, and so on. The font is chunky at small sizes, but it's built into the library with no external dependencies. GFX also supports custom bitmap fonts (the `setFont()` call), which is how you get proportional typefaces if that's where your project goes.

The `display.print()` call works exactly like `Serial.print()` — it takes strings, integers, floats, whatever you'd normally print to serial. The output lands on the display at the cursor position.

One small gotcha Lonnie caught in the video: the call is `display.setTextColor()`, not `display.setColor()`. Easy to mistype, and the error message in the Arduino IDE isn't particularly helpful when you do.

## The gotcha: nothing shows without display.display()

Worth repeating because it's the thing people hit twice. If you run a sketch and the screen is blank, the first thing to check isn't your wiring — it's whether you called `display.display()` after your draw commands. This is responsible for a significant fraction of "my OLED doesn't work" posts in every Arduino forum.

The second thing to check: did you call `display.clearDisplay()` before drawing? If you skip the clear, the buffer still has whatever was there from the last frame, and your new drawing gets layered on top. On a monochrome display that usually just looks like garbage.

## Where the GFX library reaches

The library list that GFX supports is long and keeps growing. Beyond the SSD1306, you'll find GFX under the hood of the [Nokia 5110 / PCD8544 driver](https://github.com/adafruit/Adafruit-PCD8544-Nokia-5110-LCD-library), Adafruit's various ePaper and e-ink displays, the SH1106 (which is a common alternative OLED controller that looks just like the SSD1306), and many of their TFT displays via the ILI9341, ST7789, and HX8357 drivers. The color displays add a full 16-bit color argument instead of the 0/1 you're using here, but the drawing calls — drawLine, drawRect, drawCircle, print — are identical.

This means if you write a clean GFX-based display routine for your SSD1306 prototype, swapping to a bigger TFT for the final build is a driver swap and a color constant update, not a rewrite.

## References and further reading

- [Adafruit GFX Graphics Library — official documentation](https://learn.adafruit.com/adafruit-gfx-graphics-library/overview)
- [Graphics Primitives reference page](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives) — the page to have open at the bench
- [Adafruit SSD1306 library on GitHub](https://github.com/adafruit/Adafruit_SSD1306)
- [SSD1306 datasheet (Solomon Systech)](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf) — if you want to understand what the driver is actually doing
- [Adafruit Monochrome OLED Breakouts guide](https://learn.adafruit.com/monochrome-oled-breakouts/arduino-library-and-examples) — wiring and library setup if you haven't gotten there yet
- [Random Nerd Tutorials: Guide for I2C OLED with Arduino](https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/) — solid secondary reference with wiring diagrams
