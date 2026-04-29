---
title: 'How to Use a PIR Sensor to Detect Motion'
description: 'The HC-SR501 PIR sensor is one of the most practical components you can add to an Arduino project. Three wires, a handful of configuration options, and you have reliable motion detection for under $2.'
pubDate: 'July 28 2021'
youtubeId: 'EqWxUT4o8kA'
heroImage: '../../assets/posts/use-pir-sensor-motion-detection-arduino/thumbnail.jpg'
tags: ['arduino', 'sensor', 'pir', 'motion', 'tutorial']
---

Security systems, automatic lights, alarm triggers — a surprising amount of infrastructure relies on one of the simplest sensor types in electronics. A PIR sensor (Passive Infrared) detects the infrared radiation emitted by warm bodies moving through its field of view. It doesn't actively emit anything, which is where the "passive" comes from. It just listens for changes in the infrared energy of the scene in front of it, and pulls an output pin high when it detects movement.

The HC-SR501 is the ubiquitous version of this sensor in the hobbyist world. It costs around $1–2 in quantity, it runs on 5–12 V, and it works reliably right out of the bag. This post covers how it works, what the adjustment trimmers and the jumper do, and how to wire it up.

## What's on the module

The HC-SR501 is built around the BISS0001 PIR controller IC and a RE200B pyroelectric sensing element — the white hemispherical dome on top. That dome is a Fresnel lens, and it's doing real optical work: it focuses incoming infrared into the sensing element and divides the field of view into zones, so the sensor responds more strongly to motion across the field than to slow approach.

Flip the module over and you'll find three pins: VCC, GND, and OUT. On many HC-SR501 modules the pin labels are hidden underneath the dome — pop it off to see them. It's press-fit and comes back on cleanly.

You'll also find two small trim potentiometers and a two-position jumper. These are where most of the useful configuration lives.

## The two trimpots

The sensitivity pot adjusts how much of a change in infrared energy triggers a detection. Full clockwise is maximum sensitivity — it'll catch motion from across a room and may trigger on air currents from vents or other heat sources. Back it off counterclockwise if you're getting false triggers.

The time pot controls the *retrigger delay* — the window after a detection event during which the sensor won't fire again, even if there's continued motion. Fully counterclockwise gives you the minimum delay, which is approximately 10 seconds on the module used in the video. Full clockwise stretches that to around 5 minutes. This prevents a single person walking through a doorway from generating a rapid-fire stream of triggers.

The catch with these trimpots: they're typically unlabeled. There's no S and T printed on the board, no arrows indicating which does which. You have to figure it out by testing. The trick used in the video — mark one pot with a small dot of permanent marker once you've identified it — is the right call. Otherwise you'll forget which is which within a day.

## The jumper: H vs. L

The jumper on the HC-SR501 selects one of two trigger modes.

On **H (high)**, the output goes and stays HIGH the entire time motion is being detected, for at least the duration set by the time pot. If motion continues, the output stays high; when nothing has moved long enough for the timer to elapse, it goes low. This is usually what you want for a "light turns on while someone is in the room" application.

On **L (low)**, the output alternates between high and low each time it detects motion — a toggle behavior rather than a sustained signal. Less commonly used, but useful for edge-triggered applications.

For most projects, leave it on H.

## Wiring: LED demo with no microcontroller

The simplest possible demo uses the Arduino board as nothing more than a power supply — no sketch, no code at all.

Connect VCC on the HC-SR501 to the Arduino's 5V pin and GND to GND. The OUT pin goes directly to the anode of an LED (through a 220 Ω resistor), with the LED cathode back to GND. When the sensor detects motion, it outputs 5 V, which drives the LED.

That's three connections, and it works. The LED lights when you walk into the sensor's view, holds for the time-pot duration, then goes out.

## Wiring: using the output with a microcontroller

When you want to read the sensor's state in code — to trigger something more interesting than an LED — connect the OUT pin to any digital input pin on the Arduino. Then read it like any other digital input:

```cpp
const int pirPin = 2;
const int ledPin = 13;

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int motionState = digitalRead(pirPin);
  if (motionState == HIGH) {
    digitalWrite(ledPin, HIGH);
    Serial.println("Motion detected");
  } else {
    digitalWrite(ledPin, LOW);
  }
}
```

The output is a clean digital signal — HIGH when motion is present, LOW otherwise. No analog read, no threshold math. It's one of the easier sensors to integrate.

## The gotcha: the 60-second warm-up

When you first apply power to an HC-SR501, it needs 30–60 seconds to stabilize before it's reliable. During this window, it's calibrating its baseline reading of the ambient infrared environment in front of it. It will often false-trigger repeatedly during warm-up, which can be alarming if you're not expecting it.

The right approach is to delay your application startup by at least 60 seconds after power-on, or to watch for false triggers with a counter and ignore them for the first minute. If you're uploading a sketch and the sensor seems to be triggering randomly, this is almost certainly why — just wait.

## Detection range and angle

The HC-SR501's detection range is up to 7 meters, with an approximate field of view of 110°. In practice, in a small room with reflective walls, it's sensitive enough that you'll want the sensitivity pot turned down somewhat unless you want it triggering off movement on the far side of the room. The Fresnel dome can be removed and replaced with a different lens profile to change the field angle, though that's an unusual modification for most projects.

## References

- [Last Minute Engineers: HC-SR501 PIR Sensor with Arduino](https://lastminuteengineers.com/pir-sensor-arduino-tutorial/) — the most thorough reference writeup on this sensor
- [BISS0001 datasheet](https://www.ladyada.net/media/sensors/BISS0001.pdf) — the controller IC
- [Adafruit PIR sensor overview](https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor) — Adafruit's guide covers theory, wiring, and troubleshooting
- [Arduino `digitalRead()` reference](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/)
- [Makerguides: HC-SR501 Arduino Tutorial](https://www.makerguides.com/hc-sr501-arduino-tutorial/)
