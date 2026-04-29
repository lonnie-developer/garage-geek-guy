---
title: 'Using the TI Launchpad as an In-System Programmer for MSP430 Chips'
description: 'You already own an MSP430 programmer. Pull three jumpers off the Launchpad and you can flash chips in-circuit on a breadboard — no separate programmer needed. Here is the four-wire hookup and why it beats the pop-and-swap approach.'
pubDate: 'October 19 2012'
youtubeId: 'dL2YPS96L18'
heroImage: '../../assets/posts/msp430-launchpad-isp-programmer/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'isp', 'energia', 'microcontroller', 'tutorial']
---

Once you've gotten comfortable moving MSP430 chips from the Launchpad socket to a breadboard, the next workflow question is inevitable: how do you reflash a chip that's already wired into a circuit? The options are (a) desocket the chip, move it back to the Launchpad, program it, move it back to the breadboard — bending pins every step — or (b) program it in-place using the Launchpad as an in-system programmer (ISP).

Option (b) is the right answer, and it takes four jumper wires.

The TI Launchpad uses a protocol called Spy-Bi-Wire, TI's two-wire variant of the JTAG debug and programming interface. Those signals are accessible on header pins along the left edge of the board, and with a small modification to the jumper configuration, you can use the Launchpad's USB-connected programmer half to flash any MSP430 chip that's sitting on a breadboard — without disturbing the rest of the circuit.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The one-time setup: pull three jumpers

The Launchpad has a row of jumpers near the top of the board that connect the programmer section to the target chip section. By default, those jumpers are in place so the board programs its own onboard chip. To use the Launchpad as an external programmer, pull the top three jumpers off. This disconnects the programmer from the onboard chip and exposes the raw programming signals on the left-side header pins — GND, VCC, TEST, and RST.

Leave the bottom jumpers in place. The top three are the ones to remove.

With those jumpers pulled, it doesn't matter whether there's a chip in the Launchpad socket or not. The programmer section is now decoupled and ready to drive your external target.

## The four connections

Look at the left side of the Launchpad (the side with the USB connector). You'll see pin labels for GND, VCC, TEST, and RST. Connect each to the corresponding pin on your target MSP430 chip on the breadboard:

| Launchpad pin | Target chip pin |
|---|---|
| GND | GND |
| VCC | VCC |
| TEST | TEST |
| RST | RST/NMI |

The TEST and RST pin locations vary by chip variant — check the datasheet pinout for your specific chip. On the MSP430G2553 (20-pin DIP), TEST is pin 17 and RST is pin 16. The labels on the Launchpad board itself tell you where to find them on the programmer side.

That's the complete wiring. Four wires, no level shifting, no special adapter.

## Programming in Energia

With the target wired up and the Launchpad connected over USB, open Energia and set the board type to match the chip you're programming — MSP430G2553 or MSP430G2452 in this case. There's no separate "programmer" setting to change; the Launchpad's USB interface handles it transparently. Set your COM port, hit Upload, and the chip programs just as if it were in the socket.

The blink sketch used here moved the LED from pin 14 (the Launchpad board's built-in LED) to pin 8 (an external LED on the breadboard):

```cpp
void setup() {
  pinMode(8, OUTPUT);
}

void loop() {
  digitalWrite(8, HIGH);
  delay(100);
  digitalWrite(8, LOW);
  delay(100);
}
```

When programming a different chip variant (switching from G2553 to G2452), change the board type in Energia before uploading. The programmer doesn't care — it'll flash whatever the IDE tells it to — but Energia needs to know the chip variant to compile the correct machine code.

## Programming multiple chips sequentially

This workflow really shows its value when you need to flash several chips in a row. After programming chip 1, unplug USB, move the four jumpers to chip 2 in the next breadboard row, replug USB, and upload again. The chips don't leave the breadboard at any point.

Four chips — three G2553s and one G2452 — were programmed and the whole circuit was wired up in under ten minutes here, including the programming time. The G2452 just needed the board type switched in Energia before the final upload.

Compare this to the pop-and-swap workflow: you'd pull each chip from the breadboard, insert it into the Launchpad socket, upload, pull it out, insert it back in the breadboard. That's six insertion cycles per chip across a four-chip batch, and MSP430 DIP pins are fragile enough that each cycle is a real risk of a bent pin. A bent pin on a 20-pin DIP is a pretty bad day.

One thing to note on reset pull-ups: the in-system approach works fine if the target chip's RST pin has a proper pull-up resistor (4.7 kΩ to VCC is the recommended value). In this build, RST was connected directly to VCC — skipping the resistor — and it worked, but the properly-done version uses the resistor. If your chip behaves erratically between programming sessions, check the reset pin.

## When you'd use this

Any time you have more than one or two MSP430 chips to program, in-system programming is the faster workflow. It's also the right approach when your chips are already wired into circuits with other components — you don't want to be disconnecting and reconnecting a breadboard circuit every time you iterate on code.

The Launchpad's dual role as both a development board and a standalone ISP programmer is one of the things that makes the TI ecosystem efficient for breadboard prototyping. The hardware to do this is already in your hands.

## References and further reading

- [TI MSP430 Launchpad user guide (SLAU318)](https://www.ti.com/lit/ug/slau318g/slau318g.pdf) — the Spy-Bi-Wire header layout and jumper configuration are documented here; Section 2.2 covers the hardware description
- [MSP430G2553 datasheet](https://www.ti.com/lit/ds/symlink/msp430g2553.pdf) — pinout and TEST/RST pin details; Section 18 covers the JTAG/SBW interface
- [MSP430G2452 datasheet](https://www.ti.com/lit/ds/symlink/msp430g2452.pdf) — same programming interface, different peripheral set
- [Energia IDE](https://energia.nu/) — Arduino-compatible environment for MSP430; the one used in this post
- [Spy-Bi-Wire protocol overview (SLAU265)](https://www.ti.com/lit/an/slau265/slau265.pdf) — TI application report on the two-wire debug interface; explains the protocol details
- [MSP430 hardware tools overview](https://www.ti.com/tool/MSP430-GANG) — TI's gang programmer for production; the Launchpad ISP approach is the hobbyist equivalent
