---
title: 'First Test Run of the Arduino Cardboard Robot — TB6612FNG Motor Code'
description: 'Taking the cardboard chassis robot from wired up to actually moving: borrowing motor subroutines from an earlier bot, calibrating uneven motor outputs with different PWM values, and diagnosing a rear caster height problem live on the floor.'
pubDate: 'October 08 2012'
youtubeId: 'aIyZvwsnSDw'
heroImage: '../../assets/posts/arduino-robot-test-code-run/thumbnail.jpg'
tags: ['arduino', 'robot', 'tb6612fng', 'motor-driver', 'tutorial']
---

There's a specific kind of moment in any robot build where you've wired everything up, you think it should work, and you're about to find out if you're right. The first test run on the cardboard chassis is that moment.

The hardware at this point: a Tamiya twin motor gearbox on a cardboard box chassis, driven by a TB6612FNG dual H-bridge motor driver, controlled by an Arduino Nano. Three rechargeable AA batteries for the motors (~3.8V), a 9V battery through the Arduino's voltage regulator for logic. Wiring was cleaned up in the previous post. Time to actually drive.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## Borrowing code from ClusterBot

Rather than write motor subroutines from scratch, the test uses code from ClusterBot — an earlier robot built with the same TB6612FNG. The subroutine structure is reusable: `forward()`, `backward()`, `rotateLeft()`, `rotateRight()`, `turnAround()`. Each one sets the direction pins for both motors and applies PWM.

The TB6612FNG pin assignments used throughout this robot build:

```cpp
#define PWMA  10   // Motor A speed (PWM)
#define PWMB  11   // Motor B speed (PWM)
#define AIN1   6   // Motor A direction bit 1
#define AIN2   7   // Motor A direction bit 2
#define BIN1   8   // Motor B direction bit 1
#define BIN2   9   // Motor B direction bit 2
#define STBY   5   // Standby — must be HIGH to enable outputs
```

The setup and direction logic:

```cpp
void setup() {
  pinMode(PWMA, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT);
  pinMode(STBY, OUTPUT);
  digitalWrite(STBY, HIGH);  // take driver out of standby
}

void forward(int speedA, int speedB) {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
  analogWrite(PWMA, speedA);
  analogWrite(PWMB, speedB);
}

void backward(int speedA, int speedB) {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH);
  analogWrite(PWMA, speedA);
  analogWrite(PWMB, speedB);
}
```

## Calibrating uneven motors

The Tamiya twin motor gearbox uses two separate small DC motors. Even from the same batch, they rarely produce identical output at the same PWM value — one motor turns slightly faster than the other, and the robot curves instead of going straight.

The quick fix: run them at slightly different PWM values. By empirical testing, the specific motors on this robot needed something like `forward(234, 255)` to track reasonably straight rather than `forward(255, 255)`. This is low-precision calibration — the "right" approach is a feedback loop with encoders, but for a chassis this simple, a manual offset gets you 90% of the way there without any additional hardware.

The simplified test loop:

```cpp
void loop() {
  forward(234, 255);
  delay(2000);
  backward(234, 255);
  delay(2000);
}
```

Go forward two seconds, reverse two seconds, repeat. Simple enough to verify direction and speed without complexity getting in the way.

## First run diagnostics

Two problems showed up immediately:

**Problem one: the robot spins instead of going straight at startup.** Root cause was a STBY pin issue — the TB6612FNG's standby pin wasn't being driven high correctly, so the driver was intermittently enabling and disabling. The STBY pin must be explicitly pulled HIGH in `setup()` before any motion commands. This is the single most common TB6612FNG gotcha and it looks exactly like bad wiring or bad code.

**Problem two: the rear caster is dragging.** The ball caster mounted at the rear of the chassis sits slightly too high — the caster ball doesn't quite reach the floor, leaving a cardboard bump as the actual rear contact point. The robot makes a dragging sound at speed and slows down noticeably. The fix is a cardboard shim under the caster mount to lower it until all three contact points (two drive wheels and caster) are level. Easy to adjust on a cardboard chassis — it's a zip tie and a stack of cardboard.

## What this test confirms

After fixing the caster height: the robot drives forward, reverses cleanly, and the TB6612FNG is responding correctly to both motors. That's the checkpoint before adding sensors. With no obstacle avoidance, the robot just follows its program — forward, backward, forward, backward — but the mechanical and electrical foundation is verified. The HC-SR04 sensors and the I²C LCD wiring come next.

## References and further reading

- [TB6612FNG datasheet (Toshiba)](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf) — the STBY pin behavior, direction truth table, and maximum motor current
- [TB6612FNG post on this site](/blog/arduino-nano-tb6612fng-motor-driver) — the full pin-by-pin wiring walkthrough for this motor driver
- [Cardboard chassis build](/blog/diy-arduino-robot-chassis-cardboard) — the chassis this test code is running on
- [Robot wiring and power redesign](/blog/clean-up-arduino-robot-wiring-power) — the wiring cleanup and battery configuration that preceded this test run
- [SparkFun TB6612FNG hookup guide](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide) — clear reference for anyone new to the chip
