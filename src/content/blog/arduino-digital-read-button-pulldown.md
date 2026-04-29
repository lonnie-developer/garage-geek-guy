---
title: 'How to Use a Button with Arduino — digitalRead() and the Pull-Down Resistor'
description: 'Reading a button with Arduino requires more than just wiring it to a pin. This post covers the floating-pin problem, why a 10kΩ pull-down resistor fixes it, and the complete wiring and code for a button-controlled LED.'
pubDate: 'November 07 2018'
youtubeId: 'yAWaj76VDiQ'
heroImage: '../../assets/posts/arduino-digital-read-button-pulldown/thumbnail.jpg'
tags: ['arduino', 'button', 'digitalread', 'pull-down-resistor', 'beginner', 'tutorial']
---

A button seems like the simplest possible input. It's either pressed or it isn't. Two states, a digital device, should be a one-wire connection.

It's not quite that simple. An Arduino input pin left unconnected — or connected only to the button with nothing else — doesn't reliably read LOW when the button is open. It floats. The pin picks up electrical noise from nearby traces, radio interference, your hand moving near the breadboard, capacitive coupling from adjacent wires. What you read is garbage: random HIGH and LOW transitions with no button press involved.

The fix is a pull-down resistor, and understanding why it works is worth the two minutes it takes.

## The floating pin problem

When you `pinMode(2, INPUT)` and then call `digitalRead(2)`, you're asking the Arduino what voltage it sees on pin 2. Digital read will return HIGH if that voltage is above ~3V and LOW if it's below ~1.5V. Anything in between is undefined.

If pin 2 isn't connected to anything, there's no voltage reference at all. The pin is connected only to the trace running to it and a tiny internal transistor that's high-impedance when set to input mode. With no reference, the pin voltage drifts based on electromagnetic conditions in the surrounding environment. That's the float — and it means `digitalRead()` returns arbitrary results that have nothing to do with your button.

You need to ensure the pin reads a known, stable voltage when the button isn't pressed. That's what a pull-down resistor does.

## How the pull-down resistor works

Wire the circuit like this: one leg of the button goes to 5V. The other leg connects both to Arduino digital pin 2 *and* through a 10kΩ resistor to GND.

```
5V ─── [button] ─── Pin 2 ─── 10kΩ ─── GND
```

When the button is **open**: the 10kΩ resistor pulls pin 2 to GND. No current flows through the button. The pin reads LOW. Stable and predictable.

When the button is **closed**: 5V is now connected directly to pin 2. The 5V flows into pin 2 (registering HIGH) and also flows through the 10kΩ resistor to GND. The resistor limits that current to 0.5mA — small enough to not matter, large enough to ensure the pin reads 5V and not some intermediate float.

The reason you need the 10kΩ resistor even when the button is closed is to prevent a dead short between 5V and GND through the button. Without the resistor, closing the button would connect 5V directly to GND with nothing in between. That trips the Arduino's overcurrent protection at best and damages something at worst. The 10kΩ puts enough resistance in the path that the short can't happen, while still making the pull-to-ground path high enough resistance that the 5V from the button dominates at the input pin.

## What you'll need

- Arduino Uno
- Small tactile pushbutton (the standard through-hole kind, very common)
- 10kΩ resistor (brown-black-orange)
- LED
- 150Ω resistor (brown-green-brown) for the LED
- Breadboard and jumper wires

The tactile buttons commonly sold for Arduino projects are four-legged — the legs connect in pairs. Looking at the button from above, the two legs on the left are connected to each other, and the two legs on the right are connected to each other. The button makes contact between left pair and right pair when you press it. Orient accordingly.

## Wiring

**Button:**
- One leg → 5V on the Arduino
- Other leg → Arduino digital pin 2
- That same other leg → through a 10kΩ resistor → GND

**LED:**
- Long leg (anode) → Arduino digital pin 12
- Short leg (cathode) → through a 150Ω resistor → GND

```
Arduino 5V   ──── [button leg 1]
                  [button leg 2] ──── Arduino Pin 2
                                └─── 10kΩ ──── Arduino GND

Arduino Pin 12 ──── [LED long leg]
                    [LED short leg] ──── 150Ω ──── Arduino GND
```

## The code

The Arduino IDE includes a Button example sketch under File → Examples → Digital → Button. It's worth loading because it's clean and well-commented. The only change needed for this wiring is pin 13 → pin 12 for the LED.

```cpp
const int buttonPin = 2;
const int ledPin = 12;

int buttonState = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}
```

`digitalRead(buttonPin)` returns `HIGH` when the button is pressed (5V is on pin 2) and `LOW` when it's released (pin 2 is pulled down to GND through the 10kΩ). The `if` statement lights the LED when the button is high and turns it off when it's low. Upload, press the button, LED lights. Release, LED goes off.

## The alternative: INPUT_PULLUP

The Arduino Uno has internal pull-up resistors built into every I/O pin — roughly 20–50kΩ connected between the pin and 5V. You can activate them in software without any external components:

```cpp
pinMode(buttonPin, INPUT_PULLUP);
```

With `INPUT_PULLUP`, the internal resistor pulls the pin HIGH by default. Your button wiring flips: connect one leg to GND and the other leg to the input pin. Pressing the button pulls the pin to GND, reading LOW. Releasing it returns to the internal pull-up HIGH.

The logic is inverted compared to the pull-down circuit — LOW means pressed, HIGH means not pressed — so your code checks `buttonState == LOW` instead of `buttonState == HIGH`. Otherwise identical.

Internal pull-up is fine for most projects and saves external components. The pull-down external resistor is worth knowing separately because not every microcontroller has internal pull-ups (some only have pull-ups, no pull-downs), and because understanding the external circuit makes the concept stick in a way that `INPUT_PULLUP` as magic incantation doesn't.

## What this post doesn't cover: debouncing

Mechanical buttons bounce. When you press a button, the physical contacts don't close once cleanly — they make and break contact several times in the first few milliseconds before settling. At Arduino CPU speeds, those bounces are fast enough to register as multiple presses. For a simple LED toggle that's invisible. For counting presses or triggering a state change, it produces maddening results.

The fix is debouncing — either in hardware (small capacitor across the button contacts) or in software (ignore additional state changes for 10–50ms after the first one). The Arduino IDE includes a Debounce example under File → Examples → Digital → Debounce that walks through the software approach. That's worth reading when you hit the problem.

## References and further reading

- [Arduino Reference — digitalRead()](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/) — official function documentation
- [Arduino Reference — pinMode()](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/) — covers INPUT, OUTPUT, and INPUT_PULLUP modes
- [SparkFun: Pull-Up Resistors](https://learn.sparkfun.com/tutorials/pull-up-resistors/all) — the best plain-language explanation of pull-up and pull-down resistors I've seen
- [Programming Electronics Academy: Floating Pins and Pull-Up Resistors](https://www.programmingelectronics.com/floating-pins-pull-up-resistors-and-arduino/) — covers the physics of why floating pins float
- [Arduino Tutorial — Button](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button) — the official example this post is based on, with circuit diagram
- [Arduino Tutorial — Debounce](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Debounce) — the logical next step after this one
- [Robotics Back-End: INPUT_PULLUP Explained](https://roboticsbackend.com/arduino-input_pullup-pinmode/) — detailed breakdown of the internal pull-up option
