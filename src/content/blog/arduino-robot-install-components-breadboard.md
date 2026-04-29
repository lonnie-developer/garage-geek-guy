---
title: 'Affordabot Build #2: Installing the Breadboard, Motor Driver, and Battery Pack'
description: 'Mounting an Arduino Nano and TB6612FNG motor driver onto a mini breadboard, then Gorilla-Gluing the whole assembly into the TI Launchpad box chassis — the innards of a cheap robot taking shape.'
pubDate: 'October 7 2012'
youtubeId: 'zNBp1xN93PA'
heroImage: '../../assets/posts/arduino-robot-install-components-breadboard/thumbnail.jpg'
tags: ['arduino', 'robot', 'tb6612fng', 'motor-driver', 'breadboard', 'affordabot']
---

*This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

One of the enduring tensions in robot builds is the packaging problem. You've got a microcontroller, a motor driver, sensors, a battery pack, and a pile of wires that need to coexist inside or on top of a chassis that's already committed to being as small as possible. On a full-size wheeled platform you can just velcro things down in whatever order makes sense. Once your robot is the size of a shoebox or smaller, every component placement is a negotiation.

This is Affordabot build number two. The chassis is a repurposed TI MSP430 Launchpad cardboard box — free, stiff enough for the purpose, and roughly the right size. Build one covered the chassis itself. This video is about what goes inside it: an Arduino Nano on a mini breadboard, a Toshiba TB6612FNG motor driver on its carrier board, and a 4-AA battery pack. Plus some foam spacers and a bottle of Gorilla Glue used for the first time, results to be determined.

## The Nano + TB6612FNG combination

The Arduino Nano handles the logic. It's the same ATmega328P as the Uno but in a breadboard-native form factor — it straddles the center gap of a mini breadboard, with both rows of pins accessible on either side. For a robot this size, it's a much cleaner fit than trying to cram an Uno somewhere.

The motor driver is a Toshiba TB6612FNG on a small carrier breakout board. The TB6612 is a dual H-bridge built with MOSFET technology rather than the bipolar transistors used in the L298N — the motor driver that shows up in most entry-level robot tutorials. That difference matters in practice. The L298N burns a surprising amount of its motor supply as heat: at 1 A of current per channel you're looking at 2–4 V dropped internally, which comes straight off your battery life and goes straight into a heatsink. The TB6612's MOSFET H-bridge drops only about 0.2–0.5 V at the same current. For a battery-powered robot, that's real.

The TB6612FNG can handle up to 13.5 V on the motor supply side and 1.2 A continuous per channel (3.2 A peak), which is plenty for the small Tamiya motors on this chassis. It also has a standby mode the L298N lacks, which lets you put the motor outputs in a low-power state when the robot isn't driving.

The breadboard carriers for the TB6612 (Pololu makes a popular one) bring the chip's pins out to 0.1" headers that drop into a breadboard just like any other DIP component. The Nano and the TB6612 carrier sit on the same mini breadboard, connected by short jumper wires. The whole brain-plus-driver assembly is a single compact unit, maybe 3" × 1.5", that can be mounted as one piece.

## The clearance problem

The chassis box has wheels and drivetrain hardware underneath it, and those protrude up past the floor of the box. Laying the breadboard assembly flat on the bottom would mean it's sitting on top of the tire assemblies — not ideal, mechanically or electrically.

The fix is foam spacers. A sheet of craft foam cut to roughly the footprint of the breadboard gets Gorilla Glued to the box floor, raising the breadboard assembly up enough to clear the tire/wheel assembly with some margin. The foam is thick enough to provide the needed height but still leaves room overhead for sensors on the lid and an LCD on the front panel.

The same spacer approach works for the battery pack. A 4-AA battery holder needs to live toward the back of the box where the weight distribution helps stability, but there are zip ties and wire bundles in the way along the bottom edge. A second small foam pad raises the battery pack above the clutter and gives the Gorilla Glue a flat surface to bond to.

## First time with Gorilla Glue

Gorilla Glue is a polyurethane-based adhesive rather than a cyanoacrylate (super glue) or epoxy. It expands slightly as it cures (sometimes a lot, depending on how much moisture is present), and it needs clamping time — the bond isn't instant. For this build it worked well for bonding foam to cardboard, which hot glue would have handled equally well. Hot glue would also have been faster. The Gorilla Glue went down with a work time long enough to position everything before it set, which was useful for aligning the battery pack orientation.

The takeaway from using it the first time: less is more. The expansion means a thin coat is usually enough, and too much will squeeze out the sides and need cleanup. Roughing up the surfaces slightly helps adhesion.

## Layout planning

With the foam spacers glued down and the breadboard + battery pack dry-fitting in position, the plan for the remaining wiring becomes clearer. The breadboard sits toward the front-center of the box, accessible through the lid. The battery pack is toward the rear. The power switch comes through the side of the box — keeping it accessible without opening the lid every time. Motor connectors come from the front corners where the Tamiya gearbox motors live.

Sensor mounts will go on the front edge — HC-SR04 ultrasonic sensors for obstacle detection. An LCD will eventually mount on the front panel for status readout. All of those wire runs are short from the breadboard's position, which was the goal of putting the brain in the center rather than at one end.

The lesson here applies to any robot build: route power at the start, not the end. Knowing where the switch is, where the battery connects, and where the grounds come together before anything is glued down makes everything easier than discovering it after the adhesive has cured.

## What's next

The Gorilla Glue needs overnight to fully cure before any stress testing. Once it's solid, the next steps are wiring the Nano to the TB6612FNG, running power to the breadboard from the battery pack, and getting the motors turning under code. The mechanical layout is now set.

## References and further reading

- [TB6612FNG datasheet (Toshiba)](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf) — full electrical specs for the motor driver
- [Pololu TB6612FNG carrier board](https://www.pololu.com/product/713) — the popular carrier board that brings the chip to breadboard-friendly headers
- [TB6612FNG vs. L298N comparison — Hackster.io](https://www.hackster.io/news/tb6612fng-motor-driver-better-than-the-l298n-7499a7574e63) — why the MOSFET-based driver is generally the better choice for small robots
- [Arduino Nano documentation](https://store.arduino.cc/products/arduino-nano) — pinout and specs for the brain of this build
