---
title: 'ClusterBot Build — Installing the Battery Pack (The Hard Part)'
description: 'Getting a two-AA battery pack into the ClusterBot Arduino robot chassis. Covers why 3V is marginal for Tamiya motors, the physical installation challenge on a small chassis, and the case for 4×AA instead.'
pubDate: 'January 17 2012'
youtubeId: 'sveOtJ6XoVE'
heroImage: '../../assets/posts/clusterbot-arduino-battery-pack/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'batteries', 'tutorial', 'build']
---

*Episode 4 of the ClusterBot build series — an Arduino obstacle-avoidance robot. This step: getting the motor battery pack physically installed on the chassis. Took almost an hour. The video does not glamorize this.*

There's a particular frustration in small-robot building where the component you thought would take five minutes ends up taking an hour, and it's not even the interesting part. The battery pack for ClusterBot's motors — a two-AA holder picked up at Radio Shack — turned out to be one of those components. The video is honest about it. The description says "painful to watch, but I finally get it." That's accurate.

The difficulty isn't electrical. It's physical: fitting a battery holder onto a round, already-crowded acrylic platform where the gearbox brackets, Arduino mounting, and ball caster have already claimed most of the real estate.

## The power supply split

ClusterBot uses two separate power sources. The Arduino runs off USB power during development (and can later run off a 9V battery through the barrel jack). The motors — the Tamiya Twin Motor Gearbox — run off the separate battery pack.

This split is important. The Tamiya motors draw 300–500mA each under normal load and can spike higher under stall. If the motors and Arduino shared a supply, every time the motors hit a load spike they'd pull down the supply voltage, causing the Arduino to brownout, reset, or behave erratically. Separate supplies keep the logic clean.

The motor battery also doesn't go through the Arduino at all — it connects directly to the motor driver's VM (motor voltage) input, with only the GND tied to Arduino GND to maintain a common reference.

## Why two AAs is marginal

A two-AA pack delivers 3V nominal from fresh alkaline cells. The Tamiya motors are rated for 3V, so on paper this looks fine. In practice, alkaline cells under load sag below 3V quickly. By the time you've run the robot for ten minutes, each cell is down to 1.2–1.3V, and the pack is delivering 2.4–2.6V. At that voltage, the motors are noticeably slower and stall torque drops enough that the robot struggles on any surface that isn't perfectly smooth.

The better choice for this motor is a **four-AA pack** delivering 6V nominal (5.5V+ under load). That's within the motor's operating range, well within the TB6612FNG driver's input range (up to 13.5V), and gives you consistent performance as the batteries drain. The first few volts of alkaline droop happen quickly but then the voltage stays more stable.

The reason two AAs ended up in ClusterBot rather than four is probably the Radio Shack visit — they had a two-cell holder, it went in the shopping basket, and it wasn't until the robot was running that the marginal voltage became apparent. If you're building your own version of this robot, start with four AAs. You'll appreciate the extra headroom.

## The physical challenge

A round chassis doesn't have convenient flat edges or obvious rectangular battery bays. The acrylic plate has mounting holes, but they're positioned for the Arduino and the motor driver, not for a battery holder of whatever size you happen to buy. The two-AA holder from Radio Shack is a rectangular plastic box with wire leads and, on the better versions, a switch.

Routing it onto ClusterBot without obstructing the ball caster, the gearbox output shafts, the drive wheels, or the USB port access for the Arduino requires some spatial problem-solving. Zip ties, double-sided foam tape, and occasionally a small drill are all legitimate tools here. The foam tape approach — stick the battery holder to the underside of the chassis plate, between the caster and the gearbox — works if the holder is thin enough.

The video shows the process of trying different positions, finding clearance issues, and eventually landing on a solution. That process is part of the build, not a failure of planning. Small robot chassis are tight by nature.

## Securing it properly

Whatever mounting method you use, the battery pack needs to stay put when the robot turns hard or backs away from an obstacle. A battery holder that slides around will eventually work its way loose and break the motor circuit at the worst possible moment. Double-sided foam tape is surprisingly strong on acrylic; a strip of hook-and-loop fastener (Velcro) gives you easy access for battery changes. A single zip tie through a chassis hole is the low-tech fallback.

Also: make sure the battery pack switch — if it has one — is accessible from the outside of the chassis without disassembling anything. Having to unplug the Arduino to reach the motor battery power switch is the kind of annoyance that makes you eventually just wire directly and skip the switch entirely.

## ClusterBot build series

1. [Assemble the Pololu chassis](/blog/clusterbot-pololu-robot-chassis-assembly)
2. [Solder wires to the Tamiya motors](/blog/clusterbot-solder-tamiya-motor-wires)
3. [Solder headers onto the Pololu motor driver](/blog/clusterbot-solder-pololu-motor-driver-headers)
4. Install the battery pack **(this episode)**
5. [Finish the frame](/blog/clusterbot-finish-robot-frame)
6. [HC-SR04 obstacle avoidance live demo](/blog/clusterbot-hcsr04-obstacle-avoidance-demo)

## References and further reading

- [Powering Arduino projects | Arduino documentation](https://docs.arduino.cc/learn/electronics/power-pins) — covers the distinction between logic power and motor power
- [Battery basics for robotics | SparkFun](https://learn.sparkfun.com/tutorials/battery-technologies/all) — good comparison of alkaline, NiMH, and LiPo for robot applications
- [Why separate motor and logic power? | Arduino Forum](https://forum.arduino.cc/t/powering-arduino-and-motors-from-different-supplies/120438) — community discussion of the brownout issue that makes power splitting necessary
