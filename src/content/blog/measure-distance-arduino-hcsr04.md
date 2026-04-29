---
title: 'How to Measure Distance with an Arduino and HC-SR04 Ultrasonic Sensor'
description: 'The HC-SR04 is dollar-store radar for your Arduino — four pins, a library, and a few lines of code give you distance readings in centimeters. Here is how to wire it, code it, and deal with its quirks.'
pubDate: 'August 26 2021'
youtubeId: 'siIoDgkUPEs'
heroImage: '../../assets/posts/measure-distance-arduino-hcsr04/thumbnail.jpg'
tags: ['arduino', 'hc-sr04', 'ultrasonic', 'sensor', 'distance', 'tutorial']
---

The HC-SR04 is basically a dollar of radar. You can buy ten of them for around $12 on eBay, they run directly off 5V, they talk to an Arduino with two signal pins, and they'll tell you how far away something is in centimeters with reasonable accuracy up to about 250 cm. For an object-avoidance robot, a parking sensor, a liquid-level gauge, or anything else that needs to know "is there something in front of me and how close is it," the HC-SR04 is the first part you reach for.

This post covers wiring, the library, code for two different output setups (LCD and serial monitor), and the specific quirk that will bite you if you rely on single measurements without error checking.

## How it works

The HC-SR04 has two cylindrical transducers on its face — one transmitter, one receiver. When triggered, the transmitter fires a short burst of 40 kHz ultrasonic pulses. Those pulses travel through the air, bounce off whatever is in front of the sensor, and return to the receiver. The module measures the round-trip time of that echo, and since the speed of sound in air is roughly known (about 343 m/s at room temperature), the distance calculation is straightforward: distance = (time × speed of sound) / 2, divided by 2 because the pulse makes a round trip.

It's the same principle as sonar and bat echolocation. The "dollar radar" framing isn't far off — the only meaningful difference between this and a proper ultrasonic rangefinder is accuracy, range, and the quality of the signal processing. For hobby distances under 2 meters, the HC-SR04 is plenty good enough.

## The module itself

The HC-SR04 has four pins:

- **VCC** — 5V power
- **GND** — ground
- **Trig** — trigger input (you pulse this HIGH to start a measurement)
- **Echo** — echo output (the module holds this HIGH for a duration proportional to distance)

The Trig and Echo pins are the two you connect to Arduino digital pins. VCC and GND go to 5V and GND on the Arduino. The module is small enough to press-fit into a breadboard, which makes it a convenient holder as well as a connection method.

The rated range is 2 cm to 400 cm, though in practice reliable readings drop off past 200–250 cm and get inconsistent at very short distances under about 3–4 cm. The stated accuracy is ±3 mm, which holds up reasonably well in clean conditions.

## What you'll need

- HC-SR04 ultrasonic distance module (~$1 each on eBay, or ~$12 for a pack of 10)
- Arduino Uno or similar
- Mini breadboard (optional, but useful for mounting the sensor)
- Jumper wires
- 1602 I2C LCD display (optional — you can use the serial monitor instead)

If you want to display readings on an LCD, wire that up first following the [1602 I2C LCD tutorial](/blog/arduino-i2c-lcd-1602). The sensor demo in the video uses the LCD for output, but all the distance logic works the same way if you swap `lcd.print()` for `Serial.print()`.

## Wiring

Connect the HC-SR04 to the Arduino:

- **VCC** → Arduino 5V
- **GND** → Arduino GND
- **Echo** → Arduino pin 12
- **Trig** → Arduino pin 13

If you're using the LCD as well, it connects on its own SDA/SCL lines (A4 and A5 on the Uno) and doesn't interfere with the sensor pins.

## Installing the library

The HC-SR04 library handles all the timing math — you don't need to manually measure pulse widths. Open `Tools → Manage Libraries` in the Arduino IDE and search for **HC-SR04**. Several libraries come up; the one used in the video is **HC-SR04 by Dirk Sarodnick**, version 1.1.2. Install it.

## The sketch

Here's a complete sketch that reads distance and prints it to an I2C LCD:

```cpp
#include <LiquidCrystal_I2C.h>
#include <HCSR04.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
UltraSonicDistanceSensor distanceSensor(13, 12);  // Trig pin, Echo pin

void setup() {
  lcd.begin();
  lcd.backlight();
}

void loop() {
  double distance = distanceSensor.measureDistanceCm();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Dist: ");
  lcd.print(distance);
  lcd.print(" cm");

  delay(100);
}
```

If you'd rather use the serial monitor instead of the LCD:

```cpp
#include <HCSR04.h>

UltraSonicDistanceSensor distanceSensor(13, 12);

void setup() {
  Serial.begin(9600);
}

void loop() {
  double distance = distanceSensor.measureDistanceCm();
  Serial.println(distance);
  delay(100);
}
```

Upload either version, point the sensor at something, and you should see live distance readings. At 100 ms delay you get 10 measurements per second, which is fast enough for most applications without overwhelming the display.

## The gotcha: spurious readings

Here's the thing the HC-SR04 tutorials usually gloss over: the sensor lies sometimes, and when it lies, it lies badly.

Point it at a wall at an angle. Move it fast. Hold it in certain orientations. You'll get readings that are obviously wrong — a -1 (the library's error code for a failed measurement), a reading three times the actual distance, or a sudden spike to maximum range. These aren't rare edge cases; they happen during normal use.

The fix is not to trust a single reading. A simple and effective approach is to take several measurements in quick succession, discard the highest and lowest values, and average what's left — sometimes called a trimmed mean. Here's one way to do it:

```cpp
double getStableDistance() {
  const int samples = 5;
  double readings[samples];

  for (int i = 0; i < samples; i++) {
    readings[i] = distanceSensor.measureDistanceCm();
    delay(20);
  }

  // Simple sort to find min/max
  double minVal = readings[0], maxVal = readings[0], sum = 0;
  for (int i = 0; i < samples; i++) {
    if (readings[i] < minVal) minVal = readings[i];
    if (readings[i] > maxVal) maxVal = readings[i];
    sum += readings[i];
  }

  // Subtract min and max, average the rest
  return (sum - minVal - maxVal) / (samples - 2);
}
```

For a robot that needs to decide "is there an obstacle within 30 cm," a stable filtered reading is much more reliable than acting on whatever single measurement happens to come in. Plan for this from the start rather than debugging it after.

## Range and angle considerations

The HC-SR04 measures best when the target surface is roughly perpendicular to the sensor beam. Angled surfaces scatter the pulse, reduce the reflected signal, and can cause missed detections or incorrect readings. For most obstacles a robot might encounter — walls, boxes, legs of furniture — this isn't a problem. For thin poles, angled corners, or sound-absorbing materials like foam, expect reduced range and higher error rates.

The effective sensing cone is roughly 15° to either side of center. Objects outside that cone won't be detected reliably, which is worth knowing if you're building a robot with limited sensor coverage. Mounting sensors at angles, or using multiple sensors, is the typical solution for wider coverage.

## Where this fits on a robot

The HC-SR04 is the standard first range sensor for Arduino-based robots, and for good reason: it's cheap, it's simple to code, and it works well enough for basic object avoidance. A single sensor on the front will tell you "something is close" with enough reliability to stop the robot and turn.

For more sophisticated navigation — mapping, multiple simultaneous targets, fast-moving platforms — you'll want something better. The Sharp IR distance sensors are analog and don't have the multi-path issues, but have their own non-linearity problems. A real sonar array or a LIDAR module like the RPLidar is the next tier. But for a $1 sensor that gets you up and running in an afternoon, the HC-SR04 is hard to argue with.

## References and further reading

- [HC-SR04 datasheet (PDF)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — timing diagrams and electrical specs
- [Arduino Library: HC-SR04 by Dirk Sarodnick](https://github.com/d-a-v/hcsr04) — the library used in this tutorial
- [Last Minute Engineers: HC-SR04 tutorial](https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/) — covers manual pulse timing without a library
- [Adafruit: Ultrasonic sonar article](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors) — good background on how ultrasonic ranging works
- [Arduino Playground: MedianFilter](https://playground.arduino.cc/Main/RunningMedian/) — a more robust filtering library for noisy sensor data
