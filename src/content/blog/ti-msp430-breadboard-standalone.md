---
title: 'Pulling the MSP430 Off the Launchpad: A Standalone Hello World on a Breadboard'
description: 'The TI MSP430 Launchpad ships with two chips and a DIP package you can actually remove. Here is how to take the chip off the board, run it from two AA batteries, and get blinking LEDs on a bare breadboard for about 50 cents in parts.'
pubDate: 'January 03 2012'
youtubeId: 'K_7Xxq4B2rg'
heroImage: '../../assets/posts/ti-msp430-breadboard-standalone/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'breadboard', 'microcontroller', 'tutorial', 'beginners']
---

There's a thing Arduino does that's worth naming out loud: it makes the microcontroller non-extractable. The ATmega328P on an Uno is a surface-mount device, soldered to the board. You can program it, run it, experiment with it — but at the end of the day, the chip stays on that specific PCB. If you want a standalone circuit built around an Arduino, your options are basically "use the whole Uno as a component" or "get a bare ATmega and figure out how to program it separately."

Texas Instruments' MSP430 Launchpad sidesteps this in an interesting way. The MSP430 chips in the G2 Launchpad kit are DIP packages, socketed into the development board. When you're done prototyping, you pop the chip out of the socket and drop it directly onto a breadboard. No separate programmer needed — you already programmed it. The chip carries its firmware with it.

That's what this post is about: the first project, which involves pulling the MSP430 off its Launchpad board and running it standalone on a breadboard from two AA batteries, blinking LEDs for about 50 cents in parts.

> *This build is from January 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench. It's also the first circuit ever built on a breadboard here, which explains some of the wiring.*

## The Launchpad kit itself

The TI MSP430 Launchpad (part number EXP430G2) was $4.30 when it launched in 2010 — the price was a deliberate nod to the chip family's name — and it became one of the more memorable microcontroller bargains of that era. For that price you got:

- A USB programmer/debugger board (the Launchpad itself)
- Two MSP430 chips — one pre-installed, one spare
- Pin headers, stickers, and a micro crystal
- A reset button, a user button, and a red and green LED on the board

The pre-installed chip was typically an MSP430G2231 or G2452, depending on the kit version, and it came pre-programmed with a blinking LED demo. This is what "hello world" looks like on a microcontroller: the chip already knows how to blink by the time it ships.

The G2 series chips are tiny low-power microcontrollers — 8KB to 16KB of flash, 256 to 512 bytes of RAM, clocked at up to 16 MHz, running on 1.8–3.6V. They're not the chip you'd reach for if you need USB, heavy number crunching, or a lot of I/O. They're the chip you reach for when something needs to run on a coin cell for six months without a battery change.

## Why 3V matters

The Arduino ecosystem runs on 5V (or 3.3V for the later boards), which maps cleanly to a 9V battery through the Uno's onboard regulator or USB from a laptop. The MSP430 G2 series runs on 1.8–3.6V, with 3.0V being a comfortable operating point. Two AA batteries in series is exactly 3V nominal — a clean, no-regulator power solution.

The Launchpad's onboard voltage regulator accepts 5V from USB and outputs 3.3V for the chip. Feed it 9V and you'll see about 5.5V out of the regulator — too much for the MSP430, which will get warm and potentially fail. This was confirmed the hard way: the chip survived, but it was a closer call than it should have been. Stick to USB for programming, and two AAs for standalone use.

## The circuit

The pre-programmed demo alternates between two LEDs — one on each output pin of the MSP430. The hardware to make that work on a breadboard:

**Power supply:**
- Two AA batteries in series → 3V
- A switch in series (optional but convenient)
- Positive rail → VCC pin (pin 1) of the MSP430
- Negative rail → GND pin (pin 14, or the appropriate GND for your chip variant) and VSS

**Reset pin pull-up:**
The RST/NMI pin needs to be pulled high for normal operation. Without this, the chip resets continuously and nothing works. Connect a resistor — 47K to 100K works — from the RST pin to VCC. This was the part that took the longest to figure out on this build, because the symptom (chip not running) looks identical to "the chip is broken" or "the power is wrong." The answer was in the datasheet the whole time.

**LED connections:**
- LED 1: pin P1.0 → 100Ω resistor → LED anode → LED cathode → GND
- LED 2: pin P1.6 → 100Ω resistor → LED anode → LED cathode → GND

100Ω series resistors are on the conservative side for 3V — the LEDs will be dimmer than at 5V, which is fine. The formula: (3V - 2V forward drop) / 0.01A = 100Ω. If you want brighter LEDs, drop to 68Ω or even 47Ω. Don't go below 33Ω at 3V.

The pre-programmed firmware alternates the two LEDs, giving you the classic red-green blink that serves as the MSP430's equivalent of "hello world."

## Programming before you remove the chip

The Launchpad's programming interface connects to the chip through a 10-pin JTAG/Spy-Bi-Wire header. Before removing the chip from the board, program it with whatever code you want it to run standalone. The chip retains its program in non-volatile flash — removing power doesn't erase it.

The TI development environment at the time was Code Composer Studio (free version available) or IAR Embedded Workbench. Energia, the Arduino-like IDE for MSP430, came along slightly later and is the easier on-ramp if you already know Arduino syntax. The pre-installed demo doesn't require any of this — it's already there when you open the box.

After programming, carefully remove the chip from its socket. DIP chips can be stubborn; use a small flathead screwdriver to lever up each end a little at a time rather than prying from one end, which bends pins. Straight pins are much easier to breadboard.

## What it costs

The components for the standalone circuit (not counting the batteries or breadboard):
- MSP430 chip: included in the kit, but ~$0.25 for the G2231 in single quantities from TI Direct
- 2× 100Ω resistors: ~$0.01 each
- 1× 100K resistor (reset pull-up): ~$0.01
- 2× LEDs: ~$0.10 each

Total: roughly $0.50 in parts, not counting the batteries or breadboard. That's including the processor.

This is the value proposition of the MSP430 family in concrete terms. The chips aren't as versatile as an Arduino for complex projects, but when the application fits — low power, simple I/O, battery operation — they're hard to beat on cost.

## What didn't work cleanly

Two things cost time on this build:

**The reset pin.** It's not obvious from the Launchpad schematic that you need an external pull-up when removing the chip, because the Launchpad board itself handles this internally. The datasheet says it clearly, but it's easy to miss if you're starting from a "it worked on the Launchpad" assumption. If your standalone chip isn't running at all, the reset pull-up is the first thing to check.

**The battery holder.** The solution here was male pin headers pressed into AA battery terminals — functional, but mechanically unstable. The right solution is a proper 2× AA battery holder with JST or wire leads, available for about $1. Spend the dollar.

## Where standalone chips fit

The DIP package and sub-$1 per-unit pricing make the MSP430 G2 series genuinely useful as a "leave it in the project" part. You build the circuit on a breadboard, debug it, transfer to perfboard or a cheap PCB, and the chip that was in your breadboard is the chip in the finished thing. No separate production programming run, no different chip variant to account for.

Arduino makes this harder — not impossible (the ATmega can be burned with a bootloader and programmed standalone with an ISP programmer), but harder. The Launchpad's socket is a real convenience for the "prototype to product" workflow on projects that fit the MSP430's capabilities.

For projects that need more RAM, more flash, USB, or 5V I/O, the MSP430 G2 isn't the right chip. But for blinking LEDs, reading a button, driving a sensor, or logging data on batteries for months at a time, it's a remarkably cost-effective part.

## References and further reading

- [MSP430G2 Launchpad user guide (SLAU318)](https://www.ti.com/lit/ug/slau318g/slau318g.pdf) — TI's official user guide for the EXP430G2 kit; the circuit schematic showing internal pull-ups is here
- [MSP430G2231 datasheet](https://www.ti.com/lit/ds/symlink/msp430g2231.pdf) — chip-level spec including pinout, operating voltage range, and I/O current limits
- [Energia IDE](https://energia.nu/) — Arduino-compatible development environment for MSP430 Launchpad; far easier entry point than Code Composer Studio
- [TI MSP430 Launchpad community](https://e2e.ti.com/support/microcontrollers/msp-low-power-microcontrollers-group/msp430/f/msp430-forum) — TI's E2E forum; the place to look if something isn't working and the datasheet didn't help
- [MSP430 standalone circuit basics](https://energia.nu/guide/pinmaps/launchpad-msp430g2/) — Energia's Launchpad pinout reference; useful for mapping Launchpad pin numbers to breadboard positions
- [TI's MSP430 ultra-low-power primer](https://www.ti.com/lit/an/slaa478b/slaa478b.pdf) — application note on low-power design with the G2; covers the specific features that make the chip interesting for battery-powered projects
- [ATmega standalone (for comparison)](https://docs.arduino.cc/built-in-examples/arduino-isp/ArduinoToBreadboard/) — Arduino's own guide for running an ATmega standalone; useful to compare the two approaches
