---
title: 'Running 4 HC-SR04 Ultrasonic Sensors on an Arduino Robot — Code and I2C LCD'
description: 'Four cheap ultrasonic sensors, one I2C LCD, and the crosstalk problem nobody warns you about. Full code walkthrough for a multi-sensor distance display on an Arduino robot chassis.'
pubDate: 'October 12 2012'
youtubeId: '0BfdXFP0260'
heroImage: '../../assets/posts/arduino-robot-4-hcsr04-sensors-code/thumbnail.jpg'
tags: ['arduino', 'hc-sr04', 'ultrasonic', 'robotics', 'i2c', 'lcd', 'tutorial']
---

There's a certain point in every robot build where one sensor stops being enough. One HC-SR04 tells you there's something in front of you. Four of them tell you *which* side of the front, whether anything is closing in from the sides, and which way to turn. The jump from one sensor to four isn't just "more of the same" — it changes what your robot can actually reason about.

This post covers the code side of mounting four HC-SR04 sensors on an Arduino robot chassis: how to read all four without the signals stepping on each other, how to display four simultaneous distance readings on a 16×2 I2C LCD, and a couple of gotchas that cost a few hours of head-scratching when building this setup on an actual robot in 2012.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The sensor layout

The robot has four HC-SR04 sensors in a classic compass-rose arrangement: two at the front (front-left and front-right), one pointing left, one pointing right. The two front sensors are what give you the ability to decide whether to turn left or turn right when something is ahead — if the left front sensor reads closer than the right front, the obstacle is on your left side and you want to turn right, and vice versa.

The naming in the code reflects this:

- `sonicA` — front right
- `sonicB` — front left
- `sonicL` — left side
- `sonicR` — right side

Having dedicated side sensors means the robot can also detect walls it's running alongside and react before it actually hits them — a significant upgrade over single-sensor "am I about to hit something" logic.

## What you'll need

- 4× HC-SR04 ultrasonic distance modules (~$1 each on eBay)
- Arduino Uno or compatible
- 16×2 I2C LCD display (the kind with a PCF8574 backpack, I²C address 0x27 is typical)
- [LiquidCrystal\_I2C library](https://github.com/johnrickman/LiquidCrystal_I2C) — version 1 works; grab it through the Library Manager
- [Ultrasonic library by Erick Simões](https://github.com/ErickSimoes/Ultrasonic) — the one-command `.ranging()` approach used here
- Jumper wire, a robot chassis with four sensor mounting points

Fair warning on sensor quality: out of a batch of six HC-SR04s purchased for this build, two were dead on arrival. That's not unusual for the cheapest end of eBay. Buy a few extras.

## The code

Here's the full sketch, walked through in sections:

### Includes and defines

```cpp
#include <Ultrasonic.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

Ultrasonic sonicA(2, 3);   // front right  — Trig pin, Echo pin
Ultrasonic sonicB(4, 5);   // front left
Ultrasonic sonicL(6, 7);   // left side
Ultrasonic sonicR(8, 9);   // right side

LiquidCrystal_I2C lcd(0x27, 16, 2);
```

The Ultrasonic library wraps each sensor in an object you initialize with its Trig and Echo pins. The I2C LCD gets its address (0x27 is the most common value for PCF8574-based backpacks, though 0x3F is also common — use an I2C scanner sketch to confirm yours) along with the column and row counts.

If you're not sure of your LCD's I2C address, there's already a post on this blog covering exactly that: [How to find out the address of your I2C device](/blog/arduino-i2c-lcd-1602).

### Setup

```cpp
void setup() {
  lcd.init();
  lcd.backlight();

  // Splash screen
  lcd.setCursor(0, 0);
  lcd.print("BotName");
  lcd.setCursor(0, 1);
  lcd.print("meanpc.com");
  delay(2000);

  lcd.clear();

  // Static labels — print once, they don't change
  lcd.setCursor(1, 0);  lcd.print("FR");
  lcd.setCursor(5, 0);  lcd.print("FL");
  lcd.setCursor(9, 0);  lcd.print("LT");
  lcd.setCursor(13, 0); lcd.print("RT");
}
```

The labels across the top row (FR, FL, LT, RT) are printed once in `setup()` and left there. Only the distance values on the second row get updated in the loop, which avoids the flicker you'd get from clearing and redrawing the whole display every iteration.

### The loop

```cpp
void loop() {
  int distA = sonicA.ranging(INC);
  delay(5);
  int distB = sonicB.ranging(INC);
  delay(5);
  int distL = sonicL.ranging(INC);
  delay(5);
  int distR = sonicR.ranging(INC);
  delay(5);

  // Print each reading under its label
  printDistance(1,  distA);
  printDistance(5,  distB);
  printDistance(9,  distL);
  printDistance(13, distR);
}
```

`INC` is the Ultrasonic library's constant for inches. Swap it for `CM` if you think in centimeters.

The `delay(5)` between each sensor read is the crosstalk fix, and it matters. Ultrasonic sensors work by sending a pulse and waiting for the echo. If sensor A fires and sensor B fires 50 microseconds later, B might pick up A's echo — and you'll read the wrong distance, or no distance at all. A 5-millisecond gap between readings is enough to let each echo die out before the next trigger fires.

### The display function

```cpp
void printDistance(int col, int dist) {
  lcd.setCursor(col, 1);
  if (dist > 16) {
    lcd.print("##");
  } else {
    lcd.print(dist);
    lcd.print("  ");   // two trailing spaces
  }
}
```

Two things worth explaining here.

**The 16-inch cap.** These cheap sensors are rated to 400 cm (about 157 inches), but at hobby robot scales, a reading past 16 inches is basically "nothing nearby." Rather than display a big number that takes up more columns than allocated, readings over 16 print as `##` — a clear "out of range" indicator that also keeps the layout clean.

**The two trailing spaces.** This is the one that trips people up. If the previous reading was `14` and the current reading is `6`, printing `6` over it leaves the `4` still showing — you'd see `64` instead of `6`. Printing two spaces after the value clears whatever was there. The display column width for each sensor is fixed at four characters, so two digits plus two spaces always fills the slot cleanly.

## What it looks like

On the LCD: top row is static labels, bottom row updates continuously. With the robot on a table surrounded by random objects, you'll see something like:

```
FR  FL  LT  RT
 8  12   5   9
```

Move your hand toward the left side and the LT column ticks down in real time. It tracks independently, which is exactly what you want when you're about to wire up the motor logic.

## The gotcha: DOA sensors

Two out of six HC-SR04s in this build arrived dead — one showed no echo at all, one returned garbage distances. This was a debugging nightmare because it was impossible to tell at first whether the wiring was wrong, the code was wrong, or the sensor was bad.

The fastest way to rule out a bad sensor is to swap it with one you've already verified works. If the problem follows the sensor to its new position, it's hardware. If it stays at the same pins, it's code or wiring.

For the same reason, if you're buying HC-SR04s for a multi-sensor build, order at least 20% more than you need. At a dollar apiece, the insurance is cheap.

## Where this fits in the build

This is a sensor-test sketch — its only job is to display distance readings on the LCD. That's intentional. Getting the sensors verified and displaying correctly is a milestone worth isolating before you mix in motor control logic. Once you can see all four sensors tracking independently in real time, you have a solid foundation to build the avoidance logic on top of: "if sonicA and sonicB are both under 8 inches, something is directly ahead; compare them to decide which way to turn; check sonicL and sonicR before committing to that turn."

The next step from here is combining this sensor loop with the motor driver code from [the L298N motor driver post](/blog/l298n-motor-driver-arduino-pwm) to get a first complete avoidance program running.

## References and further reading

- [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — the official spec sheet; actual useful range and timing requirements are in here
- [Ultrasonic library by Erick Simões](https://github.com/ErickSimoes/Ultrasonic) — the library used in this sketch
- [LiquidCrystal\_I2C library (johnrickman fork)](https://github.com/johnrickman/LiquidCrystal_I2C) — the I2C LCD library used here
- [NewPing library](https://bitbucket.org/teckel12/arduino-new-ping/wiki/Home) — a more actively maintained alternative with non-blocking ping support; worth looking at for more complex builds
- [Arduino: I2C LCD address scanner](https://playground.arduino.cc/Main/I2cScanner/) — find your LCD's address before your code goes nowhere
- [PCF8574 I²C port expander datasheet](https://www.ti.com/lit/ds/symlink/pcf8574.pdf) — what's on the back of most cheap 1602 I2C LCDs
- [Sensor crosstalk in ultrasonic arrays](https://www.maxbotix.com/articles/033.htm) — MaxBotix's write-up on why multiple ultrasonic sensors interfere and how to mitigate it
