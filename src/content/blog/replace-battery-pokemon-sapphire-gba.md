---
title: 'How to Replace the Battery in Pokémon Sapphire (Game Boy Advance)'
description: 'When the CR1616 battery dies in a GBA Pokémon game, the real-time clock stops — but your save data is safe. Here is how to replace it, what battery to use, and why size actually matters here.'
pubDate: 'October 22 2014'
youtubeId: 'Tg-i-uZ74xg'
heroImage: '../../assets/posts/replace-battery-pokemon-sapphire-gba/thumbnail.jpg'
tags: ['pokemon', 'game-boy', 'retro-gaming', 'battery', 'repair']
---

*This build is from 2014, when the channel was still MeanPC.com — same Lonnie, same garage, same workbench.*

I picked up Pokémon Gold and Pokémon Sapphire for $10 total — the reason they were cheap being that the batteries in both were dead. That's a perfectly good reason to get a deal on retro games, because the fix is straightforward and the parts cost almost nothing.

This post covers the Sapphire repair specifically. Gold is a different generation with different stakes around the battery — I'll get to that below.

## What the battery actually does (and doesn't do)

This is the thing that trips people up. In GBA-era Pokémon games — Ruby, Sapphire, Emerald — the internal battery powers the Real Time Clock (RTC). It does not power the save file.

When the battery dies, your save data is completely safe. The game saves to Flash memory, which retains data without any power source. What stops working is anything tied to the in-game clock: berry growth, tidal events in Shoal Cave, and other time-based mechanics. The game gives you a message on startup — "The internal battery has run dry. The game can be played. However, clock-based events will no longer occur" — which is the game's polite way of telling you the RTC is dead.

Once you replace the battery, you're back to normal. Save intact, clock ticking again.

(Pokémon Gold is different: that's a Game Boy Color cartridge, and the battery there also backs the save RAM. When that one dies, you can still play, but you can't save at all. The stakes are higher. Handle that one carefully.)

## The battery: what to use

The original battery in Pokémon Sapphire is a **CR1616** — a coin cell that's smaller in diameter than the more common CR2032 and slightly thinner than a CR2025. At the time of filming, I had CR2025s on hand and used one of those instead. It works, but the case closes with a slight gap because the CR2025 is physically larger. It's not loose — the cartridge shell holds it in place — but it's not quite right either.

My recommendation: **use a CR1616**. It's the correct size, the case will close cleanly, and the contact tension will be what the board was designed for. CR1616s are available at any drugstore or hardware store for under $5, or in multipacks online.

The expected battery life for the RTC in these games is roughly 10 years from new — so a fresh CR1616 today should see you well into the 2030s.

## What you'll need

- CR1616 battery (or CR2025 in a pinch — it works, just oversized)
- Small flathead precision screwdriver, or a tri-wing screwdriver if you have one
- Soldering iron and solder (for a solid connection — you can get away without it but it's not ideal)
- Needle-nose pliers for bending the battery terminal

## The repair

**Opening the cartridge.** The single screw on the back of the cartridge is a tri-wing — Nintendo's way of discouraging casual disassembly. A tri-wing screwdriver is the right tool. I don't own one, so I used a small flathead precision screwdriver instead and it worked fine. Once the screw is out, the back shell slides upward and lifts off, and the PCB can fall out at that point if you're not careful — catch it.

**The battery.** On the PCB you'll see the coin cell held by two metal terminals — a negative contact on top and a positive one below. The original battery is soldered to those terminals. Desolder or carefully bend them away to free the old cell.

**Fitting the new one.** Put a slight bend in the positive terminal so it'll make firm contact with the bottom of the new battery. Slide the new battery in — negative side facing up (the top of the battery, the marked side, faces the negative terminal). The positive terminal should press against the bottom of the cell.

If you can get a solder joint on the terminal, do it. The connection will be more reliable. I had a frustrating time getting the solder to take because I was working against a dissimilar metal surface, but eventually got a workable joint with sustained heat and pressure. If soldering proves impossible (it happens), bend the terminal so there's spring tension against the battery — the pressure from the closed case will maintain the contact.

**Closing up.** Slide the PCB back in, line up the back shell, and replace the screw. Don't overtighten — it's just a plastic shell with a small tri-wing screw. Snug is enough.

**Testing.** Pop it into a DS or DS Lite (which can play GBA cartridges) and boot it. If you no longer see the "internal battery run dry" message, the clock is running. You're done.

## After the repair: resetting the RTC

Replacing the battery starts the clock from zero, but your save game remembers what "day" it was when the battery died. This means clock-based events might still not trigger correctly even after the repair — the game's internal RTC start time is out of sync with the new clock reading.

The fix involves resetting the RTC reference point in the save data, which requires either a GameShark/Action Replay code or a tool like PKHeX with a flashcart or dumped save. It's an extra step, but it's well-documented in the GBA modding community if you want the clock events fully restored.

## References and further reading

- [Instructables: Pokémon Sapphire battery replacement](https://www.instructables.com/Pokemon-Sapphire-Battery-Replacement/)
- [ConsoleMods Wiki: GBA Real Time Clock fix](https://consolemods.org/wiki/GBA:Real_Time_Clock_(RTC)_Fix)
- [GBAtemp: resetting RTC after battery replacement](https://gbatemp.net/threads/how-to-reset-the-rtc-in-gba-pokemon-games-after-replacing-the-battery.558620/)
- [2Bluebox: Game Boy battery replacement guide](https://2bluebox.com/blogs/retro-tech-lab/game-boy-battery-replacement-guide)
- [Bulbapedia: Berry glitch (related RTC context)](https://bulbapedia.bulbagarden.net/wiki/Berry_glitch)
- [GBAtemp: Ruby/Sapphire/Emerald after battery replacement](https://gbatemp.net/threads/ruby-sapphire-emerald-batteries-changed-what-now.578880/)
