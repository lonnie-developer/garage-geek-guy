---
title: 'TI-99/4A AV Cable DIY — Build a 5-Pin DIN to Composite Video Adapter'
description: 'Skip the RF modulator. A 5-pin DIN connector, a spare RCA cable, and an hour at the bench gives your TI-99/4A a clean composite video signal into any modern TV.'
pubDate: 'May 03 2018'
youtubeId: 'cItNXffOOTw'
heroImage: '../../assets/posts/ti-99-4a-av-cable-diy/thumbnail.jpg'
tags: ['ti-99-4a', 'retro-computing', 'diy', 'composite-video', 'soldering', 'tutorial']
---

The Texas Instruments TI-99/4A shipped from the factory with a solution to its video output problem that worked perfectly in 1981 and has grown progressively worse ever since. The machine sends its video signal out a 5-pin DIN connector on the back, which in the original setup connects to a TI RF modulator, which converts it to a channel 3 or 4 RF signal, which you then ran through your TV's coax input. In 1981, every TV had a coax input and the RF modulator was a reasonable approach. Today, the RF path is two conversion steps away from the original signal, most modern TVs don't have a coax input without a tuner box, and the image quality that comes out of a forty-year-old RF modulator was never great to begin with.

The alternative is simple and takes under an hour: build a cable that goes directly from the TI-99/4A's 5-pin DIN output to an RCA composite video input, bypassing the modulator entirely. The signal is available on the DIN connector — you just need a cable that correctly maps the pins. The result is a noticeably sharper image and a connection that works directly with any TV that has an AV input.

## A bit of TI-99/4A background

The TI-99/4A was Texas Instruments' entry into the home computer market, introduced in 1981 and discontinued in 1984 after a brutal price war with Commodore. It was the first 16-bit home computer sold to consumers — the TMS9900 processor at its heart was a genuine 16-bit chip, not the 8-bit processors that powered the Apple II, Commodore 64, and Atari 800 of the same era. TI spent enormous resources marketing it and ultimately lost hundreds of millions of dollars on the venture before withdrawing from the home computer market entirely.

Despite that history, the TI-99/4A built a devoted user community that has lasted four decades. Software libraries exist, emulators are mature, and original hardware shows up regularly at estate sales and thrift shops. If you've found one, or pulled one out of a box in an attic, this cable build is step one to getting it working on a contemporary display.

## The 5-pin DIN pinout

The DIN-5 connector on the back of the TI-99/4A carries composite video, audio, and power for the RF modulator. Looking at the back of the connector (the side you solder to, with the pins facing you), the pinout is:

- **Pin 1 (top left):** Audio output (right/mono)
- **Pin 2 (bottom center):** Ground
- **Pin 3 (top right):** Luma (for S-Video, not used here)
- **Pin 4 (center left):** Composite video
- **Pin 5 (center right):** +5V (for the RF modulator — leave unconnected)

For a composite AV cable you need three of these: composite video out to the yellow RCA, audio out to the red RCA, and ground bridged from both ground pins to the cable shield. The white (left audio) RCA connector on a stereo cable is unused — the TI-99/4A outputs mono.

The mapping in plain terms: **red RCA → pin 1, yellow RCA → pin 4, ground → pin 2 and shield combined.** Write that down before you sit down to solder.

## What you'll need

- **5-pin DIN connectors** — male, solder-type. They come in packs of 5 on Amazon or eBay for a few dollars; you'll want at least two in case you mess up the first one
- **An RCA stereo cable** — any one you have lying around works. The shorter the better, since a long cable run can degrade composite video slightly
- **Soldering iron** — any iron that can reach temperature is fine; a Hakko FX-888 or similar with a fine tip makes the work easier
- **63/37 solder** — or whatever you have; leaded solder flows a bit more easily for small work like this
- **Wire strippers** — appropriate for the thin conductors in an RCA cable
- **Diagonal side cutters**
- **Helping hands or a vise** — almost mandatory; you're soldering into tiny cups in an awkward connector with both hands occupied

## Disassembling the DIN connector

The solder-type DIN-5 connector comes in three pieces: the metal shell (housing), a plastic insulator that holds the five pins, and a rear strain-relief clamp. Pull them apart before you do anything else.

**Important: slide the metal housing onto the cable before you solder anything.** This is the "trap for young players" of this build — once you've soldered all three connections, the only way to get the housing over the cable is to desolder everything and start over. Slide the housing on first, then do your soldering with it pushed back out of the way, then slide it forward over the finished joint at the end.

## Prepping the cable

Cut the RCA cable roughly in half, keeping the connectors on one end and leaving a few inches of pigtail on the other. You should have a cable with yellow, red, and white RCA connectors on one end and bare wires on the other.

Strip back the outer jacket to expose a few inches of the individual conductors. Inside you'll find three coaxial mini-cables — each has a center conductor and a braided shield. Strip the end of each coaxial conductor: pull back the braided shield, twist it together, then strip and tin the center conductor. The shield wires from the yellow and red conductors both become ground — twist them together and treat them as one wire.

Cut off the white connector entirely; it's unused.

Tin all three connection points: the yellow center conductor (composite video), the red center conductor (audio), and the combined ground braid. Pre-tinning makes the actual connector soldering much faster.

## Soldering the connector

The five pins on the connector body have small solder cups — they're very short and very close together, which is what makes this connector fiddly to work with. Pre-tin the three cups you'll be using (pins 1, 2, and 4) by flowing a small amount of solder into each one before attaching the wires.

With the connector held steady in your vise or helping hands:

1. Solder the combined ground wire to **pin 2** (bottom center). This is the thickest connection and needs the most heat; do it first so any extra dwell time doesn't cook a neighboring wire.
2. Solder the yellow center conductor (composite video) to **pin 4**.
3. Solder the red center conductor (audio) to **pin 1**.

Keep solder amounts minimal — the cups are small and close, and a solder bridge between pin 1 and pin 2 is an easy mistake. If any joints end up too close for comfort, a small dab of hot glue between them provides insurance against accidental shorts.

## Reassembly and strain relief

Slide the metal housing forward over the connector body. There are notches on the insulator that mate with tabs in the housing — it should click into alignment with a definite seat. Then the strain-relief clamp wraps around the cable where it exits the housing. Crimp the strain relief down firmly — this is what prevents the cable pull stress from going directly to the solder joints.

## Testing

Plug the DIN end into the TI-99/4A's video output port. Connect the yellow RCA to the yellow composite input on your TV and the red RCA to one of the audio inputs. Power up the TI and switch the TV to that AV input.

The image should appear on screen — sharp characters, no RF noise, no tuning required. The TI-99/4A's default screen is solid green with a cursor, which is a useful test pattern for confirming the signal is clean. Audio through the red RCA should come through on the corresponding speaker.

If you get a picture but no audio, check that the red cable is fully seated and that your TV input is set to receive mono audio. If you get no picture, confirm the yellow connector is in composite video input (not component video, which looks similar), and double-check that pin 4 is the one carrying your yellow wire.

## It works for Atari 800 too

The Atari 800 (and several other vintage computers from the early 1980s) used the same 5-pin DIN connector for video output with a compatible pinout. The cable you just built should work for those systems as well, or at minimum require only a minor pin remapping. The composite video approach is the same across most vintage machines of that era — they all needed to get a signal into a television, and a 5-pin DIN was a common connector for the job.

## Where this fits today

If you have a TI-99/4A, this is the cable to make. The RF modulator is a relic; composite video is the baseline for retro computing on modern displays. HDMI upscalers like the RetroTink 2X will take a composite signal and put it on an HDMI display with lag-free upscaling, which is the full modern setup. This cable is step one of that chain.

The cost is a few dollars in parts, the skill required is basic soldering, and the payoff is a noticeably better picture every time you use the machine.

## References and further reading

- [TI-99/4A DIN connector pinout — AtariAge Wiki](https://atariage.com/forums/topic/170418-ti994a-av-cable/) — community-verified pinout documentation
- [TI-99/4A technical reference manual](https://www.ti99.com/exelvision/website/index.php?page=manuals) — original TI documentation archive
- [Classic99 emulator site](http://www.harmlesslion.com/software/Classic99) — for running TI-99/4A software without the hardware
- [TI-99/4A at Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TI-99/4A) — history and hardware overview
- [RetroTink 2X](https://www.retrotink.com/) — takes composite video to HDMI; pairs naturally with this cable for a full modern setup
- [5-pin DIN connectors on Amazon](https://www.amazon.com/s?k=5+pin+din+connector+male) — the connectors you need for this build
