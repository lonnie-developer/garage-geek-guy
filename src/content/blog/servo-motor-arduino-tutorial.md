---
title: 'How to Use a Servo Motor with an Arduino'
description: 'Wiring an SG90 9g servo to an Arduino Uno and running the Sweep example — three wires, one library, and the important rule about which servos you can actually power from the board.'
pubDate: 'October 24 2018'
youtubeId: 'l1t00BvOE4o'
heroImage: '../../assets/posts/servo-motor-arduino-tutorial/thumbnail.jpg'
tags: ['arduino', 'servo', 'sg90', 'tutorial', 'servo-library']
---

There's a category of Arduino project where knowing how to control a servo motor unlocks everything: pan-tilt camera mounts, robot grippers, steering mechanisms, animatronic gadgets, anything where you need precise angular positioning. The servo takes care of the hard part — the feedback loop, the driver electronics, the gear reduction — and leaves you with a three-wire interface and a single `write()` call to point it wherever you want.

This walkthrough uses an SG90 9g micro servo, which is the right place to start for two reasons. First, it's inexpensive — a five-pack from eBay runs a few dollars, and individual units are similarly cheap from any hobbyist supplier. Second, and more importantly, it's small enough to power directly from the Arduino. That constraint matters, and we'll come back to it.

## The SG90 and what the three wires mean

The SG90 is a 9-gram micro servo that outputs about 1.8 kg·cm of torque on a 4.8V supply. Its operating range is 0–180°. It draws about 10 mA idle, 100–250 mA when actively moving, and up to 500–700 mA at stall.

The three wires coming off the connector are ground, power, and signal. The color coding on SG90s and their clones is brown-red-orange, but it's not universal — other brands use black-red-yellow, or black-red-white, or other combinations. The signal wire is usually the lightest color (orange, yellow, or white). If you're ever unsure, look up the datasheet or the seller listing for your specific servo rather than guessing.

| Wire color (SG90) | Function | Connects to |
|---|---|---|
| Brown | Ground | Arduino GND |
| Red | Power (5V) | Arduino 5V |
| Orange | Signal | Arduino digital pin 9 |

The signal pin doesn't have to be pin 9. The Arduino Servo library works with any digital pin. The examples use pin 9 by convention.

## Wiring

Connect the servo's brown wire to any GND pin on the Arduino, red to the 5V pin, and orange to digital pin 9. That's it. No breadboard required for this basic connection — the servo connector can plug onto male header pins directly if you add jumpers from each servo wire to the matching Arduino pin.

**The critical rule about power:** only power small servos directly from the Arduino's 5V pin. The SG90 draws around 200 mA when moving — within the roughly 500 mA budget of the Arduino's 5V pin (less whatever the board itself uses). A larger servo — the MG995, MG996R, or any servo labeled "standard size" or higher torque — can draw 500 mA to 1 A or more, which will overdraw the Arduino's onboard regulator, cause voltage drops, reset the board, or in bad cases damage it. For anything larger than a micro or mini servo, use an external 5V power supply and share only the ground with the Arduino.

## The code: Servo library and the Sweep example

The Arduino IDE ships with the Servo library built in. No installation needed. Find the Sweep example at File → Examples → Servo → Sweep, or copy the code below.

```cpp
#include <Servo.h>

Servo myServo;   // create a Servo object — name it whatever you like

int pos = 0;     // variable to store the servo position in degrees

void setup() {
  myServo.attach(9);  // attaches the servo to digital pin 9
}

void loop() {
  // sweep from 0° to 180°, one degree at a time
  for (pos = 0; pos <= 180; pos += 1) {
    myServo.write(pos);   // tell servo to go to position 'pos'
    delay(15);            // wait 15ms for the servo to reach the position
  }
  // sweep back from 180° to 0°
  for (pos = 180; pos >= 0; pos -= 1) {
    myServo.write(pos);
    delay(15);
  }
}
```

Upload it. The servo sweeps back and forth between 0° and 180°, pausing 15 milliseconds between each 1° step.

## Tuning the speed

The speed is controlled by two variables: the step size (how many degrees per iteration) and the delay (how long to wait at each position).

Changing the increment from `+= 1` to `+= 5` makes the servo move much faster — it jumps 5° per step. The trade-off is that if the delay is too short, the servo doesn't have time to actually reach the commanded position before the next command arrives, and you'll see it fall short of 180° before reversing.

```cpp
// faster but may not complete the full sweep at small delays
for (pos = 0; pos <= 180; pos += 5) {
  myServo.write(pos);
  delay(15);   // may need to increase to 20–30ms if sweep doesn't complete
}
```

If the servo isn't reaching the endpoints, increase the delay until it does. The `delay()` value needed depends on the servo's speed rating and the load on the output shaft.

## Beyond the sweep

The `write()` command accepts any integer from 0 to 180, so you can point the servo at a specific angle directly:

```cpp
myServo.write(90);   // center position
myServo.write(0);    // one extreme
myServo.write(180);  // other extreme
```

For finer control — mapping an analog input like a potentiometer to servo position — use `map()`:

```cpp
int reading = analogRead(A0);                // 0–1023
int angle = map(reading, 0, 1023, 0, 180);  // scale to 0–180°
myServo.write(angle);
```

This is the foundation for a manually-controlled servo, a pan-tilt mount driven by joystick inputs, or a steering mechanism in a wheeled robot.

## Where this doesn't apply

This walkthrough covers small servos powered from the Arduino board. Once you move to standard-size servos for more torque — or to more than two or three micro servos running simultaneously — you need an external 5V supply. A dedicated servo tutorial covering external power supply and multiple servos is a separate walkthrough on this channel.

## What you'll need

- Arduino Uno or compatible
- SG90 9g micro servo (or similar micro-class servo)
- Three jumper wires (male-to-female if using the servo's stock connector)

## References and further reading

- [Arduino Servo library reference](https://www.arduino.cc/reference/en/libraries/servo/) — `attach()`, `write()`, `writeMicroseconds()`, `read()`, and more
- [Arduino Sweep example](https://docs.arduino.cc/built-in-examples/servo/Sweep/) — the example used in this video
- [SG90 datasheet — Tower Pro](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf) — operating specs, torque curve, PWM timing
- [Servo motor with external power supply](https://www.arduino.cc/en/Tutorial/LibraryExamples/Knob) — when you graduate to larger servos
