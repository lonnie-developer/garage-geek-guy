---
title: 'ClusterBot Build — Assembling the Pololu Round Robot Chassis'
description: 'First steps of the ClusterBot Arduino obstacle-avoidance robot: assembling the $25 Pololu round robot chassis from Robotshop. Covers what comes in the kit, what to watch for, and how it fits into the overall build.'
pubDate: 'January 16 2012'
youtubeId: 'lJ6LrF8fOvo'
heroImage: '../../assets/posts/clusterbot-pololu-robot-chassis-assembly/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'chassis', 'beginner', 'tutorial']
---

*This is the first episode in the ClusterBot build series — an Arduino-powered obstacle-avoidance robot using a Pololu chassis, Tamiya motors, and an HC-SR04 ultrasonic sensor. The channel was still MeanPC.com when this was filmed in January 2012.*

Every robot starts with the chassis, and every chassis decision shapes everything that comes after. Motor placement determines wheel base. Mounting holes determine where the Arduino can sit. Battery position affects balance. The shape of the platform determines what sensors fit where and how the wiring routes. You can swap out a motor driver or upgrade a sensor later without much trouble, but reworking the chassis mid-build is the kind of thing that makes you want to start over from scratch.

The chassis for ClusterBot is the Pololu round robot chassis, the $25 version available from Robotshop. For a first Arduino robot in 2012 — or today — it's a solid choice.

## What comes in the kit

The Pololu round chassis is a circular acrylic platform with pre-drilled mounting holes. The kit includes the base plate, two motor mounting brackets that hold the Tamiya Twin Motor Gearbox, a ball caster for the third point of contact, wheels, and the associated hardware — screws, standoffs, and spacers. Everything needed to build a two-wheeled, differential-drive robot platform.

The diameter is roughly 150mm (about 6 inches), which gives you a compact footprint while leaving enough surface area to mount an Arduino Uno, a motor driver board, a breadboard for the sensor wiring, and a battery pack. Tight, but workable. Part of what makes the ClusterBot name apt — everything ends up clustered together.

## Assembly order

The Tamiya Twin Motor Gearbox goes in first. The gearbox sits in the motor mounting brackets, which bolt to the base plate on opposite sides. Get the gearbox positioned and secured before adding anything else, since the motor mounting hardware is the hardest to access once the rest of the build is in place.

The ball caster — a small ball bearing in a housing — provides the third contact point at the rear of the chassis (or front, depending on orientation). A two-wheeled robot without a caster tips onto the motors; the caster keeps it level and lets it rotate freely in any direction. The ball caster mounts through the pre-drilled hole in the rear of the base plate.

With motors and caster in, the chassis rolls. Everything else — Arduino, motor driver, sensor, batteries — mounts on top of or around the base plate.

## The Tamiya Twin Motor Gearbox 70097

The motor unit that ClusterBot uses is the Tamiya Twin Motor Gearbox 70097, a kit that's been in production since the 1990s and is still sold today. It comes as a kit: you assemble the gearbox yourself from plastic gear housing, two small DC motors, and a selection of gears that let you choose your gear ratio.

The 70097 offers two gear ratio options: 38.2:1 (faster, less torque) and 182.7:1 (slower, more torque). For an obstacle-avoidance robot running on a hardwood floor, the lower gear ratio — 38.2:1 — gives a reasonable speed while keeping current draw manageable. The higher ratio is better for heavy loads or climbing; on flat ground with a lightweight robot, it makes the robot frustratingly slow.

Rated voltage is 3V for each motor, with the two motors typically wired independently to a dual motor driver. Each motor draws around 300–500mA under normal load. That current requirement is why the motor power supply is separate from the Arduino's logic supply — more on that in the battery pack episode.

## What makes this chassis good for a first robot

The round shape means ClusterBot turns the same way regardless of which direction it's heading — no corners to catch on furniture legs or doorframes during obstacle avoidance. Differential drive (two independently driven wheels) gives it full maneuverability: drive both forward to go straight, drive one faster than the other to curve, reverse one while driving the other forward to spin in place.

The acrylic construction is light and easy to drill if you need extra mounting holes, and it doesn't conduct electricity, which matters when you've got bare-lead components sitting on the platform. The pre-drilled holes match standard Arduino mounting dimensions, so the Uno drops in without modification.

For about $25 in 2012, it was one of the more complete beginner chassis kits on the market. The Tamiya gearbox added another $10–15. Total chassis investment under $40.

## The build sequence

ClusterBot comes together over several short episodes, each focused on a single assembly step:

1. Chassis assembly — mounting the Tamiya gearbox to the Pololu base plate **(this episode)**
2. [Solder motor wires to the Tamiya gearbox](/blog/clusterbot-solder-tamiya-motor-wires)
3. [Solder headers onto the Pololu motor driver](/blog/clusterbot-solder-pololu-motor-driver-headers)
4. [Install the battery pack](/blog/clusterbot-arduino-battery-pack)
5. [Finish the frame and balance the chassis](/blog/clusterbot-finish-robot-frame)
6. [HC-SR04 obstacle avoidance live demo](/blog/clusterbot-hcsr04-obstacle-avoidance-demo)

## References and further reading

- [Pololu round robot chassis | Pololu](https://www.pololu.com/category/26/chassis) — current Pololu chassis lineup; the product has evolved but the approach is the same
- [Tamiya Twin Motor Gearbox 70097 | Pololu](https://www.pololu.com/product/114) — specs and assembly instructions
- [Differential drive robotics | Wikipedia](https://en.wikipedia.org/wiki/Differential_wheeled_robot) — the drive configuration ClusterBot uses
- [Robot chassis selection guide | Robotshop](https://www.robotshop.com/blogs/how-to-blog/chassis) — useful context for choosing between chassis types for different applications
