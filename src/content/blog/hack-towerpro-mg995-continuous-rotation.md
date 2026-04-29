---
title: 'How to Hack a TowerPro MG995 Servo for 360° Continuous Rotation'
description: 'Turn a sub-$10 metal-gear hobby servo into a high-torque gear motor that runs straight off an Arduino — no motor driver required. Full walkthrough of the physical mod, the resistor-divider trick, and the calibration step nobody warns you about.'
pubDate: 'August 19 2012'
youtubeId: 'cnOKG0fvZ4w'
heroImage: '../../assets/posts/mg995/thumbnail.jpg'
tags: ['arduino', 'servo', 'robotics', 'mg995', 'hardware-hacking', 'tutorial']
---

There's a particular flavor of cheapness that defines a lot of hobby robotics: you go looking for a continuous-rotation gear motor that will (a) put out enough torque to push a small robot around, (b) talk to an Arduino without a separate motor driver, and (c) cost less than a movie ticket. The honest answer is that no such part exists from a major vendor. You can have any two of those three.

Or you can spend ten dollars on a [TowerPro MG995](https://servodatabase.com/servo/towerpro/mg995) and an afternoon at the bench, and end up with something that does all three.

The MG995 is a metal-gear hobby servo that shows up in every "cheap parts off eBay" robotics build. Stock, it sweeps a 180° arc and reports its position to its own internal logic board through a feedback potentiometer. After this hack, it stops caring about position entirely and just spins — clockwise or counterclockwise, at a speed you control, all the way to either limit of the standard Arduino `Servo` library. It's the closest thing to a free lunch that hobby robotics offers.

This post walks through exactly that mod: the two changes you make inside the case, the resistor trick that fools the logic board, the gotcha that costs you the position calibration, and a couple of robot-build notes at the end. The video at the top is the full demo if you'd rather watch it; the writeup below is the version you can keep open on the bench.

> *Quick historical note: this build is from 2012, when the channel was still meanPC.com. Same Lonnie, same garage, same workbench — just a different name on the masthead.*

## The MG995 itself

Before getting into the mod, it's worth knowing what you're starting with. The MG995 is a clone-class metal-gear analog servo that's been a mainstay of low-budget robotics for over a decade. Per the [TowerPro datasheet](https://www.electronicoscaldas.com/datasheet/MG995_Tower-Pro.pdf), the basic specs are:

- **Torque:** 10 kg·cm at 4.8 V, ~12 kg·cm at 6 V (about 9 in·lb at 6V — strong for the price)
- **Speed:** 0.19 s/60° at 4.8 V, 0.15 s/60° at 6 V
- **Weight:** 55 g
- **Gear train:** Metal — that's the "MG" — with two ball bearings on the output shaft
- **Connector:** Standard 3-pin JR (signal, V+, GND)
- **Stall current:** Up to ~2 A under load, which is the part most builders forget about

That last point is the recurring gotcha with this servo. It will absolutely [draw 2 A from a USB-powered Arduino Uno](https://forums.parallax.com/discussion/77145/faster-servo) and reset the board if you try to run it without a separate power supply. Plan for an external pack from the start.

The MG995's reputation in hobby circles is "cheap, strong, and inconsistent." [RC Model Reviews](https://www.rcmodelreviews.com/mg995review.shtml) and others have noted that two MG995s out of the same bag will often have different center positions, slightly different speeds at full PWM, and different idle currents. None of that matters for our purposes — for a robot drivetrain, you're going to calibrate each one anyway. But it's why this specific servo is a teaching example, not a precision tool.

## Why hack a servo at all?

A servo and a gear motor are the same physical thing — a DC motor driving a reduction gearbox — with one extra ingredient: a feedback loop. The feedback loop is what turns motion into position. Inside the case, a potentiometer rides on the output shaft, and a small logic board compares the pot's reading to whatever the incoming PWM signal asks for, then drives the motor in whichever direction closes the gap. When the two readings match, the motor stops.

If you remove the feedback loop, what's left is exactly what you wanted in the first place: a small, geared, bidirectional motor with a built-in PWM controller, that listens on three wires.

This idea isn't new. The DIY continuous-rotation servo hack has been documented in [Parallax forums going back at least to the mid-2000s](https://forums.parallax.com/discussion/128121/how-to-hack-servos), and Parallax themselves were the ones who really commercialized it. Their [Boe-Bot educational robot](https://learn.parallax.com/kickstarts/parallax-continuous-rotation-servo/) — which has been used to introduce kids to robotics since 1997 and is the platform behind the [Boy Scouts Robotics merit badge](https://www.parallax.com/product/boe-bot-robot-kit-usb/) — runs on two Parallax-branded continuous-rotation servos. Those are essentially this hack, factory-applied, for about $15 each.

What you're about to do is the eBay-cheap version of what Parallax has been selling for thirty years. The technique is the same; the difference is you're buying a $10 metal-gear servo instead of a $15 plastic-gear one, and you're doing the modification yourself. For most robot builds, that's a fine trade.

## The two-part mod

The hack has two halves, and both have to happen for it to work.

**The physical half:** the servo case has a mechanical stop that physically prevents the output gear from rotating past 180°. This has to come out, or the gears will jam against it the first time you ask for full rotation.

**The electrical half:** the logic board has to think the output shaft is permanently sitting at the center position, no matter where the (now disconnected) shaft actually is. We do that by replacing the three potentiometer wires with a fixed [voltage divider made from two 2.2 kΩ resistors](https://forums.parallax.com/discussion/88950/continuous-rotation-servo) — same value, same center-tap, but the voltage at the center tap never changes. The logic board sees a constant "I'm at 90°" signal and happily drives the motor wherever the incoming PWM tells it to go.

Either change without the other gets you a broken servo. Together you get continuous rotation.

## What you'll need

- TowerPro MG995 servo (sub-$10 on eBay, or about $4–6 in bulk from AliExpress)
- Two **2.2 kΩ resistors** (1/4 W is fine; tolerance doesn't matter much because we're going to calibrate anyway)
- Phillips screwdriver — small enough for the four captive case screws
- A couple of flathead screwdrivers in different sizes
- Diagonal side cutters (for prying the rotation pin out)
- Needle-nose pliers
- Soldering iron + solder (60/40 leaded if you can still get it; lead-free is fine)
- Electrical tape

Optional but recommended: a phone or camera. The first thing I do when opening any servo is take a photo of the gear stack before disturbing anything. There's an order to those gears, and on the MG995 there's also a small ball-bearing pack you can lose in the carpet if you're not paying attention.

## Cracking the case

Four captive Phillips screws on the back of the servo. Loosen them, but don't try to pull them out — they're held in place by the back cover and stay with the case when you separate the halves.

Lift the back cover off and you'll see the logic board, with the three thin wires running from it to the potentiometer. Set the back cover aside.

Now turn the servo over and pop the top cover off. **This is where the photograph helps.** On the MG995 specifically, watch for a tiny pack of loose ball bearings sitting on the gear-side housing — it's part of the thrust bearing arrangement that gives this servo its long life under load. If those scatter, you're going to have a bad afternoon. Tip the case the right way, lift the top cover straight up, and put both somewhere flat.

You should now be looking at the gear stack. The output gear is the big one with the splined shaft sticking out the top.

## Removing the rotation stop

Most plastic-gear servos have a small molded bump on the output gear that hits a corresponding bump on the case at each end of travel. On those, you carve the bump off with a hobby knife and you're done with the mechanical half.

The MG995 is metal-geared, so it does it differently. There's a small **steel pin** pressed into the output gear that protrudes downward and hits a stop on the lower housing. You need to pry it out.

Grip the pin with your diagonal cutters — not as a cutter, but as pliers. The cutting jaws give you a good biting surface on the pin without crushing the gear. Walk the pin out with a gentle rocking motion. It will resist for the first millimeter or so, then give up and slide free. Don't lose it.

The output gear also has a rectangular **plastic notch** on its underside that engages a tab on the potentiometer shaft — that's how the pot knows where the gear is. Use a small flathead to widen and hollow out that notch so the pot's tab no longer engages it. You're not removing the pot here, just disengaging it from the output shaft mechanically. (If you've ever wondered why this servo's mod is "harder" than a basic plastic-gear one, this notch is half the answer. The pin is the other half.)

Test fit: drop the output gear back into place and turn it by hand. It should now rotate freely through a full circle with no clunk at either end. If it still binds, the pin wasn't fully out, or the notch isn't deep enough.

## The resistor divider

Now flip back to the logic board. The potentiometer is wired to the board with three thin leads — typically labeled S, V, G or similar, but on the MG995 they're just three solder pads on the board with three wires going to the pot. The middle one is the wiper; the outer two are the high and low ends of the pot's resistive track.

Desolder all three leads from the board. Bend the pot's pins down out of the way (or remove the pot entirely if you want a cleaner build — most people leave it floating since it adds no weight).

Now build the **resistor "trident"**: two 2.2 kΩ resistors soldered end-to-end, with their joined center forming the new wiper signal. The two free ends of the resistors are the high and low rails. You should end up with three terminals — outer, center, outer — that physically resemble the pot's three pins.

Why 2.2 kΩ? Because the original pot is typically 5 kΩ end-to-end, with the wiper sitting at the middle (~2.5 kΩ from either side) when the servo is at center position. Two 2.2 kΩ resistors give you the same fixed midpoint. The exact value isn't critical — anywhere from 1 kΩ to 4.7 kΩ will work — as long as **both resistors are the same value**. They define a fixed 50/50 divider, which is what tells the board "you're at center."

Solder the three leads of the trident onto the same three pads where the pot wires used to go: outer leg → outer pad, center → wiper pad, other outer leg → other outer pad. Polarity of the two outer legs doesn't matter (it's a symmetric divider). Wrap the whole thing in electrical tape so the bare leads can't short against the case or each other when you reassemble. *Insulation is the step you'll regret skipping.*

## Reassembly

Drop the gear stack back into the lower housing. (If you lost track of the gear order, this is when you start regretting not taking that photo.) Make sure the ball-bearing pack is still seated. Replace the top cover, then the bottom cover with the logic board, and run the four captive screws back down — finger-tight is fine, you'll over-stress the case if you torque them down.

Spin the output shaft by hand. It should turn freely in either direction with no end stops, and you should not feel any drag from the (now floating) pot.

## The Arduino test — and the calibration nobody tells you about

Wire up the servo:

- **Orange (signal)** → Arduino digital pin 9
- **Red (V+)** → external 5–6 V power supply, NOT the Arduino's 5V rail (the MG995 will brown out the Uno under load)
- **Brown (GND)** → both the external supply ground *and* the Arduino ground (common ground is mandatory)

Upload the standard `Sweep` example from the [Arduino Servo library](https://docs.arduino.cc/libraries/servo/) — `File → Examples → Servo → Sweep`. Or simpler, write a one-line `myServo.write(90);` and watch what happens.

Here's the part nobody warns you about:

**90 is not the stop value for your servo.**

In the textbook version of this mod, `write(90)` outputs the center pulse width (1.5 ms), the divider tells the board "you're at center," the error signal is zero, and the motor stops. In practice, the resistors you used aren't perfectly matched (5% tolerance is normal), the logic board has its own offset, and the result is that the actual stop position lands somewhere between 80 and 110.

For the servo I modified in the video, the true stop value was **105**. Yours will be different.

You find it by trial and error. Set `write(90)` and watch — the servo will probably drift slowly. Step the value up by 1 or 2 at a time until the drift stops completely. That's your calibration constant for this particular servo. Write it on a piece of tape on the case. You'll need it every time you write code for that motor.

Once calibrated, the rest is the standard servo idiom flipped on its head. Below the stop value drives one direction; above it drives the other. The further you are from the stop value, the faster the motor turns, up to the library's 0–180 range. So:

- `write(105)` — stop
- `write(180)` — full speed counterclockwise
- `write(0)` — full speed clockwise
- `write(115)` — slow counterclockwise
- `write(95)` — slow clockwise

It's worth saying: those direction labels depend on which way you mounted the servo and which way the output shaft faces. CCW on a left-side wheel is forward; CCW on a right-side wheel is reverse. Test before you assume.

## Robot drive notes

If you're using two of these for a differential-drive robot — which is the entire point of doing this hack at scale — there's one more calibration step. After you find each servo's stop value, you also need to find each one's **matched full-speed value**.

Two MG995s rarely match exactly. One might run flat-out at 180; the other might be visibly faster and need to be throttled to 177 to keep pace. Without matching, your robot drives in lazy curves instead of straight lines. The fix is software: define `LEFT_FORWARD = 180` and `RIGHT_FORWARD = 177` (or whatever your specific pair calls for) as constants and use those everywhere instead of raw 180.

You can either tune by eye on a smooth floor, or — if you want to be fancy about it — put the robot on a chair, run both wheels at 180, and time how long it takes each wheel to spin a marked rotation. The slower wheel becomes the reference; throttle the faster one until they match.

## Where this fits today (and where it doesn't)

The MG995 hack is a **teaching project**. It's the cheapest possible way to get from "I have an Arduino" to "I have a moving robot" without buying an L298N motor driver, a separate gear motor, and figuring out PWM duty cycles. For that purpose — and for a kid's first robot, a Halloween prop, a slow-moving art piece, anything where precision doesn't matter — it's perfect.

For anything that needs *positional* control or accurate speed regulation, this hack is the wrong tool, because you've literally cut the feedback loop. Go back to using the servo as a servo, or step up to a [TB6612FNG](https://www.adafruit.com/product/2448) or [L298N](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) driving a real gear motor with an encoder.

A few alternatives worth knowing about, in rough order of cost:

- **Pre-modded continuous rotation servos** like the [FS90R](https://www.adafruit.com/product/2442) ($6) or [Parallax 900-00008](https://www.parallax.com/product/parallax-continuous-rotation-servo/) ($15) — same idea, no soldering, but plastic gears and lower torque
- **Brushed gear motors** with an external H-bridge — more wiring, but you get real speed control and encoders
- **Brushless gimbal motors** with a controller board — overkill for most robotics, but wonderful when you need it

What none of those give you is the satisfaction of cracking open a part and turning it into a different part with two resistors and a flathead screwdriver. That's the real reason to do this hack at least once.

## References and further reading

- [TowerPro MG995 datasheet (PDF)](https://www.electronicoscaldas.com/datasheet/MG995_Tower-Pro.pdf)
- [ServoDatabase: MG995 specs and reviews](https://servodatabase.com/servo/towerpro/mg995)
- [Parallax forum: How to hack servos](https://forums.parallax.com/discussion/128121/how-to-hack-servos) — the canonical community thread
- [Instructables: Servo 360 Rotation Mod (Parallax)](https://www.instructables.com/Servo-360-rotation-mod-Parallax/) — photo-heavy walkthrough on a different servo
- [Parallax Continuous Rotation Servo](https://learn.parallax.com/kickstarts/parallax-continuous-rotation-servo/) — the educational background and Boe-Bot context
- [Arduino Servo library reference](https://docs.arduino.cc/libraries/servo/)

If you build this and run into something that didn't match the writeup, mention it in the comments — that's how this kind of recipe gets better.
