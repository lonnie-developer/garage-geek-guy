---
title: 'The $15 Amazon Arduino Robot Chassis — Assembly Walkthrough'
description: 'A two-wheel-drive acrylic robot chassis from Amazon costs $15 and includes motors, wheels, a caster, encoder discs, and hardware. Add ~$15 in electronics and you have a complete robot platform.'
pubDate: 'August 27 2021'
youtubeId: 'KYGK29j89dw'
heroImage: '../../assets/posts/arduino-robot-chassis-15-dollar-amazon/thumbnail.jpg'
tags: ['arduino', 'robot', 'chassis', 'diy', 'tutorial']
---

The entry price for Arduino robotics has dropped to the point where it's almost a rounding error. This particular 2WD chassis kit shows up on Amazon for around $15 with Prime shipping, includes everything you need to put together a rolling platform, and comes together in about twenty minutes. I liked it so much the first time I built one that I ordered two more and went ahead and documented the assembly process.

Here's what's in the box, how it goes together, and the two things worth knowing before you start.

## What you get

The kit ships as a flat acrylic base wrapped in a paper peel-off protective film (leave it on until you're ready to use the chassis — it prevents scratching during assembly), plus a bag containing:

- 2 × TT DC gear motors
- 2 × rubber wheels and tires that press-fit onto the motor shafts
- 2 × encoder discs (speed sensors) for each motor
- 2 × motor mounts and associated hardware
- 4 × standoffs and hardware for the caster wheel
- 1 × ball caster wheel
- 1 × battery compartment (4 × AA)
- 1 × power switch
- Pre-stripped motor wires (4 total, red and black for each motor)
- A bag of M3 screws, nuts, and standoffs
- Instructions

One more thing: a small handwritten card from the manufacturer with a rough translation along the lines of "missed meetings can be rescheduled, missed sunsets will return, but missed friends can only be missed." Grammatically approximate, but genuinely touching — someone put that in there intentionally.

There's also a clip-on phone holder included. I have no idea what to do with it either, but there it is.

## What you'll need to add

The chassis itself has no electronics — it's the mechanical platform only. To make it actually do something, budget for roughly another $15 in components:

- An Arduino Uno (or clone) — ~$5–10
- A motor driver module (L298N dual H-bridge is the standard choice) — ~$3–5
- Jumper wires, power wiring, and whatever sensors you want to add

For a basic obstacle-avoiding robot, an HC-SR04 ultrasonic sensor (~$2) rounds out the parts list. The chassis has plenty of mounting space for all of this.

## Assembly walkthrough

**Motors first.** Each motor mounts to the underside of the acrylic base using a plastic motor mount bracket and two long screws that pass through the mount, through the motor, and into a nut on the other side. The contacts face outward.

**Encoder discs go on before you tighten the motor screws** — this is the thing to know ahead of time. The encoder disc fits onto the back shaft of the motor (the side facing inward, opposite from where the wheel goes). If you tighten the screws down first, you lose clearance to slide the disc on. Loose-mount the motor, slip the encoder disc on, then snug everything up.

**The bottom nut is awkward.** When securing the lower motor mount screw, you're working in a tight space between the acrylic base and the motor. The trick is to angle the nut in sideways and nudge it into position with needle-nose pliers before you start threading. It's not hard once you know to expect it — just takes a minute of maneuvering.

**The caster wheel.** Four standoffs mount through the rear of the chassis base, the caster assembly attaches to those, and you tighten everything down. The standoffs bring the caster to the same rolling height as the main wheels so the robot sits level.

**Motor wires need soldering.** The kit includes pre-stripped wires, but they're not pre-soldered to the motor terminals. You'll solder the red and black leads onto the motor contacts and route them up to your motor driver on the top deck. If you're doing the electronics in a separate session (as I did here), just leave them dangling for now.

**Battery compartment gotcha.** The battery holder as packaged mounts to the underside of the bottom acrylic plate — which means it rides with the opening facing down, making it annoying to change batteries during a build session. I recommend either mounting it on the top deck or rigging up a different power solution. This was enough of an annoyance that I changed the approach on my second and third builds before I even started.

## Room on top

Once assembled, the top surface of the chassis has a generous amount of open real estate. I'm planning to run an Arduino Uno and an L298N motor driver up there on standoffs, along with a couple of HC-SR04 sensors mounted at the front. There's also a bit of bottom clearance for additional components if you need it.

The encoder discs I mentioned — once you add an encoder sensor module, you can read motor RPM and implement speed control, which makes for much better straight-line driving than relying on identical motor outputs alone.

## Is it worth $15?

Yes, easily. You get a real robot chassis with motors, wheels, hardware, instructions, and a thoughtful little card from the manufacturer. Even accounting for the battery compartment frustration and the fiddly bottom motor nut, it's a solid afternoon build that ends with an actual rolling platform ready for electronics. For a first robot project, it's a better foundation than most.

I bought three.

## References and further reading

- [DIYables 2WD kit with L298N motor driver](https://diyables.io/products/2wd-rc-robot-car-kit-with-l298n-motor-driver-and-sensors)
- [Columbia University 2WD motor robot assembly instructions (PDF)](https://www.cs.columbia.edu/~sedwards/presentations/robot-car-instructions.pdf)
- [s4scoding: Arduino UNO Smart Robot Car Kit instructions](https://s4scoding.com/arduino-uno-smart-robot-car-kit-instructions/)
- [L298N motor driver guide (this blog)](/blog/l298n-motor-driver-arduino-pwm)
- [HC-SR04 ultrasonic distance sensor guide (this blog)](/blog/measure-distance-arduino-hcsr04)
