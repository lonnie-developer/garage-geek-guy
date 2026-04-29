---
title: 'How to Use the L298N Motor Driver with Arduino — Wiring + PWM Speed Control'
description: 'Everything you need to wire and code the L298N dual H-bridge motor driver with Arduino — IN1-4, ENA/ENB, common ground, PWM speed control, and the stall-current trick nobody documents.'
pubDate: 'August 29 2021'
youtubeId: 'drYpq7qxyYs'
heroImage: '../../assets/posts/l298n-motor-driver-arduino-pwm/thumbnail.jpg'
tags: ['arduino', 'motor-driver', 'l298n', 'robotics', 'pwm', 'tutorial']
---

The Arduino Uno's digital output pins are rated for 40 mA maximum. A typical small DC motor wants 250–500 mA just to turn freely, and several times that under load. If you connect a motor directly to an Arduino pin, you'll either blow the pin driver or the USB hub or the voltage regulator — and whichever one fails first will teach you why you needed a motor driver in an unpleasant way.

The L298N is the cheap blue board with the big heat sink that you'll find in almost every beginner Arduino robot kit. It sits between your battery pack and your motors, accepts direction and speed commands from the Arduino's low-current signal pins, and handles the actual current delivery from its own power supply. For two small DC motors, a 4xAA battery pack, and an Arduino Uno, it's the right tool for the job.

This post walks through every connection, every code variable, and the specific PWM trick that keeps your motors from stalling out at low speeds.

## Why you can't drive a motor from an Arduino pin

It's worth spending a minute on this because "you need a motor driver" is advice you'll get everywhere, and it's useful to understand what the driver is actually doing.

An Arduino's output pin is driven by the microcontroller's GPIO logic, which operates at low current — enough to light an LED, trigger a logic-level transistor, or talk to a sensor. Motors are inductive loads that draw heavy current and generate back-EMF when they spin (or when they stop suddenly). Connecting that kind of load directly to a GPIO pin breaks the pin, corrupts the voltage on the logic rail, or resets the microcontroller — sometimes all three.

A motor driver solves this by using the Arduino's logic signal as a low-power control input and doing the actual work with a separate power path — the H-bridge circuitry inside the L298N chip, powered by your motor battery pack. The Arduino tells it what to do; the L298N does the heavy lifting.

## What the L298N board is

The L298N is a dual H-bridge driver chip from STMicroelectronics, originally specified for driving inductive loads like DC motors and stepper motors. The blue module you'll find on Amazon and AliExpress for $3–6 is a breakout board that puts the L298N chip, its required decoupling capacitors, a flyback diode array, and a small onboard 5V regulator onto a compact PCB with screw-terminal outputs and header pins for the control signals.

Key specs from the [L298N datasheet](https://www.st.com/resource/en/datasheet/l298.pdf): motor supply voltage from 5V to 46V, continuous current of 2A per channel, peak current up to 3A per channel. For 6V hobby motors those numbers are plenty of headroom.

One note on the onboard 5V regulator: the L298N board includes a small voltage regulator that can supply 5V to the Arduino from the motor battery, which is handy for simple setups. If your motor supply voltage is above 12V, remove the jumper next to the regulator first — at higher voltages the regulator overheats. For a 6V four-AA battery pack, leave the jumper on; it's fine.

## The wiring

### Motor connections

The two screw-terminal blocks on the short ends of the board are the motor outputs. One terminal block drives motor A (left side, typically), the other drives motor B. Each motor gets two wires into its block — the polarity determines which direction the motor defaults to, and you can always flip it in code via the IN pins.

### Power connections

The three-terminal block in the center handles power:

- **+12V** — connect your motor battery positive here. Despite the label, it accepts 5–46V; the silkscreen is just optimistic about what voltage you're using.
- **GND** — motor battery negative here.
- **5V** — this can output 5V to the Arduino (from the onboard regulator) or accept 5V in (if you've removed the regulator jumper and are powering the Arduino separately).

### The common ground — don't skip this

Both the motor battery ground and the Arduino GND must be connected together. If they're on separate grounds, the Arduino's IN1–IN4 signals have no reference point, the L298N sees garbage on its control pins, and the behavior is unpredictable.

The simplest approach: run a wire from the L298N's GND terminal to one of the Arduino's GND pins. That's it. One wire, but critical.

### IN1, IN2, IN3, IN4 — direction control

These four pins go from the L298N to four Arduino digital output pins. IN1 and IN2 control motor A; IN3 and IN4 control motor B. For each motor, you set one pin HIGH and the other LOW to spin — swapping which is HIGH and which is LOW reverses the direction.

```
Motor A forward:  IN1 = HIGH, IN2 = LOW
Motor A reverse:  IN1 = LOW,  IN2 = HIGH
Motor A brake:    IN1 = HIGH, IN2 = HIGH  (or both LOW)
```

Motor B works identically with IN3 and IN4.

In Lonnie's robot build, the motors are mounted on opposite sides of the chassis facing each other. Because of that mirror mounting, setting one motor "forward" and the other "reverse" actually drives both wheels in the same physical direction — both pushing the robot forward. When you get to writing robot routines, forward, back, turn-left, turn-right, and spin-in-place are all just different combinations of IN1–IN4.

### ENA and ENB — speed control

ENA and ENB are the enable pins for each motor channel. By default they come with jumpers installed, which ties them to 5V and runs each motor at full speed whenever IN1/IN2 (or IN3/IN4) command movement.

To get variable speed, remove those jumpers and connect ENA and ENB to Arduino pins that support PWM — the ones with the tilde (~) symbol next to the pin number on the Uno's silkscreen. Pins 3, 5, 6, 9, 10, and 11 all support PWM on the Uno; pins 10 and 11 are a natural pair since they're adjacent.

Once connected, you control motor speed with `analogWrite()`:

```cpp
analogWrite(ENA, 200);  // ~78% speed
analogWrite(ENA, 0);    // stopped
analogWrite(ENA, 255);  // full speed
```

## The code

Here's the full sketch, including the potentiometer speed control from the video:

```cpp
// Motor A
const int IN1 = 0;
const int IN2 = 1;

// Motor B
const int IN3 = 2;
const int IN4 = 3;

// Enable (PWM speed) pins
const int ENA = 10;
const int ENB = 11;

// Potentiometer
const int POT_PIN = A5;

int drive;
int converted;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(POT_PIN, INPUT);
}

void loop() {
  drive = analogRead(POT_PIN);  // 0 to 1023
  converted = map(drive, 0, 1023, 110, 255);

  // Don't run at stall-current speeds
  if (drive < 50) {
    converted = 0;
  }

  // Set direction — both motors forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  // Set speed
  analogWrite(ENA, converted);
  analogWrite(ENB, converted);
}
```

## The stall current trick — map to 110, not 0

The `map(drive, 0, 1023, 110, 255)` line is the part that's easy to miss and worth understanding.

PWM works by rapidly switching the motor voltage on and off. At 255 (100% duty cycle) the voltage is on continuously — full speed. At 128 the motor gets power half the time. At low duty cycle values, you're sending very short power pulses that aren't long enough to keep the motor shaft turning, but long enough to draw current through the stalled windings and cook them.

Every motor has a minimum PWM threshold below which it stalls. For the cheap 6V hobby motors in this build, that threshold was around 110. Below 110, the motors stopped spinning but the current kept flowing through the windings — exactly the situation you don't want for motor longevity.

Mapping the pot range to 110–255 instead of 0–255 means the lowest "on" speed the driver ever commands is 110, safely above the stall point. The separate `if (drive < 50) { converted = 0; }` check handles the fully-off case — if the potentiometer is all the way down, cut the power entirely rather than outputting 110.

Your exact stall threshold will depend on your motors. A good way to find it: start at 255, step down by 5 each time you upload, and watch when the motors stop turning but the driver is still getting the PWM signal. That bottom value plus 10–15 is a safe floor.

## From speed demo to robot routines

The sketch above handles speed control in one direction. For a real robot, you'll want named routines for each movement:

```cpp
void forward(int speed) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void backward(int speed) {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void spinLeft(int speed) {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
```

One practical note on motor matching: two motors from the same bag rarely spin at exactly the same speed at the same PWM value. If your robot drifts to one side going "straight," run both motors at the same PWM and time one full revolution of each wheel by eye. Throttle the faster one down by 5–10 PWM counts until they match. Define those as constants — `LEFT_SPEED` and `RIGHT_SPEED` — and you'll save yourself a lot of adjustment later.

## Where the L298N fits and where it doesn't

For two small DC motors running at 6–12V, the L298N is hard to beat at the price point. It's a known quantity, tutorial support is everywhere, and the heat sink buys you plenty of thermal headroom for hobby-scale loads.

It does have real limitations. The chip has about 2V of voltage drop across each H-bridge output, which at 6V means your motors are actually seeing around 4V — a meaningful efficiency loss that you won't notice in a demo but will matter if you're trying to squeeze runtime out of a battery pack. The chip also can't do regenerative braking, and it gets genuinely warm under continuous load at high current.

Better alternatives worth knowing: the [TB6612FNG](https://www.adafruit.com/product/2448) has much lower drop-out voltage, higher efficiency, and is a straight pin-compatible replacement for most L298N projects. The [DRV8833](https://www.adafruit.com/product/3297) is similar and even smaller. Both are worth the slight price premium if you're moving from prototype to something that runs on battery for hours.

For this build — a cardboard-chassis learning robot, two 6V motors, 4xAA pack, Arduino Uno — the L298N is exactly the right call. Save the TB6612FNG for when you care about efficiency.

## References and further reading

- [L298N datasheet (STMicroelectronics)](https://www.st.com/resource/en/datasheet/l298.pdf)
- [Last Minute Engineers: L298N Motor Driver module in depth](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) — the most thorough hookup guide available
- [DroneBot Workshop: DC Motors with L298N and Arduino](https://dronebotworkshop.com/dc-motors-l298n-h-bridge/) — good walkthrough of the H-bridge concept
- [HowToMechatronics: Arduino DC Motor Control Tutorial](https://howtomechatronics.com/tutorials/arduino/arduino-dc-motor-control-tutorial-l298n-pwm-h-bridge/)
- [Arduino analogWrite() reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)
- [Adafruit TB6612FNG breakout](https://www.adafruit.com/product/2448) — recommended upgrade if efficiency matters
