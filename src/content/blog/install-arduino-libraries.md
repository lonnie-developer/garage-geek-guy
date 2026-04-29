---
title: '3 Ways to Install Arduino Libraries into the Arduino IDE'
description: 'When a sensor or display needs a library, you have three routes: the built-in Library Manager, ZIP file import, and dropping files directly into the Arduino libraries folder. Here''s how each one works.'
pubDate: 'November 10 2018'
youtubeId: 'xvfrozY4NAc'
heroImage: '../../assets/posts/install-arduino-libraries/thumbnail.jpg'
tags: ['arduino', 'ide', 'libraries', 'beginner', 'tutorial']
---

At some point in almost every Arduino project, you hit a wall. You've got an OLED display, or a keypad, or a real-time clock module, and the thing needs a library — a pre-written chunk of code that handles the low-level communication so your sketch can just call `display.print("hello")` instead of manually bit-banging I2C. The question is how to get that library into your Arduino IDE so it's available when you compile.

There are three ways. They all work. Which one you reach for depends on where you found the library and how you like to work.

## Method 1: the Library Manager

This is the easiest route when the library you want is in the official Arduino repository. Open the IDE, go to **Tools → Manage Libraries**, and a search window opens with a curated list of indexed libraries.

Search for what you need — `LiquidCrystal I2C`, `Keypad`, `DHT sensor library`, whatever it is — and the matching results show up with version numbers and author names. Click **Install** on the one you want, wait a few seconds, and it's done.

A critical thing to do after any library install, regardless of which method you use: **close the Arduino IDE and reopen it.** The IDE scans the libraries folder at startup and builds its menu from what it finds there. If you install a library while the IDE is running and don't restart, it won't show up under File → Examples and the `#include` autocomplete won't know it exists. Reopen it and you'll see the new library in the list.

After restarting, go to **File → Open** and look for the library under the examples submenu. Most libraries include example sketches — those are worth opening to see working code before you try writing your own from scratch.

The Library Manager works well for popular, actively maintained libraries. For anything more obscure, or for a library that's not in the official index (a lot of GitHub-only libraries fall into this category), you'll need one of the other two methods.

## Method 2: ZIP file import

A lot of Arduino libraries live on GitHub. The author maintains the code there but hasn't submitted it to the Arduino index — or they have, but the version in the index lags behind the GitHub version. In either case, you can download it as a ZIP and import it directly.

On the GitHub page for the library, click the **Code** button (green, top right) and select **Download ZIP**. Note where your browser saves it — usually your Downloads folder.

Back in the Arduino IDE: **Sketch → Include Library → Add .ZIP Library**. Navigate to the ZIP file you just downloaded, select it, and click Choose (or Open). The IDE extracts it into your libraries folder and makes it available.

Same rule applies: restart the IDE afterward. Once restarted, it'll show up under File → Examples with any example sketches the library author included.

## Method 3: manual folder placement

This one skips the IDE entirely. The Arduino libraries folder is just a regular folder on your computer, and you can drop library folders directly into it without touching the IDE at all.

On Mac, it lives at **~/Documents/Arduino/libraries/**. On Windows, it's typically **Documents\Arduino\libraries\\** — the exact path depends on your Arduino IDE version and whether you've changed the sketchbook location in preferences.

Open that folder. You'll see subfolders for every library you've already installed — one folder per library, named after the library. If you have a library ZIP downloaded from GitHub, extract it and drop the extracted folder straight in here. The name of the folder is what appears in the IDE's menus.

To confirm it's working: close the Arduino IDE, reopen it, and check File → Examples. The library should be there.

This method is also how you remove libraries. Find the folder for the library you want to uninstall, move it to Trash (or Recycle Bin), restart the IDE, and it's gone from the menus.

## Which method to use when

For anything in the official Arduino library index — use the Library Manager. It handles version management and lets you update libraries later without hunting for ZIP files. Search, click Install, restart, done.

For a GitHub-only library or a specific version that isn't in the index — download the ZIP and use **Add .ZIP Library**. It's two extra steps compared to the Library Manager but not meaningfully slower.

For power users who want to install multiple libraries at once, manage library versions by hand, or work with locally modified library code — use the folder method. It gives you direct access to the library files, which is useful if you ever need to look at a library's source to understand why it's behaving a certain way.

## The gotcha: version conflicts

If you have two versions of the same library installed — one from the Library Manager and one dropped manually into the libraries folder — the IDE may get confused about which one to use. The symptom is usually a compile error that refers to duplicate definitions or conflicting function signatures.

The fix is to check the libraries folder directly, remove the duplicate, restart the IDE, and re-install the version you actually want via one of the three methods above. The Library Manager shows you what's currently installed if you go to Tools → Manage Libraries and look at the Installed tab.

## A note on library versions and the IDE

The video was made with Arduino IDE 1.7. The same three methods apply to IDE 2.x, though some UI details differ — Library Manager is now its own sidebar panel rather than a popup window, and there's a dedicated Libraries view. The keyboard shortcut `Ctrl+Shift+I` (or `Cmd+Shift+I` on Mac) opens it directly. The underlying mechanics — the libraries folder, the ZIP import, the restart-to-refresh — work exactly the same way.

## References and further reading

- [Arduino Reference — Libraries](https://www.arduino.cc/reference/en/libraries/) — index of all officially supported libraries
- [Arduino Guide — Installing Libraries](https://docs.arduino.cc/software/ide-v1/tutorials/installing-libraries/) — official documentation for all three methods
- [Arduino Playground — Library List](https://playground.arduino.cc/Main/LibraryList/) — community-maintained index including libraries not in the official index
- [GitHub — Arduino Libraries Organization](https://github.com/arduino-libraries) — official library source repositories
- [Adafruit — Installing Libraries](https://learn.adafruit.com/adafruit-all-about-arduino-libraries-install-use) — Adafruit's guide, useful if you're installing their sensor/display libraries
