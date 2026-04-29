---
title: 'Arduino digitalWrite on All 20 Pins — Including the Analog Ones'
description: 'Every I/O pin on an Arduino Uno can be used as a digital output, including the six analog pins. Here is how to address all 20 at once with a for loop, why analogRead pins double as digital pins, and a chasing-LED demo that uses every pin on the board.'
pubDate: 'November 02 2018'
youtubeId: 'nktHeoqXhHU'
heroImage: '../../assets/posts/arduino-digital-write-all-pins/thumbnail.jpg'
tags: ['arduino', 'digital-write', 'tutorial', 'beginner', 'leds', 'pins']
---

Something that trips up a lot of newcomers to Arduino: the six pins labeled A0 through A5 on the Uno are not exclusively analog. They're analog-capable, meaning they have analog-to-digital converter (ADC) connections on those pins, but they can be used as standard digital inputs and outputs too — the same `pinMode()`, `digitalWrite()`, and `digitalRead()` functions work on them exactly as they do on the numbered digital pins.

This means an Arduino Uno has 20 usable general-purpose I/O pins, not 14. And they can all be driven by a for loop.

This post wires 20 LEDs to all 20 pins, writes the code to chase them in sequence, and uses that setup to explain a few fundamental Arduino concepts: program structure, `for` loops in `setup()`, and how the analog pins fit into the numbering scheme.

## The hardware

Twenty LEDs, all with their cathodes (short leg, flat side) connected to a common ground rail on the breadboard. That rail connects to one of the GND pins on the Arduino. Each anode (long leg) connects through a 220Ω current-limiting resistor to one Arduino pin.

The 220Ω value gives about 12 mA through each LED at 5V minus a typical 2V forward drop — well within the 40 mA per-pin limit of the ATmega328P, and well below the 200 mA total current limit across all I/O pins simultaneously.

Pins D0 through D13 fill the 14 digital slots. Then A0 through A5 get the remaining 6 LEDs.

## Addressing the analog pins as digital outputs

In code, you can refer to A0–A5 two different ways:

**By name:** `A0`, `A1`, `A2`, `A3`, `A4`, `A5` — the Arduino IDE defines these as constants.

**By number:** `A0` is pin 14, `A1` is pin 15, continuing to `A5` as pin 19 (zero-indexed from the bottom of the pin numbering).

Both are equivalent. `pinMode(A0, OUTPUT)` and `pinMode(14, OUTPUT)` do the same thing. The numeric form is what makes a for loop possible over all 20 pins:

```cpp
void setup() {
  for (int i = 0; i <= 19; i++) {
    pinMode(i, OUTPUT);
  }
}
```

This runs `pinMode(0, OUTPUT)` through `pinMode(19, OUTPUT)` — all 20 pins set as outputs in four lines instead of twenty. The for loop in `setup()` is a clean pattern worth knowing: `setup()` runs once, and a for loop in setup just means that one-time initialization happens to iterate, which is perfectly valid.

## The chase sketch

```cpp
void setup() {
  for (int i = 0; i <= 19; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  int wait = 9;  // milliseconds per LED — change this to adjust speed

  // Forward pass: 0 → 19
  for (int i = 0; i <= 19; i++) {
    digitalWrite(i, HIGH);
    delay(wait);
    digitalWrite(i, LOW);
  }

  // Reverse pass: 19 → 0
  for (int i = 19; i >= 0; i--) {
    digitalWrite(i, HIGH);
    delay(wait);
    digitalWrite(i, LOW);
  }
}
```

The `wait` variable at the top of `loop()` is worth highlighting as a practice. The delay value is used in two places. By declaring it as a variable once instead of hardcoding the number in both for loops, you only need to change one line when experimenting with speeds — and the code becomes self-documenting. At 9 ms, each LED lights for 9 ms before handing off to the next, giving a smooth-looking scan across 20 LEDs.

The forward and reverse passes together make the classic Knight Rider/Larson Scanner effect: lights appear to bounce back and forth.

## Speed experiments

At 9 ms the chase effect is clearly visible. Raise it to 20 ms and the individual LEDs become obviously distinct and the scan feels slow. Drop it toward 5 ms and the motion starts to blur. At 1 ms per LED the pattern is still technically running, but persistence of vision makes it look like all LEDs are on at half brightness — you're updating 20 LEDs in 20 ms, which is 50 Hz, and that's fast enough for your eyes to average.

At 0 ms delay the loop runs as fast as the Arduino can execute it. The LEDs now turn on and off so quickly that they appear uniformly lit — human vision can't track individual 100-microsecond on/off events. Commenting out the `LOW` line and just setting everything HIGH looks noticeably brighter than the 0ms delay version, which demonstrates that even "instantaneous" code execution leaves each LED off for most of the duty cycle.

This kind of hands-on speed experiment is a good way to build intuition for how `delay()` relates to apparent behavior, and how persistence of vision affects what LED patterns look like in practice.

## A note on D0 and D1

This sketch includes D0 (RX) and D1 (TX) in the pin loop. The sketch uploads and runs fine — nothing catastrophic happens — but there's a caveat: these pins are connected to the Arduino's USB serial interface. While the Arduino is uploading a sketch over USB, D0 and D1 need to be free to communicate. If you have LEDs or other hardware connected to those pins during upload, you may see intermittent upload failures or the LED state may interfere with serial communication during debugging.

The safe practice: leave D0 and D1 unconnected if you're using serial (`Serial.begin()`) for any reason, or expect to re-upload sketches regularly. For a final demo circuit with no serial and no re-uploading needed, wiring them is fine.

## When this matters beyond the demo

The practical takeaway from this sketch isn't that you should wire 20 LEDs to your Arduino — it's that the analog pins are available as extra digital I/O when you need them. If you're building a keypad matrix, a segment display driver, or a sensor array and you're running short on digital pins, A0–A5 are available. You don't need to switch to a Mega just because you used up D2–D13.

The for-loop initialization pattern is also useful beyond the LED demo. Driving a shift register, initializing a pin bank for a button matrix, or clearing a group of outputs in a tidy way — the for loop approach keeps the setup function readable regardless of how many pins are involved.

## References and further reading

- [Arduino digital pins reference](https://www.arduino.cc/en/Tutorial/Foundations/DigitalPins) — official docs covering input/output modes, current limits, and the hardware serial caveats for D0/D1
- [Arduino `analogRead()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) — explains the 10-bit ADC on A0–A5 and the dual-use with digital I/O
- [ATmega328P datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf) — the source for the 40 mA per-pin and 200 mA total I/O current limits (Section 29: Electrical Characteristics)
- [Arduino `for` loop reference](https://www.arduino.cc/reference/en/language/structure/control-structure/for/) — includes examples of for loops in both setup and loop contexts
- [Persistence of vision explained](https://en.wikipedia.org/wiki/Persistence_of_vision) — why fast-flashing LEDs appear continuously lit; explains the 0ms delay behavior observed in this sketch
- [Arduino Uno pinout diagram](https://content.arduino.cc/assets/Pinout-UNOrev3_latest.pdf) — the official pin reference; shows the PWM-capable pins (~) and the ADC-capable analog pins in context
