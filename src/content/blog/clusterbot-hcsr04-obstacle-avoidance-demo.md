---
title: 'ClusterBot — HC-SR04 Arduino Obstacle Avoidance Live Demo'
description: 'Watch ClusterBot, an Arduino-powered robot, avoid obstacles in real time using an HC-SR04 ultrasonic sensor. Covers how the sensor works, the obstacle-avoidance sketch logic, and what makes this a good first robotics project.'
pubDate: 'January 23 2012'
youtubeId: 'ivvVy6KpTfU'
heroImage: '../../assets/posts/clusterbot-hcsr04-obstacle-avoidance-demo/thumbnail.jpg'
tags: ['arduino', 'robotics', 'clusterbot', 'hc-sr04', 'ultrasonic', 'obstacle-avoidance', 'tutorial']
---

*The final episode of the ClusterBot build series — the payoff: the completed robot running the obstacle-avoidance sketch on a real floor. No narration, no overlays, just the robot doing the thing it was built to do.*

The moment a robot you built moves through a room on its own, sensing and responding to the world without any input from you, is a genuinely good moment. It doesn't matter that the logic is simple. It doesn't matter that the obstacle course is plastic storage bins and a laptop on the floor. The robot is navigating. That's the thing.

ClusterBot is a two-wheeled differential-drive robot on a Pololu round chassis, with an Arduino Uno as its brain and a single HC-SR04 ultrasonic distance sensor mounted at the front. The obstacle-avoidance behavior is a simple threshold loop: read the sensor, compare to a threshold, steer accordingly. It works surprisingly well.

## The HC-SR04 ultrasonic sensor

The HC-SR04 is the canonical beginner ultrasonic distance sensor, introduced around 2010–2011 and still ubiquitous. It has four pins: VCC (5V), GND, Trig (trigger input), and Echo (echo output). It operates at 40kHz — well above human hearing — and can measure distances from 2cm to about 400cm, though reliable accuracy holds up to about 200cm in practice.

The operating principle: send a 10-microsecond HIGH pulse on the Trig pin, and the sensor fires 8 cycles of 40kHz ultrasound from the transmitter transducer. When the pulse reflects off an object and returns to the receiver transducer, the Echo pin goes LOW. The time the Echo pin spends HIGH — from the end of the Trig pulse to the falling edge of Echo — is proportional to the round-trip distance. Divide by 58 for centimeters, or 148 for inches.

The sensor has a roughly 15–30 degree effective beam angle. Objects outside that cone don't register, which means ClusterBot can miss obstacles to the side and sometimes scrape corners on its way through a gap. For a basic "don't drive into things" behavior, the front-mounted sensor is sufficient. For more complete coverage, you'd add sensors to the sides or mount the HC-SR04 on a servo to sweep.

## The obstacle-avoidance sketch

The core logic is a loop that runs continuously. Each pass through the loop takes a distance reading; if the reading is below a threshold, the robot turns; if it's clear, the robot drives forward. The structure:

```cpp
void loop() {
  int distance = readDistance();

  if (distance < STOP_DISTANCE) {
    stopMotors();
    delay(100);
    reverse(TURN_SPEED);
    delay(300);
    turnRight(TURN_SPEED);
    delay(500);
  } else {
    driveForward(FULL_SPEED);
  }

  delay(50); // reading interval
}
```

The thresholds are the tuning knobs: `STOP_DISTANCE` determines how close is too close. Set it too low and the robot collides before it can turn; too high and it's timid, stopping two feet from every object. For a floor obstacle course with items like storage bins, 15–20cm is a reasonable starting point.

`TURN_SPEED` and the turn delay together determine how far the robot rotates before checking again. Too short a turn on a close obstacle puts the robot facing another obstacle; too long and it spins in circles in a corner. These values get tuned by running the robot on a real floor and watching what happens.

## The NewPing library

In 2012, the standard library for the HC-SR04 was NewPing by Tim Eckel. The raw `pulseIn()` approach has a problem: if no echo is received (the object is too far away or the pulse is absorbed), `pulseIn()` waits for its full timeout before returning. That's up to 30ms per reading — long enough to cause visible motor stuttering and slow the obstacle-avoidance loop.

NewPing solves this with timer-based reading and a configurable timeout. `sonar.ping_cm()` returns quickly whether or not an echo arrives, keeping the control loop responsive. It also offers `ping_median(iterations)` to filter out spurious readings — a median of 5 samples takes about 25ms total but is much less prone to false detects from vibration or environmental noise.

## What the video shows

ClusterBot navigating a hardwood floor with a handful of objects scattered around — plastic storage cases, a tin, a small ottoman, a laptop. The robot drives forward until it detects an obstacle, backs up slightly, turns, and proceeds. It doesn't always make the cleanest decisions — a slow turn radius and the 2×AA voltage sag mean it sometimes just barely clears an obstacle — but it navigates the whole obstacle course without hitting anything.

That's the test. A robot that navigates a cluttered room floor on two AA batteries, a $25 chassis, a $4 motor driver, and a $2 ultrasonic sensor, programmed with about 80 lines of Arduino code. Total hardware investment under $60 in 2012.

## What you'd change for a better robot

The two-AA motor supply is the biggest limitation. Four AAs or a small LiPo at 7.4V through the motor driver would give the motors consistent speed across the whole battery discharge curve. At 6V the robot is noticeably more responsive than at 3V.

A servo-mounted sensor — rotating the HC-SR04 to scan left and right before committing to a turn direction — dramatically improves navigation. The fixed-front sensor means the robot always turns the same way regardless of whether there's a wall on both sides or an open path to the left. A sweep-and-compare before turning gets you smarter decisions.

Adding a second ultrasonic sensor or a pair of IR distance sensors to the sides would catch the obstacles that fall outside the front sensor's cone, especially in tight spaces.

None of these improvements change the core lesson: a single HC-SR04 with a threshold-compare loop is enough for a convincing first demonstration of autonomous navigation. Start here, then extend.

## ClusterBot build series — complete

1. [Assemble the Pololu chassis](/blog/clusterbot-pololu-robot-chassis-assembly)
2. [Solder wires to the Tamiya motors](/blog/clusterbot-solder-tamiya-motor-wires)
3. [Solder headers onto the Pololu motor driver](/blog/clusterbot-solder-pololu-motor-driver-headers)
4. [Install the battery pack](/blog/clusterbot-arduino-battery-pack)
5. [Finish the robot frame](/blog/clusterbot-finish-robot-frame)
6. HC-SR04 obstacle avoidance live demo **(this episode)**

## References and further reading

- [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — operating specs, timing diagram, and mechanical dimensions
- [NewPing library | Arduino Playground](https://playground.arduino.cc/Code/NewPing/) — documentation and download for Tim Eckel's HC-SR04 library
- [Ultrasonic distance sensor tutorial | SparkFun](https://learn.sparkfun.com/tutorials/ping-ultrasonic-distance-sensor) — how the sensor works with clear diagrams of the timing protocol
- [Arduino obstacle avoidance robot | Instructables](https://www.instructables.com/Obstacle-Avoiding-Robot/) — a similar project that adds a servo-mounted sensor for directional scanning
- [HC-SR04 limitations and filtering | RobotShop Community](https://www.robotshop.com/community/forum/t/hc-sr04-false-readings-and-filtering/13571) — discussion of the false-detect issue that NewPing's median filter addresses
