---
title: 'Program a TI Launchpad MSP430 Like an Arduino with Energia'
description: 'The TI MSP430 LaunchPad costs $4.30 and runs on the same code as an Arduino — thanks to Energia, a community-built IDE that ports the Arduino framework to TI microcontrollers.'
pubDate: 'August 14 2012'
youtubeId: '-KKmkwHapSw'
heroImage: '../../assets/posts/program-launchpad-msp430-energia/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'energia', 'arduino', 'microcontrollers', 'tutorial']
---

There's a version of the Arduino's origin story that doesn't get told often: in 2012, TI shipped a microcontroller development board called the MSP430 LaunchPad for $4.30 — not forty-three dollars, not fourteen — four dollars and thirty cents. Shipping included. The Uno that most Arduino beginners started with cost around $30. The LaunchPad was built around TI's own MSP430 chip, which runs at lower voltages and burns far less power than an ATmega328, and TI practically gave it away because they wanted developers writing MSP430 firmware. The hardware was a deal. The software was the problem.

Then Energia happened.

Energia is an open-source IDE that ports the Arduino framework to TI microcontrollers — same editor, same Blink example, same `setup()` / `loop()` structure, same library conventions, almost the same exact code. If you already know Arduino, you can have a LaunchPad blinking its onboard LED in about ten minutes. This post walks through exactly that demo, covers the one pin-numbering gotcha you'll hit on day one, and points you to the community that has kept Energia going.

> *This video is from 2012, back when the channel was still called meanPC.com. Same bench, same Lonnie, different logo on the screen.*

## The MSP430 and why it matters

The MSP430 is TI's family of 16-bit ultra-low-power microcontrollers, in continuous production since 1993 and found in everything from utility smart meters to medical implants to remote sensor nodes. The flagship property of the family is power consumption — an MSP430 in standby can run for years on a coin cell. That's not relevant when you're blinking LEDs on a workbench, but it's the reason TI has been selling these chips for three decades and why the platform has real industrial backing.

The [MSP430 LaunchPad](https://www.ti.com/tool/MSP-EXP430G2) (officially the MSP-EXP430G2) is TI's entry-level development board. At $4.30 it was clearly a loss-leader, TI subsidizing hardware to build developer mindshare in a market dominated by Arduino and AVR. The board includes two onboard LEDs, a USB connection for programming and serial communication, and an onboard programmer — so the $4.30 gets you everything you need to write and run firmware right out of the box.

## What Energia is — and where the name comes from

Energia was built by a community of developers centered on the [43oh.com forum](https://43oh.com), the MSP430 enthusiast hub that predates the LaunchPad launch. The project took the Arduino IDE's codebase and wired it to TI's compiler toolchain, with a hardware abstraction layer that maps Arduino's `digitalWrite()`, `analogRead()`, `Serial.print()`, and the rest onto MSP430 register operations. The result is that most Arduino sketches run without modification — or need only minor porting.

As for the name: Energia was a Soviet heavy-lift rocket program from the 1980s, used to launch the Buran shuttle. The connection to microcontrollers is loose at best, but the name stuck. The project lives on [GitHub at energia/Energia](https://github.com/energia/Energia), and the 43oh forum remains the main support community.

## What you'll need

- TI MSP430 LaunchPad (MSP-EXP430G2) — check eBay or the TI store
- Energia IDE — download from [energia.nu](http://energia.nu/) or the GitHub repo
- A USB cable to connect the LaunchPad to your computer

No breadboard, no components, no wiring — the onboard LED handles the first demo.

## Installing Energia

Installation mirrors Arduino almost exactly. Download the zip, extract it somewhere sensible, and launch the executable. On Windows you may need to install a driver for the LaunchPad's USB interface; the 43oh forum has pinned threads covering this for every OS. Once the IDE opens, it will look almost identical to the Arduino IDE: the same compile/upload toolbar, the same serial monitor, the same `File → Examples` menu structure.

## Selecting your board and port

Before uploading, tell Energia which hardware you have. Go to `Tools → Board` and select your LaunchPad variant — if you have the original MSP-EXP430G2, look for `LaunchPad w/ msp430g2553` or similar. Then set `Tools → Serial Port` to whatever port the LaunchPad shows up on. On Windows that'll be a COM port; on Mac it'll be something like `/dev/tty.usbmodem`.

## The Blink sketch — and the gotcha

Here's the standard Arduino Blink sketch, exactly as it appears in `File → Examples → Basics → Blink`:

```cpp
int LED = 13;  // Built-in LED on most Arduino boards

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
  delay(1000);
}
```

Paste that into Energia and upload it. It will compile and upload fine. The LED probably won't blink. This is the first thing everyone runs into.

**On the MSP430 LaunchPad, the built-in LEDs are not on pin 13.** LED1 is on pin 2; LED2 is on pin 14. (The exact numbers can shift depending on which chip variant is socketed — the original G2 boards shipped with either the G2231 or G2553 — so check the [Energia pinout map for your specific board](https://energia.nu/pinmaps/) if the numbers below don't match.)

Change the pin assignment to 14 and re-upload:

```cpp
int LED = 14;
```

Hit upload, watch the LaunchPad — the LED blinks at one-second intervals, same as an Arduino Mega running the identical sketch next to it. That's the whole point. Same code, different hardware, a fraction of the cost.

## The libraries situation

One of the big selling points of Energia's early growth was the library porting effort on 43oh. The community had already brought over the Servo library, I2C (`Wire`), SPI, serial LCD drivers, and many of the common peripheral libraries by the time this video was made. The ports aren't always complete — some libraries rely on ATmega-specific timer registers and need adaptation — but for the majority of common Arduino shields and modules, something workable had already been ported.

The 43oh Energia forum section was where you went to ask "does library X work?" and usually got an answer within a day. That community knowledge is still searchable today even if new activity has slowed.

## Where Energia fits today

Energia's development has slowed as TI shifted focus to [Code Composer Studio](https://www.ti.com/tool/CCSTUDIO) and the newer SimpleLink ecosystem. But the project still works, the 43oh community still answers questions, and for the MSP430G2 LaunchPad specifically, Energia remains the easiest possible on-ramp for anyone coming from Arduino.

The honest pitch in 2012 — and still roughly true today for hobby work — was: if you need ultra-low-power operation, if you're building something battery-operated that needs to sleep for months, or if you just picked up a LaunchPad and want to see it do something in the next fifteen minutes, Energia is where you start. It's not better than Arduino for general tinkering. It's better than Arduino for MSP430, which is a very specific sentence that happens to matter a lot when you're trying to run a wireless sensor node for two years on a pair of AAs.

## References and further reading

- [Energia IDE downloads and documentation](http://energia.nu/)
- [Energia on GitHub (energia/Energia)](https://github.com/energia/Energia)
- [43oh.com — MSP430 community forum and Energia support](https://43oh.com)
- [TI MSP-EXP430G2 LaunchPad product page](https://www.ti.com/tool/MSP-EXP430G2)
- [Energia pinout maps by board variant](https://energia.nu/pinmaps/)
- [MSP430G2553 datasheet (PDF)](https://www.ti.com/lit/ds/symlink/msp430g2553.pdf) — the chip on most original LaunchPads
- [Wikipedia: Energia (rocket)](https://en.wikipedia.org/wiki/Energia_(rocket)) — the Soviet launcher the IDE is named after
