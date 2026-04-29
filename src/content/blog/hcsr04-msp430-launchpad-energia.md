---
title: 'HC-SR04 Ultrasonic Sensor with the TI MSP430 Launchpad and Energia'
description: 'The HC-SR04 runs on 5V. The MSP430 Launchpad runs on 3.3V. Here is the two-jumper trick to pull 5V from the Launchpad itself, the Energia pin assignments, and a distance-to-tone sketch that turns the sensor into a theremin.'
pubDate: 'September 10 2012'
youtubeId: 'xKun856q0IQ'
heroImage: '../../assets/posts/hcsr04-msp430-launchpad-energia/thumbnail.jpg'
tags: ['msp430', 'ti-launchpad', 'energia', 'hc-sr04', 'ultrasonic', 'tutorial']
---

The HC-SR04 ultrasonic sensor is cheap — usually around $3 on eBay — and it works well. But it's a 5V device. The MSP430 Launchpad is a 3.3V device. If you pull the HC-SR04's VCC from the Launchpad's VCC pin, you're feeding it 3.3V, and it either behaves erratically or doesn't work at all.

The obvious fix — a separate 5V supply — solves it but adds wiring. The less obvious fix: the Launchpad has two test points near the USB connector that carry 5V *before* the onboard 3.3V regulator. Solder two header pins there, pull your 5V and GND from those points, and the MSP430 itself stays at 3.3V while the sensor gets what it needs.

This post covers the 5V tap, the Energia pin assignments for the HC-SR04, and a sketch that maps distance to tone frequency — a theremin-style demo using nothing but the sensor, a small PC speaker, and the `tone()` command.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The voltage problem and the test-point fix

The Launchpad's onboard USB input goes through a TPS73733 3.3V LDO regulator before it reaches the main VCC rail. Before the regulator, though, there's raw USB 5V. Texas Instruments exposed this as two test points — small through-holes just above the USB connector on the board edge, one for 5V and one for GND.

The procedure: solder a short pin header to each test point. They're close together and the holes are small, but they're not difficult — just slow, careful work. Once the headers are in, run a jumper from the 5V test point to the HC-SR04's VCC pin and from the GND test point to the HC-SR04's GND. The sensor is now on USB 5V. The MSP430 continues running on 3.3V. No level shifting required for the signal lines in this case — the HC-SR04's trigger and echo logic is at 5V but the MSP430 G2 series can tolerate 5V-level inputs on its I/O pins even though it operates at 3.3V.

This same tap works for any low-current 5V device you want to hang off the Launchpad. It's one of those ideas that looks obvious in retrospect once someone shows you where the points are.

## Hardware setup

- MSP430G2553 on a v1.5 TI Launchpad (powered by a USB battery pack — four AA cells in a USB housing)
- HC-SR04 ultrasonic distance sensor
- Small PC case speaker (the kind salvageable from almost any desktop computer)
- Dupont female jumper wires

**Wiring:**

| HC-SR04 pin | Connection |
|-------------|-----------|
| VCC | Launchpad 5V test point |
| GND | Launchpad GND test point |
| TRIG | MSP430 pin 12 (Energia numbering) |
| ECHO | MSP430 pin 13 (Energia numbering) |

Speaker: one terminal to MSP430 pin 6 (Energia numbering), other terminal to GND.

These Energia pin numbers map to the physical header positions on the Launchpad. When wiring, work from the silkscreen labels on the Launchpad board rather than trying to convert P-port notation by hand.

## The sketch

This code intentionally skips the `Ultrasonic.h` library — it's simpler to write the timing logic directly, and the library had some compatibility issues with Energia at the time. The approach: send a trigger pulse, measure the echo duration with `pulseIn()`, convert to inches.

```cpp
const int trigPin = 12;
const int echoPin = 13;
const int speakerPin = 6;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(speakerPin, OUTPUT);
}

void loop() {
  // Send trigger pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure echo duration
  long duration = pulseIn(echoPin, HIGH);

  // Convert to inches: sound travels ~13,500 in/s; round trip = /2
  long distance = duration / 148;

  // Translate distance to tone frequency
  if (distance >= 20 || distance <= 1) {
    noTone(speakerPin);
  } else {
    tone(speakerPin, distance * 40);
  }

  delay(10);
}
```

The frequency formula is `distance * 40` — purely empirical, chosen to keep tones in an audible but not annoying range. At 2 inches you get 80 Hz (low rumble). At 10 inches you get 400 Hz (a clear tone). At 19 inches you get 760 Hz (getting high). Tones outside the 2–19 inch window are silenced with `noTone()`.

The `map()` function would work here too — something like `map(distance, 2, 19, 80, 800)` — and gives you explicit control over the output range. The manual formula is simpler to read at a glance.

## The 10ms delay

The `delay(10)` at the bottom matters. The HC-SR04 can't reliably interpret echoes if the next trigger pulse fires before the previous echo has died out. At 10ms per cycle you're limited to about 100 distance readings per second, which is more than enough for any interactive application. You can push this down to 1ms if you need faster polling, but 10ms is conservative and reliable.

## A note on Energia code size

Energia's compiler produces noticeably larger binaries than writing native MSP430 code in Code Composer Studio. This sketch — a few hundred lines of simple logic — compiled to around 5.5 KB of the MSP430G2553's 16 KB program flash. For a demo or prototype that's fine. If you're pushing against the memory ceiling, native CCS code is meaningfully more efficient. The tradeoff for Energia is obvious: you get Arduino-compatible syntax and the `tone()` function for free.

## What the demo sounds like

The result is a proximity theremin. Move your hand toward the sensor from across the room — the speaker is silent. Get within 19 inches and it starts playing. Move closer, the pitch drops. Touch distance (1 inch and under), silence again. The response is roughly linear since frequency scales linearly with distance.

It's a good proof-of-concept for any application that needs coarse proximity sensing with an audio indicator — alerting when something is too close, or too far, without needing a display.

## References and further reading

- [HC-SR04 datasheet (Elecfreaks)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — trigger pulse requirements, echo timing, and the 2cm–4m range spec
- [Energia IDE](https://energia.nu/) — the Arduino-compatible toolchain for MSP430
- [MSP430G2553 datasheet (TI)](https://www.ti.com/lit/ds/symlink/msp430g2553.pdf) — I/O voltage tolerance spec confirming 5V-tolerant pins on the 3.3V device
- [TI Launchpad MSP430 pin map (Energia)](https://energia.nu/guide/pinmaps/launchpad-msp430g2/) — maps Energia pin numbers to physical header locations
- [Arduino `pulseIn()` reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/pulsein/) — the timing function used for echo measurement; behavior is identical in Energia
- [Arduino `tone()` reference](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) — covers frequency range and the PWM pin requirement
