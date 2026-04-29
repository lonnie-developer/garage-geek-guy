---
title: 'How to Fix the Arduino Uno Serial Port Problem on Mac'
description: 'Arduino clone not showing a serial port in the IDE on macOS? The fix is a CH340 driver install plus one terminal command. Here is exactly what to do.'
pubDate: 'October 23 2018'
youtubeId: '4tOAwJ8Rn9c'
heroImage: '../../assets/posts/fix-arduino-uno-serial-port-mac/thumbnail.jpg'
tags: ['arduino', 'troubleshooting', 'macos', 'serial', 'beginner']
---

There's a specific kind of frustration that hits when you plug in your new Arduino Uno, fire up the IDE, go to Tools → Port — and find nothing but a couple of Bluetooth entries. No `/dev/cu.usbserial-...`. No `/dev/cu.wchusbserial-...`. Just Bluetooth and a sinking feeling that you're about to spend two hours reading forums.

If that's you, there's a good chance the problem isn't your Arduino, your cable, or your Mac. It's a missing driver for the USB-to-serial chip that most Arduino clones use. This post walks through exactly what to install and why, and gets you back to uploading sketches in about ten minutes.

## Why clones and official boards behave differently

The genuine Arduino Uno uses an ATmega16U2 as its USB interface chip. That chip has native macOS driver support built in — plug it in and it just works.

The vast majority of Arduino Uno *clones*, though, swap that chip out for a CH340 or CH341, made by the Chinese manufacturer WCH. It costs less, it works well, and it runs the same firmware protocol — but macOS has no built-in driver for it. The IDE can't see the serial port because the operating system doesn't know what to do with the chip.

This is that problem in miniature: you've got a board that behaves identically to a genuine Uno in every meaningful way, except for a $0.50 chip difference that requires one extra installation step on Mac. It's not a defect. It's just something the listings rarely mention.

## What you'll need

- Your Arduino clone (CH340-based — if you're not sure, it almost certainly is if it didn't come in official Arduino packaging)
- Arduino IDE installed from [arduino.cc](https://www.arduino.cc/en/software)
- The CH340 driver for macOS — the most reliable current build is maintained at [github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver](https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver), and the WCH manufacturer also maintains official drivers at [sparks.gogo.co.nz/ch340.html](https://sparks.gogo.co.nz/ch340.html)

## Installing the driver

Download the `.pkg` installer and double-click it. The install process is straightforward but macOS will stop you at least once — on newer macOS versions, a third-party kernel extension triggers a security prompt that you have to acknowledge manually.

When that happens, the installer will tell you to go to **System Preferences → Security & Privacy** (or **System Settings → Privacy & Security** on Ventura and later) and click **Allow** next to the blocked developer entry. The button only stays visible for a short window after the blocked install attempt, so go there immediately. Once you've approved it, run the installer again — it will complete cleanly.

## The terminal command

After the driver is installed but *before* you restart, the WCH driver page specifies running a command in Terminal to finalize the install. Open Terminal and run:

```bash
sudo nvram boot-args="kext-dev-mode=1"
```

On some macOS versions this step isn't required, but it doesn't hurt to run it. When in doubt, run it.

Then restart your Mac.

## After the restart

Once the Mac is back up, plug in your Arduino and open the IDE. Go to **Tools → Port** — you should now see an entry along the lines of `/dev/cu.wchusbserial-1420` or `/dev/cu.usbserial-1410`. The exact name varies, but it will say something about USB serial, and it will be clearly distinct from the Bluetooth entries.

Select that port, open the Blink sketch (**File → Examples → 01.Basics → Blink**), and hit upload. If the onboard LED goes from its panicked fast-blink to a calm one-per-second blink, you're done.

## The gotcha: macOS keeps changing the rules

The CH340 driver situation on macOS has been a moving target since Apple started tightening kernel extension (kext) policies around macOS High Sierra and continuing through Catalina, Big Sur, and beyond. If you're on a newer macOS and the above steps don't work, the most common causes are:

- **Driver version is old.** WCH and the community maintainers update these fairly often. Grab the newest package from the links above and try again.
- **SIP is blocking the kext.** On Macs with System Integrity Protection fully enabled, some older driver packages can't load. The GitHub link above tends to stay current with Apple's evolving signing requirements.
- **Conflicting drivers.** If you've installed both Apple's built-in CH34x support (present in some macOS builds) and the third-party driver, they can fight over the port and produce nothing. Uninstall the third-party driver, restart, and try the native one first.

The [Arduino forum thread on CH340/CH341 and macOS Mojave](https://forum.arduino.cc/t/in-case-you-are-having-problems-with-macos-mojave-and-ch340-usb-drivers/548030) is worth bookmarking — the community keeps it updated as macOS versions shift.

## Why the clone is still fine

None of this changes the fact that CH340-based clones are perfectly capable hardware. They're compatible with every library, every sketch, every project — the only difference is this one setup step on Mac. Once the driver is in, the board works exactly like a genuine Uno. The $10–$12 price difference buys you a bit of plug-and-play convenience on macOS and that's about it.

If you're buying boards regularly and you're primarily on Mac, it's worth keeping one genuine Arduino Uno around for when you want to hand something to a student or colleague without worrying about driver setup. But for your own bench? The clone is fine.

## References

- [CH340/CH341 driver, community-maintained macOS build](https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver)
- [CH340 Drivers for Windows, Mac, and Linux — sparks.gogo.co.nz](https://sparks.gogo.co.nz/ch340.html)
- [Arduino forum: CH340 and macOS Mojave troubleshooting thread](https://forum.arduino.cc/t/in-case-you-are-having-problems-with-macos-mojave-and-ch340-usb-drivers/548030)
- [Arduino IDE download — arduino.cc](https://www.arduino.cc/en/software)
- [WCH official CH341SER Mac driver page](http://www.wch-ic.com/downloads/CH341SER_MAC_ZIP.html)
