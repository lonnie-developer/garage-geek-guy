---
title: 'How to Use a Keypad with Arduino — Matrix Wiring and the Keypad Library'
description: 'A 4x4 membrane keypad gives you 16 buttons through only 8 Arduino pins. This post covers the matrix logic, the Keypad library, wiring, and how to display keypresses on an I2C LCD.'
pubDate: 'August 21 2021'
youtubeId: 'uRUqYm9Y6sA'
heroImage: '../../assets/posts/arduino-keypad-tutorial/thumbnail.jpg'
tags: ['arduino', 'keypad', 'lcd', 'i2c', 'input', 'tutorial']
---

Most Arduino projects are pretty good at producing output — blinking LEDs, spinning servos, updating displays. The input side is where things get thin fast. You've got a handful of analog pins for potentiometers and sensors, and a few digital pins you can tie to individual buttons. But the moment you need more than three or four distinct inputs, you've burned most of your pins and the wiring gets ugly.

A matrix keypad solves this by multiplexing. A 4x4 membrane keypad — the rubbery kind with 16 labeled buttons — gives you all 16 buttons through just 8 Arduino pins. That's possible because the buttons are arranged in a grid of rows and columns, and you only need one wire per row and one wire per column to uniquely identify every key. It's the same trick calculator keyboards have used for decades.

This post covers how the matrix logic works, how to wire it, how to get the Keypad library installed, and how to display keypresses on an I2C LCD — which is what the video does. If you just want to read keystrokes without a display, the LCD parts are optional.

## How the 4x4 matrix works

The keypad has 16 buttons arranged in 4 rows and 4 columns. Behind the flex membrane, each button is just a normally-open switch connecting one row trace to one column trace. Eight wires come off the connector — the first four connect to the four row traces, the last four to the four column traces.

When you press the "3" key, it makes contact between Row 1 and Column 3. The Arduino detects this by scanning: it sets Row 1 high and reads all four column pins. Only Column 3 goes high. Since it knows which row it just set high and which column responded, it knows the key was "3." It cycles through all four rows in sequence, reading the columns after each one. At the ~1000 Hz scan rate the library runs, this all happens so fast that no keypress gets missed and no combination registers as something else.

The result: 16 unique key combinations identified using exactly 8 digital pins, with the library handling all the scanning logic so you never have to write any of it.

## What you'll need

- Arduino Uno (or Mega/Nano — pin counts are flexible)
- 4x4 membrane keypad (~$2–4 shipped)
- I2C LCD display (16x2 or 20x4) with PCF8574 backpack (~$3–5)
- Jumper wires

The I2C LCD uses only 2 Arduino pins (SDA and SCL) regardless of display size, which is why it pairs so well with a keypad — you've already used 8 pins on the keypad, so the 2-pin I2C interface matters.

## Installing the Keypad library

Open the Arduino IDE, go to **Sketch → Include Library → Manage Libraries**, and search for `keypad`. You want the one by Mark Stanley and Alexander Brevig — it says "Library for using matrix style keypads with the Arduino." Click Install.

While you're there, also install **LiquidCrystal I2C** by Frank de Brabander if you're adding the LCD. Search for `liquidcrystal i2c` and install it.

## Wiring the keypad

The connector on a standard 4x4 keypad comes out as 8 pins in a row — Row 1 through Row 4, then Column 1 through Column 4. In the video I'm using Arduino pins 3, 2, 1, 0 for the rows and 7, 6, 5, 4 for the columns. You can use different pins, but update the arrays in the code to match.

```
Keypad pin 1 (Row 1) → Arduino pin 3
Keypad pin 2 (Row 2) → Arduino pin 2
Keypad pin 3 (Row 3) → Arduino pin 1
Keypad pin 4 (Row 4) → Arduino pin 0
Keypad pin 5 (Col 1) → Arduino pin 7
Keypad pin 6 (Col 2) → Arduino pin 6
Keypad pin 7 (Col 3) → Arduino pin 5
Keypad pin 8 (Col 4) → Arduino pin 4
```

No resistors, no extra components. The Keypad library enables internal pull-up resistors on the column pins, so you're set with just wires.

The I2C LCD connects to 5V, GND, and then the SDA/SCL pins — on the Uno that's A4 (SDA) and A5 (SCL).

## The code

```cpp
#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

// LCD at I2C address 0x23 (check yours with the I2C scanner sketch)
LiquidCrystal_I2C lcd(0x23, 16, 2);

// Keymap — edit this to match your physical keypad layout
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// Pin assignments — rows first, then columns
byte rowPins[ROWS] = {3, 2, 1, 0};
byte colPins[COLS]  = {7, 6, 5, 4};

Keypad customKeypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.print("Initiated");
  delay(3000);
  lcd.clear();
}

void loop() {
  char customKey = customKeypad.getKey();

  if (customKey) {
    lcd.clear();
    lcd.print(customKey);
  }
}
```

`customKeypad.getKey()` returns a character if a key is currently pressed, or `NO_KEY` (which is falsy) if nothing is pressed. The `if (customKey)` check skips the LCD update when no key is held down, so you're not constantly clearing the display.

## The part that trips people up: keymap layout

The `keys[][]` array maps positions in the grid to the characters your sketch will see. The default example from the library uses a generic layout, but your physical keypad may not match it exactly. In the video, the keypad's star key was showing up as something else — the fix was to edit the array until it matched the physical printing on the membrane.

The easiest way to figure out your actual layout: temporarily replace the `lcd.print(customKey)` with `Serial.print(customKey)` and open the serial monitor. Press each key and note what character appears. If the "A" button returns "B", swap them in the array. Five minutes of mapping usually fixes any mismatch.

It's also remappable in software. If you want the star key to input "Z" instead:

```cpp
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'Z', '0', '#', 'D'}   // '*' replaced with 'Z'
};
```

Upload, and now pressing the star key sends 'Z' to your sketch. No hardware changes, no extra circuitry.

## Finding your LCD's I2C address

The address `0x23` in the code above is specific to an LCD backpack with A2 bridged and A0/A1 open. If your LCD backpack has different jumpers set (or no jumpers at all), its address will be different — typically `0x27` or `0x3F`.

The easiest way to find the right address: open the Arduino IDE, go to File → Examples → Wire → i2c_scanner, upload it, and open the serial monitor. It'll list every I2C device it finds and their addresses. Use whatever address it reports.

## Scaling up

A 4x4 keypad uses 8 of your digital pins. If you're on an Uno that leaves you 6 digital pins plus 6 analog pins — tight, but workable for simple projects. If you need more room, an Arduino Mega has 54 digital pins and 16 analog pins, and the Keypad library works identically on it.

For security or access-control projects, the library also supports reading multiple simultaneously pressed keys (full matrix scan) rather than just one at a time. Check the library's [playground documentation](https://playground.arduino.cc/Code/Keypad/) for the multi-key event API.

## References and further reading

- [Arduino Playground — Keypad Library](https://playground.arduino.cc/Code/Keypad/) — complete API reference for the library used in this post
- [Last Minute Engineers: 4x4 Keypad Tutorial](https://lastminuteengineers.com/arduino-keypad-tutorial/) — thorough wiring diagrams and code examples
- [Circuit Basics: How to Set Up a Keypad](https://www.circuitbasics.com/how-to-set-up-a-keypad-on-an-arduino/) — beginner-friendly intro with wiring diagrams
- [CircuitDigest: Inside a 4x4 Membrane Keypad](https://circuitdigest.com/microcontroller-projects/interface-4x4-membrane-keypad-with-arduino) — explains the physical construction of the membrane
- [Arduino Reference — Wire Library](https://www.arduino.cc/reference/en/language/functions/communication/wire/) — I2C communication reference, useful for LCD troubleshooting
- [I2C Scanner Sketch](https://playground.arduino.cc/Main/I2cScanner/) — finds the address of any connected I2C device
