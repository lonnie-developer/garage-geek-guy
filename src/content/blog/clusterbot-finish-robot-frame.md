---
title: 'ClusterBot Build — Finishing the Robot Frame'
description: 'Final physical assembly of ClusterBot, an Arduino obstacle-avoidance robot on a Pololu round chassis. Covers Arduino mounting, breadboard layout, the balance problem that named the robot, and the wiring that ties it all together.'
pubDate: 'January 17 2012'
youtubeId: 'eC330Rq3zEw'
heroImage: '../../assets/posts/clusterbot-finish-robot-frame/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'assembly', 'tutorial', 'build']
---

*Episode 5 of the ClusterBot build series — an Arduino obstacle-avoidance robot. This step: finishing the mechanical and electrical assembly so the robot is ready for software.*

ClusterBot got its name from necessity, not aesthetics. The Pololu round chassis is about 150mm in diameter — roughly the footprint of a large coffee mug. On that circular platform, you need to fit an Arduino Uno (53mm × 68mm), a half-size breadboard, a dual motor driver board, a battery pack, and eventually an HC-SR04 ultrasonic sensor. There's not a lot of room, and getting everything balanced so the robot doesn't tip onto its nose or drag a corner required a "weird design" — in the words of the build description — that ended up looking like a cluster of components barely held together in working configuration.

Which, honestly, is part of the charm of a first robot build. It doesn't need to look elegant. It needs to roll straight and avoid the furniture.

## Mounting the Arduino

The Arduino Uno mounts on standoffs through the pre-drilled holes in the chassis base plate. The standard Arduino mounting hole pattern (four M3 holes at the corners of the board) lines up with holes on the Pololu chassis or can be drilled to match. Nylon standoffs are preferred over metal: they're lighter, they don't conduct electricity (so a solder blob on the bottom of the Arduino doesn't short to the chassis plate), and they're easy to cut to the right height.

The USB port on the Arduino needs to stay accessible — you'll be uploading new sketches throughout testing. Orient the Arduino so the USB port faces toward the outside of the chassis rather than being buried under the breadboard. This sounds obvious until you've mounted one facing the wrong direction and then had to disassemble half the robot to reprogram it.

## The breadboard layout

A half-size breadboard sits on the platform alongside the Arduino. This holds the motor driver board, the HC-SR04 wiring, and any additional components like an indicator LED or the filter capacitor across the motor supply. The breadboard is the prototyping area — nothing here is permanent, which is exactly the point.

The motor driver board (with the headers soldered in the previous episode) plugs into the breadboard. Jumper wires connect from the breadboard to the Arduino digital pins for direction and speed control, and from the breadboard out to the motor leads. The HC-SR04 sensor also connects through the breadboard.

## The balance problem

A round chassis with a heavy gearbox spanning its middle and a battery pack below the plate will tip if the center of gravity ends up forward of the contact point triangle. The contact points are the two drive wheels and the rear ball caster. Add a 25g Arduino and a battery at the front of the platform, and suddenly the front of the robot is heavier than the rear — the robot wants to pivot forward on the wheels and drag the caster off the ground.

The solution for ClusterBot is the "weird design" mentioned in the build description: positioning the battery pack and Arduino so their weight roughly balances across the wheel axis. This sometimes means the Arduino ends up in an awkward spot — not centered, rotated at an odd angle, or overhanging the edge slightly. The breadboard goes where it fits. Wires route unconventionally.

The test: lift the robot by the middle and check whether it hangs level. If it nose-dives, move weight backward. If the rear sags, move weight forward. The ball caster should sit flat on a surface when the robot is idle with no external forces on it.

## Wiring it together

With everything physically mounted, the wiring pass completes the build:

The Arduino's 5V and GND pins connect to the breadboard power rails. The motor driver's VCC (logic supply) draws from the 5V rail; its GND connects to the common ground rail. The motor battery pack's negative lead also connects to the common ground rail — this is the critical common-ground tie between the two power domains. The motor battery positive connects to the driver's VM pin.

From the Arduino's digital pins: four wires go to the motor driver's control inputs (AIN1, AIN2, BIN1, BIN2). Two more wires go to the PWM pins used for speed control (PWMA, PWMB). One wire goes to the STBY pin, which gets pulled HIGH in setup. The HC-SR04's trigger and echo pins connect to two more Arduino digital pins.

When the wiring is done, do a sanity check before powering up: verify there's no continuity between the 5V Arduino supply and the motor supply VM (they should be isolated except at ground). Verify the STBY pin is indeed wired and not floating — a floating STBY keeps the driver disabled and no amount of code will move the motors.

## What "finished" looks like

A complete ClusterBot frame has: two wheels rolling freely on the gearbox output shafts, a ball caster that swivels without binding, an Arduino Uno seated on standoffs with the USB port accessible, a breadboard with the motor driver and all jumper wires in place, a battery pack secured to the chassis, and a sensor mounting point at the front. Compact, a little chaotic-looking, but functional.

The next step — loading the obstacle avoidance sketch and watching it move for the first time — is the payoff for all the physical assembly work that came before.

## ClusterBot build series

1. [Assemble the Pololu chassis](/blog/clusterbot-pololu-robot-chassis-assembly)
2. [Solder wires to the Tamiya motors](/blog/clusterbot-solder-tamiya-motor-wires)
3. [Solder headers onto the Pololu motor driver](/blog/clusterbot-solder-pololu-motor-driver-headers)
4. [Install the battery pack](/blog/clusterbot-arduino-battery-pack)
5. Finish the robot frame **(this episode)**
6. [HC-SR04 obstacle avoidance live demo](/blog/clusterbot-hcsr04-obstacle-avoidance-demo)

## References and further reading

- [Arduino Uno dimensions and mounting holes | Arduino](https://docs.arduino.cc/hardware/uno-rev3) — official mechanical drawings for the Uno PCB
- [Nylon standoff kit | Amazon](https://www.amazon.com/dp/B012DZTRRY) — the type of hardware used to mount the Arduino on acrylic platforms
- [Center of gravity in wheeled robots | Robotics StackExchange](https://robotics.stackexchange.com/questions/296/how-do-i-calculate-the-center-of-gravity-for-a-two-wheeled-robot) — discussion of balance considerations for differential-drive robots
- [Prototyping with breadboards | SparkFun](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard) — covers the breadboard wiring conventions used throughout this build
