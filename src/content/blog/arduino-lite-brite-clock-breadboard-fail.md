---
title: 'Arduino Lite Brite Clock: Why 22-Gauge Wire Fails in Breadboards (and the Perfboard Fix)'
description: 'A short but useful detour — discovering that 22 AWG solid-core wire sits too loosely in standard breadboard sockets to be reliable, and why the Lite Brite Clock matrix connections need to move to soldered perfboard instead.'
pubDate: 'July 29 2012'
youtubeId: 'jsWGvqNl6pU'
heroImage: '../../assets/posts/arduino-lite-brite-clock-breadboard-fail/thumbnail.jpg'
tags: ['arduino', 'led', 'breadboard', 'perfboard', 'lite-brite', 'clock', 'project']
---

*This project is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

This is part of the Arduino Lite Brite Clock build series. The [previous episode](/blog/arduino-lite-brite-clock-testing-leds) covers LED testing and polarity.

---

Not every episode of a build goes forward. This one is a short step sideways — but the lesson it demonstrates is one that saves headaches on a lot of projects, not just this one.

## The wire problem

The plan going into this episode was to run the common anode connections through the breadboard: bring all the anode leads for each row together, pass them through a breadboard column (with the current-limiting resistors on the same board), and route outgoing wires from there to the Arduino.

The problem is 22 AWG solid-core hookup wire. Standard breadboard sockets are designed for leads and wires in the 20–22 AWG range, but 22 AWG is at the thin end of that tolerance, and in practice many breadboards — especially the inexpensive ones common in hobbyist kits — have contact springs that are sized to grip 20 AWG snugly and only barely hold 22 AWG. The result: wires that seat loosely, make intermittent contact, and shift when you breathe on them. For a one-off test circuit that you're actively monitoring, this is annoying. For a completed clock that you want to put in a Lite Brite housing and have run reliably for months, it's not acceptable.

## The fix: perfboard

The solution is straightforward — move the matrix connections off the breadboard and onto perfboard, where every connection is soldered and stays put. The anode resistors are already on perfboard from an earlier episode. The same approach applies to all the other connections that need to be permanent: solder them onto pads, run wires to the Arduino from there, and don't rely on friction contacts inside a breadboard socket for anything that needs to be reliable.

This isn't a criticism of breadboards — they're the right tool for exploratory prototyping, where you're trying things out and changing them frequently. Once you know what goes where and it needs to stay put, soldered connections on perfboard (or a custom PCB if volume justifies it) are the next step.

## What gets moved

The connections that are being promoted from breadboard to soldered perfboard:

- The five common anode row wires (one per row of the LED grid)
- The twelve cathode column wires, which will connect via the anode resistor board already on perfboard

The Arduino connections themselves will still be jumper wires — the Arduino headers accept the same 22 AWG wire, but the connector is tighter and more positive than a breadboard socket, so it holds adequately.

## A note on the soldering iron

The transcript from this episode also includes a recurring complaint about the soldering iron — a basic iron with no temperature indicator and no adjustability. You can't tell if it's on or off without touching something to it, which means it either gets left on (wasting energy, fire hazard) or you have to wait for it to heat up each time.

A temperature-controlled soldering station is not a luxury on a project like this. When you're making dozens of small joints in close proximity to each other — with anode and cathode leads sitting only a millimeter or two apart — the difference between "hot enough to flow solder cleanly" and "too hot, wicking solder onto adjacent leads" matters. A station with an adjustable setpoint and a visible ready indicator is a meaningful quality-of-life improvement and pays for itself in salvaged time fairly quickly.

## What's next

With the breadboard abandoned in favor of soldered perfboard connections, the next step is the anode column wiring — running hookup wire across each column of LED anodes, soldering the connections, and testing for shorts before closing anything up. That's covered in the [anode columns post](/blog/arduino-lite-brite-clock-solder-anode-columns).
