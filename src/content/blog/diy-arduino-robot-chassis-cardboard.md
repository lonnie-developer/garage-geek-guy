---
title: 'Cheap DIY Arduino Robot Chassis — Cardboard Box, Tamiya Gearbox, and Zip Ties'
description: 'A robot chassis for under $10 in new parts: a cardboard box for the frame, a Tamiya twin motor gearbox for drive, and zip ties for everything else. Here is the build, the design logic, and why cheap and fast beats precise and slow when you are still figuring out what you want.'
pubDate: 'October 05 2012'
youtubeId: 'hJ772uChdsg'
heroImage: '../../assets/posts/diy-arduino-robot-chassis-cardboard/thumbnail.jpg'
tags: ['arduino', 'robot', 'chassis', 'tamiya', 'beginner', 'tutorial']
---

There's a particular kind of project paralysis that comes from wanting to build "the right robot" before you've figured out what right means. You sketch chassis ideas, compare motor options, price aluminum extrusion — and nothing gets built.

The alternative is to grab the nearest box and start cutting.

This chassis uses a cardboard box as the frame — specifically, the box a TI MSP430 Launchpad ships in, which turns out to be surprisingly rigid. A Tamiya twin motor gearbox provides the drive train. Everything attaches with zip ties. Total new-parts cost: under $10, maybe well under depending on what you have around. Build time: an afternoon.

It won't be the last chassis. It'll be the first one, which is more valuable.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## Why cardboard works

Cardboard gets dismissed as a prototyping material because it feels impermanent. But what you actually need from a robot chassis at this stage isn't permanence — it's rigidity, punchability, and forgiveness. Cardboard has all three. You can cut it with a knife, poke holes with a screwdriver, and run zip ties through improvised mounting points without needing a drill press or a 3D printer.

The Launchpad box specifically has a useful quality: it's a small, sturdy double-walled shipping box, not the flimsy single-layer kind. It holds its shape under the weight of a breadboard, a battery pack, and a handful of sensors without deforming. It also happens to be roughly the right size for a two-wheeled differential drive robot — long enough to fit the Tamiya gearbox at the front with room for electronics toward the rear.

## Parts

- **Tamiya twin-motor gearbox kit (Item #70168)** — around $7–8 from hobby shops or Amazon; comes with two small DC motors and a simple plastic gearbox housing. You'll need to solder wires to the motor terminals — four wires total, two per motor. This is about a 10-minute job with basic soldering skill.
- **Wheels** — not included with the gearbox; sold separately, usually $3–5 for a set compatible with the Tamiya axle size. Tamiya's "Track and Wheel Set" (Item #70100) is the common pairing.
- **Ball caster** — a small ball-bearing caster wheel for the rear; these come in robot kits and cost about $3–4 standalone. Provides the third contact point so the chassis sits level.
- **Zip ties** — buy a bag, use many
- **Cardboard box** — the sturdier the better; shipping boxes beat cereal boxes by a lot

## The build

**Step one: figure out orientation before cutting anything.** The motor gearbox goes at the front, where the wheels will be. Plan for HC-SR04 sensors at the very front corners, an LCD display somewhere on the top surface, and electronics (breadboard, battery) in the interior. Having this mental model before cutting means the holes end up in the right places.

**Step two: mark and cut wheel clearance holes.** The wheels need to extend below the bottom of the box. Mark their positions on the sides with a knife tip, then cut the clearance holes with a few passes. Precision isn't important here — the holes just need to be big enough for the wheels to spin freely. Go fast and fix it if needed.

**Step three: mount the gearbox with zip ties.** Poke holes through the cardboard on either side of the gearbox mounting points with a screwdriver. Run zip ties through and around the gearbox frame, pull snug with a needle-nose pliers. Add a second set of zip ties around the full perimeter of the motor mount for lateral stability. Trim the tails.

**Step four: route the motor wires.** Poke a small hole through the floor of the chassis near the gearbox and feed the motor wires through into the interior. This keeps the bottom clean and reduces the chance of wires snagging when the robot moves.

**Step five: mount the ball caster.** The caster goes at the rear, centered. Punch holes and zip tie it the same way as the gearbox. Before you tighten, check that the chassis sits level with the caster installed — if the caster arm is too long or too short for the wheel diameter you chose, you may need a cardboard shim underneath to level it out.

## The zip tie gospel

Zip ties are the right fastener for this. Not because they're permanent — they aren't — but because they're adjustable, they grip uneven surfaces, they don't require hardware, and they can be replaced in ten seconds when something shifts. For a prototype robot that's going to be rebuilt several times as you figure out what works, that's exactly what you want.

A few things learned through practice: pull them snug with needle-nose pliers rather than fingers — you get twice the tension with half the effort. Don't over-tighten on cardboard or you'll pull through. And run two zip ties wherever vibration from the motors might work something loose over time.

## What this chassis is for

This build is the foundation for a multi-part robot project: the Tamiya gearbox driven by a TB6612FNG motor driver, an MSP430 or Arduino as the brain, four HC-SR04 ultrasonic sensors for obstacle avoidance, and an I²C LCD for displaying sensor data. The cardboard chassis is explicitly a first iteration — the goal is to get something rolling quickly so the electronics and code work can begin without waiting on a "real" chassis.

Once you've driven a robot around and figured out what works and what doesn't, you'll have a much better spec for version two. Maybe that version gets cut from acrylic or printed. But it'll be designed around real experience rather than imagined requirements.

## References and further reading

- [Tamiya twin motor gearbox (Item #70168)](https://www.tamiyausa.com/shop/educational-construction/twin-motor-gearbox-kit/) — the gearbox used in this build; includes assembly instructions and motor specifications
- [Tamiya Track and Wheel Set (Item #70100)](https://www.tamiyausa.com/shop/educational-construction/track-and-wheel-set/) — the compatible wheel set for the Tamiya axle
- [Tamiya universal plate set](https://www.tamiyausa.com/shop/educational-construction/universal-plate-set/) — for builders who want a more rigid base before moving to full custom chassis
- [TB6612FNG motor driver (SparkFun)](https://www.sparkfun.com/products/14451) — the motor driver wired to this chassis in subsequent posts; handles both motors with PWM speed control and direction
