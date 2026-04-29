---
title: 'Cleaning Up Arduino Robot Wiring and Redesigning the Power System'
description: 'Replacing spaghetti jumper wires with pre-cut fitted wires, switching from 4× alkaline AA to 3× rechargeable AA for the motors, and moving logic power to a 9V battery through the Arduino voltage regulator. Why you should clean up before you expand.'
pubDate: 'October 09 2012'
youtubeId: 'r1RSWzFmycc'
heroImage: '../../assets/posts/clean-up-arduino-robot-wiring-power/thumbnail.jpg'
tags: ['arduino', 'robot', 'wiring', 'power-supply', 'tutorial']
---

There's a moment in every breadboard robot project where you have to decide: keep adding things to the spaghetti, or stop and clean it up first. The spaghetti option feels faster in the short run. It isn't.

Loose jumper wires — the kind that are all the same length regardless of how far they need to span — sit high off the breadboard. They snag on things. They fall out when you pick up the robot. They make it almost impossible to trace a connection or debug a problem without pulling three other wires loose in the process. And they're especially bad when you're about to add more connections on top.

This post covers the cleanup, and a simultaneous power system redesign that addresses two problems that showed up during the first test run.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## What was wrong with the power system

The original power setup had everything running from a single 4×AA alkaline battery pack — 6V, with the Arduino also drawing off the same pack. Two problems emerged:

**Problem one: 6V is too fast for the Tamiya twin motor gearbox.** The gearbox motors are rated for about 3V. At 6V they run, but they run hard — battery life was around an hour and the robot moved faster than was useful for tuning obstacle avoidance code. The fix: cut one cell out of the series string by bridging it with a jumper, then replace the remaining three alkaline cells with three rechargeable NiMH AA batteries at 1.2V nominal each. Target voltage: 3.6V. Measured on the bench: 3.8V per cell at full charge, so the pack was coming in around 3.84V. Close enough for the Tamiya motors.

**Problem two: the Arduino shouldn't be on the same rail as the motors.** Motors generate noise on the supply rail when they start, stop, and change direction. Powering logic from the same rail invites resets, glitches, and brownouts at the worst possible moments. The fix: a 9V battery dedicated to the Arduino through its onboard voltage regulator (the barrel jack input, which the regulator drops to a clean 5V). The 5V from the Arduino's output rail then powers the breadboard's logic power rail and — eventually — will power the sensors and display on the top deck.

## The two-supply wiring model

After the redesign, the power topology is:

```
3× NiMH AA (3.8V) ──────────────┬──── TB6612FNG VMOT (motor supply)
                                 │
                                 └──── (motor driver GND → Arduino GND → common ground)

9V battery ──── Arduino barrel jack ──── Arduino 5V output ──── logic breadboard rail
```

Motor supply goes directly to the TB6612FNG's VMOT and GND pins. That's its only destination — the motor driver has its own internal regulation for the logic pins. Logic supply (9V → Arduino regulator → 5V) goes to the breadboard's power rail for everything else: the Arduino itself, sensors, display.

Both supplies share a common ground. This is non-optional — without a common ground reference, the Arduino's signal pins can't communicate reliably with the motor driver's logic pins.

## Replacing the jumper wires

The cleanup approach is methodical: go connection by connection, cut a wire to length, strip and fit it, then move to the next one. Pre-cut jumper wire kits are available cheaply and include short fixed-length wires in multiple colors. You can also cut to length from a spool of solid hookup wire — 22 or 24 AWG works fine on a breadboard.

The practical difference between a fitted wire and a long jumper: the fitted wire lies flat against the breadboard surface. It doesn't loop up over adjacent components. It's visually obvious where it goes. If you need to pull it, you pull just that wire without disturbing anything next to it.

A few things that make this easier:

**Don't cross over chip sockets.** If you're running a wire that could go either over or around a chip, route it around. When (not if) you need to swap a chip, you don't want to move six wires first.

**Do the power connections last.** Leave GND and VCC wires for the end. That way you can see exactly what's being fed where before any of it has power on it.

**Leave motor connections loose until the logic wiring is done.** Motor wires going to the TB6612FNG can be pulled temporarily while you work on the adjacent logic connections — the motor driver's pin spacing makes it easy to bump a logic pin when reaching past it.

## TB6612FNG connection map

For reference, here's how the TB6612FNG is wired on this robot (the same pin assignments from the motor driver build post):

| TB6612FNG pin | Connection |
|---------------|-----------|
| VMOT | Motor battery pack + (3.8V) |
| GND | Common ground |
| VCC | Arduino 5V (logic supply) |
| STBY | Arduino 5V (must be HIGH to enable motor output) |
| AIN1 | Arduino D6 |
| AIN2 | Arduino D7 |
| PWMA | Arduino D10 |
| BIN1 | Arduino D8 |
| BIN2 | Arduino D9 |
| PWMB | Arduino D11 |
| AO1, AO2 | Motor A terminals |
| BO1, BO2 | Motor B terminals |

## Verifying the motor direction

After a wiring cleanup, it's easy to accidentally reverse a motor connection — either at the TB6612FNG output pins or at the motor terminals themselves. The test sketch is simple: run forward for 2 seconds, backward for 2 seconds, repeat.

```cpp
const int AIN1 = 6, AIN2 = 7, PWMA = 10;
const int BIN1 = 8, BIN2 = 9, PWMB = 11;
const int STBY = 5;

void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(STBY, OUTPUT);
  digitalWrite(STBY, HIGH);
}

void forward(int speed) {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
  analogWrite(PWMA, speed); analogWrite(PWMB, speed);
}

void backward(int speed) {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
  analogWrite(PWMA, speed); analogWrite(PWMB, speed);
}

void loop() {
  forward(180);
  delay(2000);
  backward(180);
  delay(2000);
}
```

If the robot spins in place on "forward" instead of going straight, one of the motors is wired in reverse. Fix it by swapping that motor's AO1/AO2 outputs at the TB6612FNG — no need to touch the code.

## What this accomplishes

After the cleanup: the breadboard has fitted low-profile wires instead of a jumper tangle. Power is separated by function — motors on their own battery at a voltage that matches what the motors actually want, logic on clean regulated 5V from the Arduino. The TB6612FNG's STBY pin is explicitly tied high. The whole thing is physically much more stable.

The result is a robot that can be picked up without wires falling out, and a power architecture that can be extended to the next level (sensors, display, more logic) without revisiting the foundation. The next posts cover adding the HC-SR04 sensors and the I²C LCD on the top deck.

## References and further reading

- [TB6612FNG datasheet (Toshiba)](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf) — the VMOT/VCC separation, STBY behavior, and maximum motor current specs
- [NiMH AA battery specifications](https://data.energizer.com/pdfs/nickelmetalhydride_appman.pdf) — Energizer's application manual; covers the 1.2V nominal vs 1.28V fresh voltage and discharge curves
- [Arduino Uno voltage regulator input range](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) — the barrel jack input accepts 7–12V; 9V is the standard safe choice
- [SparkFun TB6612FNG breakout hookup guide](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide) — clear walkthrough of the dual H-bridge including the STBY gotcha
- [Tamiya twin motor gearbox (Item #70168)](https://www.tamiyausa.com/shop/educational-construction/twin-motor-gearbox-kit/) — the gearbox used on this chassis; rated for 1.5–3V per the documentation
