---
title: 'How Much Electricity Does a 3D Printer Actually Use?'
description: 'A watt meter and a calibration cube answer the question properly. The Anycubic Mega S draws up to 225W while heating, drops to 40–50W while printing, and costs about 2 cents per hour to run — less than most people guess.'
pubDate: 'June 03 2022'
youtubeId: 'SNV_c2XnL2k'
heroImage: '../../assets/posts/how-much-electricity-3d-printer/thumbnail.jpg'
tags: ['3d-printing', 'electricity', 'power', 'anycubic', 'workshop', 'tutorial']
---

The answers floating around forums range from "50 watts" to "500 watts," which is a ten-to-one spread and not particularly helpful if you're trying to figure out whether your workshop circuit can handle three printers running simultaneously. The honest answer requires a watt meter and an actual test, so here's one: the Anycubic Mega S measured at the wall across a complete calibration cube print.

## The test setup

The meter used here is a plug-in watt meter of the Kill-A-Watt type — it goes between the printer's power cord and the outlet, and shows real-time wattage, cumulative kilowatt-hours, amps, voltage, and running cost. These meters cost around $15–20 and are worth keeping in the shop. The cost per kWh was set to $0.15 for this test, which is close to the U.S. national average; your actual rate is on your utility bill and will vary.

The printer is the Anycubic Mega S, a bed-slinger with a heated bed (up to 110°C) and a direct-drive extruder running PLA at 200°C. The test print is a 5-gram calibration cube sliced at 0.2mm layer height, standard resolution.

## What the numbers showed

**Idle (printer on, not printing):** ~7W — just the power supply fan, the motherboard, and the display. Essentially nothing.

**Heating phase (bed and hotend coming up to temperature):** 180–220W. This is the peak draw. Both heaters running simultaneously is what pulls maximum wattage. The heated bed is the dominant consumer here — it heats a large aluminum plate and is the main reason modern FDM printers draw significantly more than their predecessors.

**While printing (after reaching temperature):** the draw cycles. When just the hotend and stepper motors are running, it drops to around 40–50W. Whenever the heated bed cycles on to maintain temperature, it spikes back to 200–220W. The average over a full print is somewhere in between.

**Final results for one calibration cube:** 41 minutes, 0.071 kWh consumed, cost = 1 cent.

That 0.071 kWh over 41 minutes works out to roughly 104W average, which is consistent with the observed cycle between 40–50W and 200–220W during printing.

## The circuit capacity question

The real-world application of this data: how many printers can you run on one circuit without tripping a breaker?

A standard 15A circuit at 120V has a theoretical maximum of 1,800W. The practical safe continuous load is 80% of that — 1,440W — because breakers are rated for intermittent loads and running sustained close to the limit causes nuisance trips and heat buildup in wiring.

At a maximum draw of ~225W per printer, the math:

- 1 printer: 225W — no issue
- 3 printers: 675W — comfortable
- 6 printers at simultaneous max: 1,350W + ~200W for other workshop load (computer, lighting) = ~1,550W — right at the safe continuous limit

In practice, printers don't all heat simultaneously, and the heated bed cycles rather than running constant, so 6 printers on a 15A circuit is probably workable. More than that and a second circuit starts making sense.

## What the heated bed actually costs

The heated bed is responsible for roughly 75% of a printer's peak draw. Without it, the hotend heating only pulls about 54W. This was tested with a no-bed-heat reslice of the same calibration cube — the hotend heated to 200°C in that run, and the meter showed 54W during the hotend-only warm-up.

The practical catch: without a heated bed, PLA often lifts off the build surface, particularly on larger prints. The no-bed test print here lifted and failed. The heated bed isn't just a luxury — it's a real adhesion mechanism, and for printers designed around it, you can't simply turn it off and expect reliable prints.

But for filaments that don't need a heated bed (most PLA at lower ambient temperatures, some TPU), or for printers designed without one, the power budget is significantly lower.

## The running cost

At 2 cents per hour of printing:

- A 1-hour print: $0.02
- 8 hours of printing a day for a month: ~$4.80
- Running a printer 24/7 for a month: ~$14.40

These are the actual electricity costs. The filament is almost always the bigger variable cost — a typical 1kg spool runs $15–25, and a modest print might use 20–50 grams of it.

The per-print electricity cost for the 5-gram calibration cube here: about 0.6 cents for the filament (from a $13 spool), 1 cent for the electricity. Total material cost: approximately $0.016. If your concern is running costs, the electricity is a rounding error compared to filament.

## The watt meter as a shop tool

Having a plug-in watt meter available makes this kind of measurement trivial. Beyond printers, it's useful for: understanding whether an older desktop computer or monitor is worth the standby power cost, profiling a laser cutter or CNC machine's power draw before adding it to an existing circuit, or just satisfying curiosity about what things around the shop actually use.

The $15–20 investment pays for itself the first time it helps you avoid either an undersized circuit or an unexpectedly large electricity bill.

## Broader context: 3D printers vs. other workshop tools

For reference, typical workshop power draws:

- Bench-top drill press: 400–600W running
- Shop vacuum: 600–1,200W
- Table saw (contractor): 1,000–1,800W
- Air compressor (small): 700–1,500W
- 3D printer (FDM with heated bed): 40–225W

The 3D printer is at the low end of shop tool power consumption. It runs for hours unattended at relatively low wattage rather than drawing high current for short cutting bursts. From a circuit-planning standpoint, it's closer to a power tool on standby than a power tool in use.

## References and further reading

- [Kill-A-Watt P4400 meter](https://www.p3international.com/products/p4400.html) — the reference meter for this type of test; good baseline for comparing results
- [Anycubic Mega S specifications](https://www.anycubic.com/products/anycubic-mega-s-upgrade-version) — the printer tested; rated power and heated bed specs are listed here
- [Understanding your electric bill](https://www.energy.gov/energysaver/articles/electricity-bills-how-read-your-electricity-bill) — DOE guide on reading utility bills and finding your actual kWh rate
- [NEC 80% continuous load rule](https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=70) — the electrical code basis for the 80% circuit load guideline; Article 210 in the National Electrical Code
- [3D printer power consumption comparison (Reddit)](https://www.reddit.com/r/3Dprinting/comments/power_consumption/) — community measurements across many printer models; useful for comparing this result to Enders, Prusas, Bambus, etc.
- [Heated bed adhesion mechanics](https://all3dp.com/2/heated-bed-3d-printing-do-you-need-it/) — explains why the heated bed matters for print adhesion and when you can safely skip it
