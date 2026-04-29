---
title: 'I Bought the Elm Eco Pro 2 Key Card Hack — and It Works'
description: 'The Elm Eco Pro 2 disc resurfacing machine runs on proprietary timed key cards that expire after 800 minutes. A UK modder built a small microcontroller hack that gives you unlimited time for $138.'
pubDate: 'January 21 2024'
youtubeId: '6ywFIZZM5SA'
heroImage: '../../assets/posts/elm-eco-pro2-key-card-hack/thumbnail.jpg'
tags: ['disc-repair', 'hardware-hack', 'diy', 'review']
---

There's a business model hiding inside a lot of professional equipment: sell the machine at a reasonable price, then lock the consumables. Razor blades, printer ink, coffee pods. The Elm Eco Pro 2 disc resurfacing machine runs a variation of this — it uses proprietary key cards that expire after 800 minutes, at which point you buy another one from ELM USA and keep going.

That's fine when the machine is new and busy. It gets less fine after a few years when you're resurfacing discs occasionally and watching the minute counter tick down on a card you've had to order twice already. So when I heard someone in the UK was making an unlimited mod for it, I paid attention.

## What the Elm Eco Pro 2 is

The Eco Pro 2 is a professional-grade disc resurfacing machine — it buffs and polishes scratched CDs, DVDs, and Blu-rays back to playability. It's a step above the consumer disc repair kits you'd see at a GameStop counter. The machine dispenses a precise amount of compound, spins the disc against a resurfacing pad, and tracks cumulative use through the key card system.

The key card does two things: it unlocks the machine and it acts as the usage meter. No card, no run. Expired card, buy a new one. ELM USA sells them in 800-minute packs — their [ECO Pro 800 Minute Supply Kit](https://www.elm-usa.com/products/single-800-minute-pack) includes compound and a fresh card. If you're doing volume work, those consumable costs add up.

## The mod

I found out about this through a YouTube video by a UK creator named Darren — the original is [on his channel here](https://www.youtube.com/watch?v=VjUoeEufbRQ). He's built a small plug-and-play device: there's what looks like a little microcontroller inside, a short cable that connects between the mod and the machine's key card slot, and a button on the side. The device tricks the machine into thinking a valid key card with unlimited time is present.

I reached out to Darren via his YouTube video, paid $138 shipped from the UK, and it showed up in about five days. The package included the mod itself, the connecting cable, a power cord for the mod, and instructions.

## The install

The process is exactly as straightforward as it looks:

1. Plug the USB connector into the mod, plug the other end into a USB power supply.
2. Take a fresh new key card and insert it into the mod's slot, sticker side down.
3. Press the reset button on the side of the mod.
4. Power on the Eco Pro 2 — it'll show no key card detected, which is fine.
5. Plug the mod's key card connector into the machine.
6. Power cycle the Eco Pro 2.

After the power cycle, my machine showed 800 minutes. The instructions said to remove the key card from the mod at that point, which I did. I ran a short cycle — the machine worked fine, completely without the physical key card present. The mod is doing the talking now.

I went ahead and burned through a couple of minutes just to get off 800 and verify it was counting down normally. It was. One button press and the machine is back to 800 minutes whenever I need it.

## What's actually in the mod

I haven't cracked it open, but based on the behavior — read the card once during setup, then emulate it indefinitely — it's almost certainly a small microcontroller that captures and replays the key card protocol. The card format isn't encrypted in any sophisticated way, which is probably why this was a fairly tractable reverse engineering project. The reset button presumably reloads the emulated time value back to 800.

## A note on warranty

Almost certainly voids it. ELM USA's terms reserve the right to deny support for machines running unauthorized components, which this technically is. If you're running a commercial shop and your machine is still under warranty, that's worth factoring in. If you've had the machine for a few years and the warranty is long gone, the math looks different.

The machine itself doesn't know anything's wrong — it just sees what it believes is a valid key card. Nothing about the resurfacing mechanism is being modified or bypassed.

## The bottom line

$138 is a real number. It's also roughly what a single replacement key card kit costs, so if you're looking at two or three more card purchases over the life of the machine anyway, it pays off quickly. The install took about two minutes. It works exactly as advertised — I've had mine for nearly four years at this point.

If you're interested, Darren's contact info (potman100@gmail.com) and the original demo video are linked in the description of the video above. He ships to the US and turnaround is fast.

## References and further reading

- [ELM USA — Key Card instructions](https://www.elm-usa.com/pages/ecopro2instruction-manual-5usingthekeycard)
- [ELM USA — Supplies explained](https://www.elm-usa.com/pages/supplies-explained)
- [Darren's original unlimited mod demo](https://www.youtube.com/watch?v=VjUoeEufbRQ)
- [ECO Pro 2 Operation Manual (PDF)](https://m.discmagic.net/f/ELM-USA_ECOPro2__Manual_V8.1.15.pdf)
