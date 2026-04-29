---
title: 'ClusterBot Build — Soldering Headers onto the Pololu Motor Driver'
description: 'Soldering pin headers onto the Pololu dual DC motor driver board for the ClusterBot Arduino robot. Covers why the headers matter, alignment technique, and how the board bridges Arduino logic to motor power.'
pubDate: 'January 16 2012'
youtubeId: 'uiDYZZx-W-U'
heroImage: '../../assets/posts/clusterbot-solder-pololu-motor-driver-headers/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'soldering', 'motor-driver', 'tutorial']
---

*Episode 3 of the ClusterBot build series — an Arduino obstacle-avoidance robot. This step: preparing the Pololu dual DC motor driver for use by soldering on the breakout headers.*

Pololu ships most of their carrier boards and breakout modules without headers soldered on. This is a deliberate choice: the same board might get soldered directly into a PCB, connected with loose wires, or mounted on a breadboard, and each of those installations wants a different header type or no header at all. You get a bare board and you add what you need.

For ClusterBot, the motor driver goes on the breadboard for prototyping — a half-size breadboard with the Arduino and a few other components on it, all clustered together on the chassis platform. That means standard 0.1" male headers: the type that plug into breadboard holes and let you connect jumper wires.

## The Pololu dual DC motor driver

The specific board here is Pololu's dual DC motor driver, most likely the TB6612FNG carrier or a similar H-bridge-based driver that was available from Pololu in early 2012. The TB6612FNG (made by Toshiba) was popular for small robot builds — it handles two independent DC motors, operates from 2.7V to 13.5V motor supply, and pushes up to 1.2A continuous per channel with 3A peak. That's enough for two Tamiya motors with headroom.

The driver is an H-bridge: it can push current through each motor in either direction, which is what gives you both forward and reverse control. A simple PWM signal on the speed pin sets how fast, and a digital direction pin sets which way. The Arduino controls both — it never touches the motor current directly.

## Soldering the headers

The headers themselves are a row of 0.1"-pitch male pins that press through the through-holes on the carrier board and get soldered from the back. The challenge is keeping them perpendicular to the board during soldering — a row of pins that's tilted five degrees off vertical will still fit in a breadboard, but with much more friction and a tendency to pull out if you're not careful.

The standard technique: place the header strip in the breadboard first (pins pointing up), then place the carrier board on top of the pins (through-holes down). The breadboard holds the header perfectly vertical and at the correct pitch. Flip the whole assembly over and solder the pins from the top of the carrier board with the breadboard facing down. Gravity and the breadboard's grip keep everything aligned while you work.

Solder one pin at each end of the row first — that locks in the alignment — then work your way through the remaining pins. Each joint should take two to three seconds: enough time for the solder to flow and wet both the pin and the pad, not so long that you push heat into the board or the adjacent pin.

## What the pins connect to

The TB6612FNG carrier has two sets of connections: the motor output side and the control input side.

On the control side, the pins are: VM (motor power supply, up to 13.5V), VCC (logic supply, 3.3V or 5V), GND, and then the control signals — AIN1, AIN2, PWMA for motor A, and BIN1, BIN2, PWMB for motor B, plus a STBY (standby) pin that must be pulled high to enable the chip. The AIN/BIN direction pins connect to Arduino digital output pins; PWMA/PWMB connect to Arduino PWM pins (3, 5, 6, 9, 10, or 11 on the Uno) for speed control. STBY goes to a digital pin that you pull high in `setup()`.

On the output side, the motor output pads — AO1, AO2 for motor A, BO1, BO2 for motor B — are where the Tamiya motor wires from the previous episode connect. These are screw terminal or solder pad connections rather than header pins, since they carry motor-level current (up to 1.2A) that would be uncomfortable running through a breadboard header.

## The key distinction: logic ground vs. motor ground

Both the Arduino and the motor driver need a common ground reference. The motor supply can be a separate battery from the Arduino supply — and for ClusterBot it is — but the GND of both supplies must be connected together at the motor driver board. If the grounds aren't tied, the direction logic signals from the Arduino (which reference Arduino's GND) are meaningless to the driver board (which has a different reference). The symptom: unpredictable motor behavior or no response at all.

This common-ground requirement trips up a lot of first-time robot builds. Tie the grounds.

## ClusterBot build series

1. [Assemble the Pololu chassis](/blog/clusterbot-pololu-robot-chassis-assembly)
2. [Solder wires to the Tamiya motors](/blog/clusterbot-solder-tamiya-motor-wires)
3. Solder headers onto the Pololu motor driver **(this episode)**
4. [Install the battery pack](/blog/clusterbot-arduino-battery-pack)
5. [Finish the frame](/blog/clusterbot-finish-robot-frame)
6. [HC-SR04 obstacle avoidance live demo](/blog/clusterbot-hcsr04-obstacle-avoidance-demo)

## References and further reading

- [TB6612FNG dual motor driver carrier | Pololu](https://www.pololu.com/product/713) — datasheet, pinout, and sample code
- [TB6612FNG datasheet | Toshiba](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf) — full electrical specifications
- [Adafruit motor driver tutorial](https://learn.adafruit.com/adafruit-motor-shield/overview) — a different driver but a clear explanation of why H-bridges are needed for DC motor direction control
- [Soldering header pins tutorial | SparkFun](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering) — the same breadboard-alignment technique described above, with photos
