---
title: 'How to Use Servos with Arduino — Wiring + Code (HiTec HS-322HD, TowerPro MG995)'
description: 'How to wire and control hobby servos with Arduino — external power, common ground, lead color schemes for HiTec and TowerPro, Servo library code, and why jitter happens.'
pubDate: 'November 20 2013'
youtubeId: 'ybV8vitYAWU'
heroImage: '../../assets/posts/servo-with-arduino/thumbnail.jpg'
tags: ['arduino', 'servo', 'tutorial', 'motors', 'robotics']
---

There's a particular kind of frustration that comes from wiring up a servo to an Arduino, watching it twitch uncontrollably, and not knowing if the problem is the wiring, the code, the power supply, or the servo itself. The answer is almost always the power supply — but only if you know what to look for.

This post covers hobby servo basics from the ground up: what servos are and why they're worth using, how to wire them to an Arduino with a separate battery pack (and why that matters), the lead color differences between HiTec and TowerPro servos that catch people off guard, a walkthrough of the Arduino Servo library, and the jitter issue that shows up at the extreme ends of the travel range.

*This video is from 2013, when the channel was still running as MeanPC.com — same workbench, same hands, just a different name on the channel.*

## What a servo actually is

A hobby servo is a self-contained actuator: a DC motor, a gearbox, a potentiometer, and a small control board all packed into one housing. That control board reads a PWM signal on the signal wire and drives the motor until the potentiometer reads the position you asked for. The whole feedback loop is inside the servo — you don't need to write a PID controller, you don't need an H-bridge or motor driver, you just tell it where to go.

The tradeoff for that simplicity is range. Standard servos rotate 180 degrees. That's it. They were designed to steer model aircraft control surfaces and RC car wheels, where 180 degrees of travel is plenty. If you want a servo that spins continuously like a regular motor, you need either a purpose-built continuous rotation servo or a standard servo that's been modified — which involves removing the end-stops and replacing the feedback potentiometer with a fixed resistor pair. We've covered that modification in depth in the [TowerPro MG995 continuous rotation hack post](/blog/hack-towerpro-mg995-continuous-rotation).

For robotics, animatronics, pan-and-tilt camera mounts, throttle linkages, and anything that needs to hold a specific angular position, standard servos are hard to beat. The motor control circuitry is already paid for, the gearing is already tuned, and the units are cheap — often well under $10 for a capable hobby servo.

## Two servos, two lead color schemes

Most servos use the same three-wire interface: ground, power, and signal. The problem is that different manufacturers use different wire colors for these connections, and if you've only ever used one brand you'll be caught off guard the first time you pick up the other.

The **HiTec HS-322HD** follows the most common convention:

- **Yellow** — signal (control)
- **Red** — power (positive)
- **Black** — ground

The **TowerPro MG995** flips things around enough to trip you up:

- **Orange** — signal (control)
- **Red** (or reddish-orange) — power (positive)
- **Brown** — ground

Brown-for-ground is the TowerPro convention across essentially their whole lineup. Once you know it, it's easy enough to remember, but the first time you see a TowerPro servo and expect black for ground you're going to have a bad time. The quick rule: if there's a brown wire, brown is ground.

As far as capability goes, the HiTec HS-322HD is a lighter, quieter servo — about 42g, 3.0 kg·cm of torque at 4.8V, rated for 4.8–6V. The MG995 is a beefier beast at around 55g, claims 8.5–10 kg·cm depending on voltage, runs on 4.8–7.2V, and has metal gears that explain both the torque and the occasional grinding when something goes wrong. Both are fine for general hobby use; the HS-322HD is the tidier choice for lightweight builds and the MG995 is what you reach for when you need it to actually do work.

## Power: the part most tutorials skip

Here's where servos bite beginners: powering them from the Arduino's 5V pin.

On paper, the Arduino 5V pin can source up to 200mA (from USB) or 400–800mA (from a 7–20V barrel connector input through the onboard regulator). In practice, a servo under load can pull 500mA to over 1A in stall conditions. Trying to pull that through the Arduino's regulator — especially over USB — results in the classic Arduino brownout: the board resets, the servo twitches, everything acts weird.

The cleaner approach, especially for any project that might put real torque on the servo, is a separate power supply. Four AA alkaline batteries in series give you roughly 5.8–6V — right in the sweet spot for both the HS-322HD and the MG995. A 4-cell AA battery holder with a switch is a dollar part and solves the problem permanently.

The critical thing when using a separate supply: **the grounds have to be common**. Run a wire from the battery pack's negative terminal to one of the Arduino's GND pins. Without that shared ground reference, the Arduino has no reference point for the PWM signal it's sending on the signal wire and the servo doesn't know what to do with it. This is a straightforward rule that applies to anything you power externally while driving with an Arduino signal.

Wiring from there is simple:

1. Battery pack negative → Arduino GND
2. Battery pack positive → servo power (red) wire
3. Battery pack negative → servo ground wire (black for HiTec, brown for TowerPro)
4. Any Arduino digital pin → servo signal wire (yellow for HiTec, orange for TowerPro)

Notice step 4: **any digital pin works**. Servos use PWM, but the Arduino Servo library generates that PWM in software and can do it on any digital pin — you don't need to limit yourself to the hardware PWM pins (3, 5, 6, 9, 10, 11 on the Uno).

## The Servo library

The Arduino Servo library comes pre-installed; no downloads needed.

```cpp
#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);  // tell the library which pin the servo is on
}

void loop() {
  myServo.write(180);  // rotate to 180 degrees
  delay(2000);         // give it time to get there
  myServo.write(0);    // rotate to 0 degrees
  delay(2000);
}
```

The `attach()` call registers the pin. The `write()` call sets the target angle, 0–180. That's it for basic use — the library handles the PWM timing internally.

The `delay()` calls matter more than they look. When you call `myServo.write(180)`, the Arduino sends the new position command and moves on immediately — it does not wait for the servo to physically get there. If your next `write()` comes before the servo has finished moving, the servo will receive the new target mid-travel and head toward that instead. For a sweep demo that doesn't care about overshoot this is fine, but for anything that needs the servo to actually reach a position before the next action, size your delays for the servo's rated speed (the HS-322HD does 0.19 s/60° at 4.8V, so roughly half a second to cover the full 180°).

If you need finer timing control, `writeMicroseconds()` gives you access to the raw PWM pulse width: 1000µs is fully clockwise, 2000µs is fully counterclockwise, and 1500µs is center. Some servos respond better to microsecond values at the extremes of their range than to the degree-based `write()` mapping.

The library supports up to 12 servos on most boards (the Mega can handle 48), and each servo object operates independently — you just create multiple `Servo` instances and attach each to a different pin.

## The jitter problem

Run a servo to exactly 0 or 180 degrees and you'll often see it shudder at the endpoint. This is a calibration mismatch: the servo's internal mechanical stops are at positions slightly outside the range the Servo library maps to 0° and 180°. The servo is trying to get to a position its mechanics can't quite reach, so the control loop hunts back and forth trying to close the error.

The fix is straightforward — back off a few degrees from the endpoints:

```cpp
myServo.write(10);   // instead of 0
myServo.write(170);  // instead of 180
```

How much margin you need varies by servo. Some cheap units jitter at 5°, others at 15°. If jitter is a problem, creep inward from the endpoints until it stops. For most hobby applications the 10–170 range covers everything you actually need.

If a servo jitters throughout its range rather than just at the endpoints, the issue is usually power — either the voltage is too low, the current supply is marginal, or the ground connection is flaky.

## Continuous rotation servos: the same code, different result

If you run the sweep code with a continuous rotation servo — one that's been modified or purpose-built with the position potentiometer removed or replaced — you'll notice the servo just spins continuously regardless of the `write()` value. That's expected behavior.

Without a potentiometer, the servo's control board has no way to know its position. It receives a target angle from the signal wire, looks for the potentiometer to tell it where it actually is, can't find that feedback, and so keeps driving the motor trying to close a gap it can never close.

On a purpose-built continuous rotation servo, the `write()` value controls speed and direction instead of angle: 90° is stopped, values below 90° rotate one direction, values above 90° rotate the other. The exact mapping depends on the servo — and on whether the center point has been calibrated. On a DIY-modified servo where the pot was just removed and shorted out, the behavior is less predictable and mostly "just spinning."

## Where servos fit and where they don't

For anything that needs a held angular position — a pan-tilt head, a steering linkage, a door latch, a throttle lever — a standard servo is still one of the most cost-effective actuators available. Sub-$10 price, no external driver, works directly from a microcontroller signal. The 180° limit is rarely the constraint it sounds like in practice.

For continuous rotation at variable speeds, a dedicated continuous rotation servo is fine for lightweight applications, but a DC motor with an H-bridge or L298N driver gives you more control and doesn't carry the overhead of servo mechanics you're not using. For precision positioning beyond 180°, a stepper motor is the right tool.

## References

- [Arduino Servo library documentation](https://docs.arduino.cc/libraries/servo/) — attach, write, writeMicroseconds, and the full API reference
- [HiTec HS-322HD product page](https://www.hitecrcd.com/products/servos/sport-servos/analog-sport-servos/hs-322hd/product) — specs, dimensions, torque curves
- [TowerPro MG995 datasheet](http://www.towerpro.com.tw/product/mg995-robot-servo-180-rotation/) — torque, voltage, dimensions
- [Parallax Standard Servo documentation](https://learn.parallax.com/tutorials/robot/shield-bot/robotics-board-education-shield-arduino/chapter-4-boe-bot-robot-0) — the Boe-Bot connection if you want historical context on hobby servos in robotics
- [Adafruit guide: All About Servos](https://learn.adafruit.com/adafruit-motor-selection-guide/servo-motors) — good overview of servo types and selection criteria
- [RC Servo PWM signal explained](https://en.wikipedia.org/wiki/Servo_control) — Wikipedia on the 1–2ms pulse width standard
