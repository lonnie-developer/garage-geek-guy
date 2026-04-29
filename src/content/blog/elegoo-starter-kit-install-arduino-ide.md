---
title: 'Elegoo Starter Kit #1: Installing the Arduino IDE and Selecting Your Port'
description: 'Kicking off a new series with the Elegoo Most Complete Starter Kit — downloading the IDE and drivers from elegoo.com/download, selecting the right COM port, and verifying the connection with the serial monitor.'
pubDate: 'October 26 2019'
youtubeId: 'ZKC0fgAPbK0'
heroImage: '../../assets/posts/elegoo-starter-kit-install-arduino-ide/thumbnail.jpg'
tags: ['arduino', 'elegoo', 'ide', 'beginner', 'starter-kit', 'tutorial']
---

Seven years is a long time away from Arduino. Long enough that the ecosystem has changed in meaningful ways — the IDE is on a newer version, the community has grown enormously, and the hardware landscape looks different. But the fundamentals are the same, and the first step is still the same: install the IDE and get the board talking to the computer.

This is lesson one of a series using the [Elegoo Most Complete Starter Kit](https://amzn.to/2PjdurN). Elegoo reached out and sent the kit a few months back, and the unboxing video got me genuinely excited to dig into it — excited enough to actually start the tutorial series rather than just leaving the kit on a shelf. If you want to follow along with exactly the same hardware, that link will get you the same kit.

## Why Windows for Arduino development

The setup is a Windows machine for the Arduino programming side and a MacBook Air for research. That's a deliberate split. Windows has historically been friendlier to Arduino development, particularly with clone boards — and most Arduino boards you'll encounter in starter kits are clones, including the Elegoo UNO in this kit.

The issue is USB-to-serial chips. Official Arduino boards use an ATmega16U2 (on the Uno R3 and later) as the USB-to-serial bridge. Clone boards typically use a CH340G or CH341, which is cheaper and works fine, but requires a driver that doesn't ship with Windows out of the box — and definitely isn't installed by default on macOS. Installing CH340 drivers on a Mac adds a step that can involve kernel extension approval in System Preferences, a reboot, and occasionally a fight with Gatekeeper. On Windows the same driver installs quietly and the board shows up in Device Manager immediately. If you have a choice of machines for an Arduino setup and one is Windows, use that one.

## Where to get the Elegoo software

There are two ways to install the Arduino IDE: the official Arduino website at [arduino.cc/en/software](https://www.arduino.cc/en/software), and the Elegoo download page at [elegoo.com/download](http://www.elegoo.com/download). The Elegoo page is worth visiting even if you install the IDE from Arduino directly, because it hosts the PDF tutorial documentation for each kit model — detailed enough that it covers library installation, code examples, and wiring diagrams for every lesson. The download is around 250 MB.

One thing worth noting from the Arduino IDE download page: it prompts you to donate before downloading. There's a "just download" option right there alongside the contribute button. The documentation for this, bless their hearts, explicitly says to click "just download." Arduino is open-source, the IDE is free, and if you want to support the project there are better ways than a one-time donation prompt — but don't let the prompt create the impression that you owe anything before you can download.

## Installing and first launch

The IDE install is straightforward on Windows — run the installer, accept the defaults. The IDE will install any necessary drivers for official Arduino boards automatically. For clone boards with the CH340 chip, you may need to install the CH340 driver separately if the board isn't recognized. The Elegoo download page includes the driver for exactly this reason.

First launch gives you the familiar IDE: the toolbar at the top, the code editor in the center, the output console at the bottom. Before you upload anything, two things need to be configured in the Tools menu: the board type and the port.

## Board selection

Go to Tools → Board and select "Arduino Uno" for the Elegoo UNO R3. Despite being a clone, the board is functionally identical to the original Uno for purposes of the IDE — same bootloader, same ATmega328P, same pin assignments. The IDE doesn't need to know it's an Elegoo.

## Port selection — the grayed-out gotcha

The port dropdown under Tools → Port will be grayed out until you plug in the Arduino. This trips up a lot of first-time users who try to select the port before connecting the board. Plug in the USB cable, wait a moment, then go back to Tools → Port. You'll see something like "COM3 (Arduino Uno)" on Windows, or "/dev/cu.usbserial-..." on Mac.

If the port shows up but says something like "COM3 (Unknown)" without naming the Arduino, the board is connected but the driver isn't installed. Go install the CH340 driver from the Elegoo download page and try again.

## One thing Elegoo got right

The Elegoo UNO has a small design detail that's easy to overlook until you've been bitten by its absence: the pin labels are printed on the sides of the female headers — not just on the PCB silkscreen, but right on the plastic housing of the connectors. So instead of reading a number off a board and then counting pins to figure out where your jumper is going, you can read the label directly on the connector as you're pushing the wire in.

This matters more than it sounds. Off-by-one pin errors are genuinely common with standard Arduino boards, especially if you're looking at the board at any angle. The parallax between where your eye is and where the board reads as "pin 5" can land your jumper on pin 4 or 6 before you notice. Having the label right there on the connector housing is the kind of small ergonomic improvement that you don't think to ask for until you've mislabeled a pin one too many times.

## Opening the serial monitor

The last step of lesson one is confirming the connection by opening the serial monitor — Tools → Serial Monitor (or the magnifying glass icon). Select the baud rate matching your sketch (the default Blink sketch doesn't send serial output, but the serial monitor opening without errors is confirmation that the port is recognized and the connection is live).

If everything's in order: IDE installed, board plugged in, COM port selected, serial monitor responding. That's lesson one done.

## What's next

Lesson two in the Elegoo documentation goes into library management — how to install libraries from the Library Manager and how to import libraries from a .zip file. That's where the more interesting sensors and components start coming into play.

## What you'll need

- [Elegoo Most Complete Starter Kit UNO R3](https://amzn.to/2PjdurN) — the hardware used throughout this series
- [Arduino IDE](https://www.arduino.cc/en/software) — free download from arduino.cc
- [Elegoo downloads page](http://www.elegoo.com/download) — PDF tutorials and CH340 driver

## References and further reading

- [Arduino IDE download page](https://www.arduino.cc/en/software) — official IDE, all platforms
- [Getting started with Arduino — official guide](https://docs.arduino.cc/learn/starting-guide/getting-started-arduino/) — board selection, uploading, and serial monitor basics
- [CH340 driver information and download](https://sparks.gogo.co.nz/ch340.html) — if your clone board doesn't show up in the port list
- [Elegoo download center](http://www.elegoo.com/download) — kit-specific tutorials and driver package
