---
title: 'Banggood Arduino UNO Starter Kit and L298N Robot Kit Arrive — New Series Upcoming'
description: 'Banggood sends over an Arduino UNO R3 starter kit and an L298N 2WD ultrasonic robot kit. Unboxing both, plus a channel rebrand: welcome to Garage Geek Guy.'
pubDate: 'September 12 2017'
youtubeId: 'dFWGsB1R8y8'
heroImage: '../../assets/posts/banggood-arduino-l298n-robot-kit-arrival/thumbnail.jpg'
tags: ['arduino', 'robot', 'l298n', 'starter-kit', 'unboxing']
---

A few years' gap in the electronics videos ends here. Banggood reached out and asked me to pick a couple of products from their catalog to review — and if you're going to get back into Arduino, getting back into it with a robot kit and a full starter kit is not a bad way to do it.

Full disclosure up front, the same way it's given in the video: the hardware here was provided by Banggood at no charge, and they gave me no directions on what to say about it. They sent the products, I opened them, and that's the whole arrangement. No payments, no scripted talking points. They asked me to share their links, which I'll do, but the reaction to what's in the boxes is genuine — and the reaction is that for the price, this is a ridiculous amount of hardware.

## The L298N 2WD robot kit

This is the one I was most excited about. The kit shows up in a bag with everything for a two-wheeled Arduino robot: a chassis, two DC motors with wheels, an L298N motor driver board, an Arduino Uno clone, some form of control/sensor connector board, a servo motor (almost certainly for pivoting an ultrasonic sensor to scan left and right), a battery pack, a USB cable, jumper wires, and all the hardware to hold it together.

The price at time of order: $17.07 with free shipping. That number is difficult to contextualize if you've been in hobby electronics for a while. When I first got started with Arduino, a bare Arduino board — just the board, no sensors, no motors, no kit — cost more than that. Getting a complete rolling robot with motors and a motor driver for $17 is a function of how much the Chinese electronics supply chain has matured over the last decade.

The L298N motor driver is the standard dual H-bridge you'll see in most beginner robot tutorials. It handles two DC motors and runs a 5V logic supply off the same motor battery so you don't need a separate power rail for the Arduino. The tradeoff is efficiency — the L298N uses bipolar transistors in its H-bridge, which burn a few volts as heat at typical robot currents. For a first robot it's fine. For a second robot, you might look at the TB6612FNG or DRV8833.

The hardware pack includes a screwdriver, which is either a nice touch or a quiet acknowledgment that most people who buy this kit will not have one handy.

Fourteen days from shipment to arrival in the US, with free shipping from China. That's been my consistent experience with Banggood over several orders — somewhere between ten days and two weeks.

## The Arduino UNO R3 starter kit

The second item is a complete Arduino UNO starter kit, on sale at the time for $29.99 with free shipping. The kit ships in a rigid carry case with optional foam dividers that let you organize components into compartments. The label on the case identifies the brand as "Inferno" — an Arduino clone brand I hadn't encountered before, but clone Unos are clone Unos.

The component list is long. A breadboard and a mini breadboard. An extension/GPIO expansion board. Jumper wires in several varieties. Resistors, LEDs, capacitors, transistors. A 1602 LCD display. An LED segment display. A servo. A stepper motor and driver. Potentiometers. Push buttons. CDS photocells. A 9V battery pack with barrel connector. An IDE ribbon cable-style connector. What looks like a relay module and a real-time clock module. An IR receiver and remote. And an IC chips of various kinds I'd need to actually pull out and identify.

The appeal of this kit for this channel specifically is that it allows for a consistent hardware baseline across tutorial videos. If you pick up the same kit, you'll have the exact same components to work with as what's shown on screen. That solves a persistent problem in Arduino tutorials where the presenter has hardware you can't easily identify or source.

## What's next

Two possible directions for the first series: work through the robot kit (my instinct, and the more visually interesting build) or use the starter kit to revisit some of the introductory Arduino material from earlier in the channel's history, this time with consistent hardware. Either way there's enough in these two boxes to fill several months of videos.

## Links

- [L298N 2WD Ultrasonic Robot Kit on Banggood](https://goo.gl/fPhcQB) — the robot kit from this video
- [Arduino UNO R3 Starter Kit on Banggood](https://goo.gl/w9tcPN) — the starter kit from this video
