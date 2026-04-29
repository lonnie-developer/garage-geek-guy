---
title: 'ClusterBot Build — Soldering Wires to the Tamiya Twin Motor Gearbox'
description: 'Soldering hookup wires to the motors of the Tamiya 70097 Twin Motor Gearbox for the ClusterBot Arduino robot. Covers motor terminal access, wire gauge choice, polarity conventions, and the gotcha that reverses your robot.'
pubDate: 'January 16 2012'
youtubeId: '58qj3-4G6A4'
heroImage: '../../assets/posts/clusterbot-solder-tamiya-motor-wires/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'soldering', 'motors', 'tutorial']
---

*Episode 2 of the ClusterBot build series — an Arduino obstacle-avoidance robot. This step: getting wires onto the Tamiya gearbox motors so they can connect to the Pololu motor driver.*

There's a reason robotics tutorials spend a paragraph on motor wire polarity even when it seems obvious: the consequences of getting it wrong are exactly backwards from what you'd expect. If you wire both motors with reversed polarity, the robot drives in reverse when you command it forward — annoying, but trivially fixed by swapping all four wires. If you reverse only *one* motor, the robot spins in place when you command it forward, which is harder to diagnose if you don't immediately suspect polarity.

Two minutes of video, two minutes of work, one soldering session. But it sets up every motor control decision that follows.

## The Tamiya 70097 motor terminals

The Tamiya Twin Motor Gearbox 70097 houses two small DC motors inside a single plastic gearbox. Each motor has two terminals — small metal tabs that stick out from the motor housing after gearbox assembly. The terminals are close together and relatively small, which makes them the first real soldering challenge in the build.

The trick is to tin the terminals before trying to attach wires. Apply a small amount of solder directly to each terminal tab and let it flow and solidify. This creates a pre-wetted surface that accepts wire solder quickly and with less heat exposure to the motor — DC motors don't love prolonged heat at their terminals, and the small size of these particular terminals means your iron is close to the motor body. Get in and out fast.

## Wire choice

Solid-core hookup wire works for prototyping but will eventually fatigue and break at the motor connection if the robot vibrates a lot. Stranded wire — even 22–24 AWG stranded hookup wire — handles vibration better and is worth reaching for here. The current draw (300–500mA per motor under normal load) is well within 22 AWG's capacity.

Length matters: leave enough wire to reach the motor driver with some slack. The motor driver board mounts on the chassis platform, and the wires need to reach it without pulling taut when the gearbox shifts slightly during assembly. Six to eight inches per lead is usually sufficient for a palm-sized robot; add a few inches if you're unsure.

## Polarity conventions

DC motors run in one direction with positive applied to one terminal, and reverse with polarity swapped. There's no universal color convention for which terminal is "positive" — the motor doesn't care which way current flows, it just runs in the direction determined by the current direction.

The practical approach: pick a convention and document it before you start. Red wire to the right terminal tab (or whichever you designate as the reference), black wire to the left. Do both motors identically, with both motors oriented the same way relative to the chassis (both facing forward). When you program the motor driver, you'll know that "positive current to the red lead = forward rotation." If the robot ends up going the wrong direction, you swap both red and black on both motors simultaneously — not just one motor.

The reason to swap both rather than invert in software: if you invert one motor's software direction to fix a symptom, you've hidden the wiring inconsistency rather than correcting it. The next time you read the code, the "reverse" command to motor A will look like a bug. Fix it in hardware; keep the software clean.

## Strain relief

The motor terminals are the most mechanically stressed solder joints in the build, because the wires leading away from them get pulled and bent every time the gearbox moves. After soldering, secure the wires against the gearbox body with a small zip tie or a dab of hot glue a centimeter back from the joint. The strain relief doesn't need to be pretty — it just needs to keep the solder joint from working loose over the course of a few hundred obstacle avoidance cycles.

## What connects to the other end

These motor wires connect to the Pololu dual DC motor driver — the topic of the next episode. The driver board sits between the Arduino and the motors, translating Arduino logic signals into the current levels the motors need. You can't run a DC motor directly from an Arduino I/O pin; the motor's current demand (300–500mA) would immediately exceed the pin's 40mA limit. The motor driver handles the heavy lifting.

## ClusterBot build series

1. [Assemble the Pololu chassis](/blog/clusterbot-pololu-robot-chassis-assembly)
2. Solder wires to the Tamiya motors **(this episode)**
3. [Solder headers onto the Pololu motor driver](/blog/clusterbot-solder-pololu-motor-driver-headers)
4. [Install the battery pack](/blog/clusterbot-arduino-battery-pack)
5. [Finish the frame](/blog/clusterbot-finish-robot-frame)
6. [HC-SR04 obstacle avoidance live demo](/blog/clusterbot-hcsr04-obstacle-avoidance-demo)

## References and further reading

- [Tamiya 70097 Twin Motor Gearbox instructions | Tamiya](https://www.tamiya.com/english/products/70097twin_motor/index.htm) — official assembly instructions and gear ratio details
- [DC motor basics | SparkFun](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all) — good explainer of how brushed DC motors work and what the spec numbers mean
- [Wire gauge current capacity table | Blue Sea Systems](https://www.bluesea.com/resources/1437) — reference for matching wire gauge to current requirements
