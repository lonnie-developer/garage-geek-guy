---
title: 'How to Connect a Nintendo Switch Pro Controller to a Mac or PC'
description: 'Pairing the Switch Pro Controller to a Mac via Bluetooth in under a minute — what to press, what to look for, and how to verify it is working before you load a game.'
pubDate: 'August 11 2022'
youtubeId: 'QoiUB_cQEGE'
heroImage: '../../assets/posts/nintendo-switch-pro-controller-mac-pc/thumbnail.jpg'
tags: ['nintendo', 'gaming', 'mac', 'bluetooth', 'tutorial', 'controller']
---

The Nintendo Switch Pro Controller is genuinely good hardware — comfortable grip, full button set, good d-pad, solid analog sticks, and about 40 hours of battery life per charge. It also happens to work over Bluetooth with Macs and PCs without any driver installation, which makes it a reasonable choice for desktop gaming if you already own one for your Switch.

The pairing process takes less than a minute once you know where the pairing button is.

## What you'll need

- Nintendo Switch Pro Controller (charged)
- A Mac or PC with Bluetooth
- Optionally: a USB-C cable if you'd rather connect wired

The wireless connection is the easier path and works well. Wired via USB-C also works and is plug-and-play on most systems.

## Pairing on Mac via Bluetooth

Open System Preferences (or System Settings on macOS Ventura and later) → Bluetooth. Make sure Bluetooth is on and you can see the device list.

On the Pro Controller, look for the small circular button on the top edge, next to the USB-C charging port. That's the pairing button — it's recessed slightly and easy to miss if you're looking for something labeled "sync" or "pair."

Hold that button for a second or two. The four player indicator lights on the front of the controller will start cycling in a sweeping pattern — the lights chase back and forth across the four positions, similar to the light pattern from KITT in Knight Rider. That sweep means the controller is in pairing mode and advertising itself.

In your Bluetooth device list, "Pro Controller" should appear. Click Connect. The lights stop sweeping and settle into a single indicator showing the controller number. The connection completes in a few seconds.

## Verifying it works

Before you load any game or emulator, it's worth doing a quick button check. The reliable way is to use a browser-based gamepad tester — [gamepad-tester.com](https://gamepad-tester.com) or the equivalent — which reads the controller through the Web Gamepad API and lights up on-screen indicators as you press each button.

Press a button and watch for the detection. The site should identify it as a Switch Pro Controller. Run through the full button set: face buttons, shoulder buttons (L/R and ZL/ZR), both analog sticks (including click), d-pad, and the Home and Capture buttons. Note that the Home button may register a system-level action on macOS — on the Mac tested here, pressing Home minimized something — so that one works, it just also does something else.

Once all inputs register correctly, you're done. The controller will remember the Bluetooth pairing and reconnect automatically on subsequent sessions.

## Using it on PC

The same pairing process applies on Windows: Bluetooth settings → Add device → Bluetooth → hold the pairing button on the controller → select Pro Controller when it appears. Windows may identify it as a generic HID device or specifically as a Pro Controller depending on the version.

For gaming on PC, most emulators (Yuzu, Ryujinx, RPCS3, RetroArch) have direct support for the Pro Controller and handle button mapping automatically. For games purchased through Steam, the Steam client has built-in Pro Controller support under Settings → Controller → Nintendo Button Layout — this lets you choose whether to swap A/B and X/Y to match Switch or Xbox conventions.

For non-Steam games that need a driver, [BetterJoy](https://github.com/Davidobot/BetterJoy) presents the Pro Controller as an Xbox controller to Windows, which makes it compatible with anything that supports XInput.

## Wired alternative

If Bluetooth is unreliable or you want zero latency, a USB-C cable connected directly to the controller and a USB-A or USB-C port on your computer works without any pairing steps. The controller is recognized as a USB HID device immediately. On Mac, it shows up in System Information under USB. The controller charges via the same cable simultaneously.

## Why the Pro Controller holds up as a desktop gamepad

The main alternatives for desktop gaming are Xbox controllers (native XInput support on Windows, works on Mac) and PlayStation DualSense/DualShock 4 (also Bluetooth-capable, good haptics). The Pro Controller sits alongside these without any major disadvantages: the button layout is comfortable, the sticks have good precision, and the battery life is exceptional compared to most competitors.

If you own a Switch, you already have it. If you're buying a controller specifically for desktop use, the XInput advantage of Xbox controllers makes them simpler on Windows — but for Mac users or anyone who prefers the Nintendo layout, the Pro Controller is a legitimate option at a fair price point.

## References and further reading

- [BetterJoy — GitHub](https://github.com/Davidobot/BetterJoy) — presents Pro Controller as XInput on Windows for non-Steam games
- [Steam Controller Settings — Valve](https://help.steampowered.com/en/faqs/view/1B05-C4C2-1C0F-61AC) — Steam's built-in controller configuration including Nintendo layout support
- [Gamepad Tester](https://gamepad-tester.com) — browser-based controller verification using the Web Gamepad API
