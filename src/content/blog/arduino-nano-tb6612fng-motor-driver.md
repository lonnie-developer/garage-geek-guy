---
title: 'Wiring an Arduino Nano and TB6612FNG Motor Driver for a Two-Motor Robot'
description: 'The Toshiba TB6612FNG dual H-bridge is a compact, capable motor driver for Arduino robots. Here is the full 16-pin breakdown, the direction truth table, the standby-pin gotcha that catches almost everyone, and the complete wiring for a two-motor drive system.'
pubDate: 'October 07 2012'
youtubeId: 'lM5IQhhQ_nI'
heroImage: '../../assets/posts/arduino-nano-tb6612fng-motor-driver/thumbnail.jpg'
tags: ['arduino', 'tb6612fng', 'motor-driver', 'robotics', 'robot-build', 'tutorial']
---

The L298N is the motor driver most beginner Arduino robot tutorials reach for first. It works, it's cheap, and there's no shortage of examples. But it has a real limitation: the L298N is a linear H-bridge that dissipates a significant fraction of its input voltage as heat. At 6V, you're losing about 2V across the chip — that's nearly a third of your motor voltage dropped before the current ever reaches the motor windings.

The Toshiba TB6612FNG doesn't have this problem. It's a MOSFET-based dual H-bridge that runs with very low on-resistance, which means almost all of your battery voltage reaches the motors. The chip is physically smaller than the L298N, handles up to 1.2 A continuous per channel (3 A peak), and runs from a 2.5–13.5V motor supply. For a small two-motor drive robot on 4–6 AA batteries, it's a better fit on almost every axis except documentation visibility.

This post covers the full wiring from scratch: the 16-pin layout explained both sides, the direction truth table, the STBY pin gotcha, pin assignments on an Arduino Nano, and all the jumper connections for a Tamiya twin motor gearbox.

> *This build is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

## The TB6612FNG layout

The chip is a 16-pin package oriented so that all motor-side connections are on one side and all microcontroller-side connections are on the other. This makes wiring cleaner than chips that interleave power and logic pins.

**Motor/power side (pins 1–8, working inward):**

| Pin | Name | Purpose |
|-----|------|---------|
| 1 | GND | Chip ground |
| 2 | VCC | Logic supply (2.7–5.5V — connect to 5V from Arduino) |
| 3 | AO1 | Motor A output 1 (one lead of motor A) |
| 4 | AO2 | Motor A output 2 (other lead of motor A) |
| 5 | BO2 | Motor B output 2 |
| 6 | BO1 | Motor B output 1 |
| 7 | VMOT | Motor supply voltage (your battery pack positive) |
| 8 | GND | Motor supply ground |

**Microcontroller side (pins 9–16, continuing):**

| Pin | Name | Purpose |
|-----|------|---------|
| 9 | GND | Ground (can tie to same rail as pin 1 and 8) |
| 10 | PWMA | PWM speed control for motor A |
| 11 | AIN2 | Direction control for motor A |
| 12 | AIN1 | Direction control for motor A |
| 13 | STBY | Standby — must be HIGH for the chip to function |
| 14 | BIN1 | Direction control for motor B |
| 15 | BIN2 | Direction control for motor B |
| 16 | PWMB | PWM speed control for motor B |

Three ground connections (pins 1, 8, and 9) all go to the same place — the common ground rail that ties the Arduino, motor driver, and battery pack together.

## The STBY pin

This is the one that catches nearly every first-time TB6612FNG user. If STBY is LOW (or left floating), the chip produces zero output regardless of what the other pins are doing. The motors don't move, the direction pins do nothing, and everything looks correctly wired from the outside. It's a confusing failure mode.

STBY is a chip-enable input. Pull it HIGH and the chip is active. Pull it LOW and the chip is in low-power standby.

Two ways to handle it:

**Tie it to VCC directly.** Wire STBY to the 5V rail. The chip is always enabled when powered. This is the right choice for most simple robots where you want the motors available at all times.

**Wire it to an Arduino digital pin.** Set it HIGH in code, but now you can disable the motors in software by pulling it LOW without cutting motor power. Useful for more complex control schemes, or if you want a software-controlled "motors off" state distinct from powering everything down.

This build ties STBY directly to VCC.

## Direction control — the truth table

AIN1, AIN2, BIN1, and BIN2 control which direction each motor turns. The relationship follows a straightforward truth table:

| AIN1 | AIN2 | Motor A |
|------|------|---------|
| HIGH | LOW  | Forward |
| LOW  | HIGH | Reverse |
| LOW  | LOW  | Coast (free-spin) |
| HIGH | HIGH | Brake (short both leads) |

Same logic applies to BIN1/BIN2 and motor B.

For a differential-drive robot going straight forward: AIN1 HIGH, AIN2 LOW, BIN1 HIGH, BIN2 LOW.

For a left turn (assuming motors are mirrored left/right): one side forward, one side reverse. Work out which motor needs to spin which direction on your specific chassis — it depends on how the motors are physically oriented.

## PWM speed control

PWMA and PWMB accept a PWM signal that controls motor speed — 0% duty cycle is stopped, 100% is full speed. On the Arduino, use `analogWrite()` to generate the PWM signal. The key constraint: PWMA and PWMB must connect to PWM-capable Arduino pins.

On the Arduino Uno and Nano, the PWM-capable pins are D3, D5, D6, D9, D10, and D11 — the ones marked with a tilde (~) on the board. Using any other digital pin for PWMA or PWMB will give you only on/off control with no speed variation.

The pin assignments used in this build:
- **PWMA → D10**
- **PWMB → D11**
- **AIN1 → D6, AIN2 → D7**
- **BIN1 → D8, BIN2 → D9**

The direction pins (D6–D9) are grouped in a clean sequential row, which makes the wiring visually tidy on the breadboard and makes the code slightly easier to read.

## Power wiring

This build uses a 4×AA battery pack — about 6V — for both the motors and the Arduino Nano. Six volts is within the Arduino Nano's Vin input range (7–12V is ideal, but 6V works) and is below the Tamiya motors' 3–9V spec, so this is a practical compromise.

Important: the grounds for the battery pack, the motor driver, and the Arduino must all connect to the same node. This common ground is what lets the direction signals from the Arduino (referenced to Arduino GND) be correctly interpreted by the motor driver (referenced to its own GND). Separate grounds between the Arduino and motor driver are a common source of unpredictable behavior.

The wiring order that avoids confusion:
1. Connect battery pack GND to the breadboard ground rail
2. Connect battery pack positive to VMOT (pin 7)
3. Connect Arduino GND to the same ground rail
4. Connect Arduino 5V to VCC (pin 2) and STBY (pin 13)
5. Wire motor leads to AO1/AO2 and BO1/BO2
6. Wire direction and PWM pins from Arduino to the chip

## The motor lead polarity question

Which motor lead goes to AO1 vs AO2 affects which direction "forward" code produces actual forward motion. There's no wrong answer at wiring time — just note which way the motor turns when AIN1=HIGH, AIN2=LOW, and adjust your "forward" assignments in code if needed. On a two-motor differential robot, you'll likely need to flip one motor's leads anyway because the motors face opposite directions on the chassis.

## Code sketch (minimal test)

```cpp
// Pin definitions
const int PWMA = 10, AIN1 = 6, AIN2 = 7;
const int PWMB = 11, BIN1 = 8, BIN2 = 9;

void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT);
  pinMode(PWMA, OUTPUT); pinMode(PWMB, OUTPUT);
}

void forward(int speed) {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW);
  analogWrite(PWMA, speed);
  analogWrite(PWMB, speed);
}

void loop() {
  forward(180);   // about 70% speed
  delay(2000);
  analogWrite(PWMA, 0);  // coast
  analogWrite(PWMB, 0);
  delay(1000);
}
```

## References and further reading

- [TB6612FNG datasheet (Toshiba)](https://toshiba.semicon-storage.com/info/TB6612FNG_datasheet_en_20141001.pdf) — the source for the pin descriptions, electrical specs, and the complete truth table; the absolute-maximum ratings section tells you what the chip can actually survive
- [SparkFun TB6612FNG breakout hookup guide](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide) — well-illustrated wiring guide using the SparkFun breakout module, which exposes the same chip
- [Tamiya twin motor gearbox assembly guide](https://www.tamiyausa.com/shop/educational-construction/twin-motor-gearbox-kit/) — if you're using the Tamiya gearbox, motor lead polarity and shaft speed specs are in here
- [Arduino `analogWrite()` reference](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/) — PWM on Arduino; the pin list for PWM-capable outputs is here
- [L298N vs TB6612FNG comparison](https://lastminuteengineers.com/tb6612fng-dc-motor-driver-arduino-tutorial/) — Last Minute Engineers' tutorial covers the efficiency difference in useful detail
- [Adafruit TB6612FNG breakout](https://www.adafruit.com/product/2448) — Adafruit's module version; the product page has a wiring diagram and library
