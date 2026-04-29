---
title: 'How to Whiten Eyes in Photoshop the Easy Way'
description: 'A five-minute portrait retouching technique using Quick Selection, a layer copy, and an opacity dial-back — works in CS3 through current Photoshop and most versions of Elements.'
pubDate: 'September 14 2012'
youtubeId: 'FA5Zzx61LYU'
heroImage: '../../assets/posts/whiten-eyes-photoshop-cs5/thumbnail.jpg'
tags: ['photoshop', 'photo-editing', 'retouching', 'tutorial', 'portrait']
---

Eye whites are one of those subtle things in portrait photography. Nobody looks at a headshot and thinks "those eyes are brilliantly white" — but everyone notices when they're not. Reddish, flat, or slightly yellowed sclera drag a portrait down in a way that's hard to pin down but easy to feel. The fix is one of the oldest tricks in portrait retouching, and it takes about five minutes.

This post walks through the technique from the video: Quick Selection to isolate the eye whites, a layer copy, the transparent-pixel lock that keeps paint inside the lines, and the opacity dial-back that makes the result look like a better photo rather than a retouched one. It works in Photoshop CS3 through current versions and in most versions of Photoshop Elements.

> *This tutorial is from 2012, when the channel was still MeanPC.com — same Lonnie, same garage, same monitor.*

## Why eyes look dull in photos

The sclera is never truly white in photographs, even on a healthy, well-lit subject. There's a slight reddish or cream cast from blood vessels and natural pigmentation that our eyes compensate for in person but cameras don't. Indoor lighting makes it worse. A tired subject makes it worse. Even a slight color temperature mismatch in your white balance can push the whites toward yellow.

The instinct is to paint over the problem with white. That instinct is wrong — pure white kills the texture and vessel detail that makes an eye look alive, and the result reads immediately as artificial. What actually works is painting a ghost of white — a translucent layer that nudges the tones toward brighter without erasing the underlying structure.

That's the whole trick. Everything below is just the mechanics of getting there.

## What you'll need

- Photoshop CS3 or later, or Photoshop Elements (the menus are slightly different but the tools are the same)
- A portrait with visible eye whites — the technique assumes you can zoom in and see what you're selecting
- The bracket keys `[` and `]` — these resize your brush cursor and you'll use them constantly

## Step 1: Duplicate the background

Before touching anything, duplicate the background layer. `Ctrl+J` (Windows) or `Cmd+J` (Mac), or Layer → Duplicate Layer. Lock the original by clicking the lock icon in the Layers panel. You're working on the copy. If anything goes sideways, the original is untouched and you can start over.

This takes ten seconds and saves the kind of grief where you've done twenty minutes of retouching and realize you painted directly on the original.

## Step 2: Select the eye whites

Grab the Quick Selection tool — it's grouped with the Magic Wand in the toolbar, usually `W` to activate. Zoom into the eyes until you can see the whites clearly. Use `[` to shrink your cursor until it's roughly the width of the sclera, then click-and-drag across the white area. Photoshop's edge detection will expand the selection outward along the contrast boundary between the whites and the iris or eyelid.

If the selection bleeds onto skin or grabs part of the iris, hold `Alt` to switch from adding to subtracting, and dab over the areas you don't want. When you release `Alt`, Photoshop will tidy the edge. The Auto Enhance checkbox helps with edge quality but does slow things down on older machines — turn it off if the tool starts lagging.

Do both eyes before moving on. You want one combined selection covering all the eye white area.

## Step 3: Layer via Copy

With the eye whites selected, go to Layer → New → Layer via Copy (or `Ctrl+J` again). Photoshop creates a new layer containing only the selected pixels — just the whites, floating on a transparent background. Everything outside that selection is empty on this new layer.

Name it "eye whites" in the layer panel. You'll be adjusting its opacity later and you want to find it quickly.

## Step 4: Lock transparent pixels

This is the step most tutorials skip, and it's the one that keeps the job clean. With the eye whites layer selected, click the **Lock Transparent Pixels** button at the top of the Layers panel — it looks like a small checkerboard grid with a lock overlay.

What this does: constrains all painting to pixels that already exist on the layer. If you paint with a brush, the paint only lands on the eye-white pixels, not on the empty transparent areas around them. You physically cannot spill white onto surrounding skin, no matter how messy your brushwork.

Also check that this layer sits *above* the background copy in the layer stack. If it's underneath, every change you make will be invisible — covered by the layer on top.

## Step 5: Paint white across the eyes

Set your foreground color to pure white. The quickest way: hit `D` to reset foreground/background to defaults (black/white), then `X` to swap them so white is in front.

Select the Brush tool. In the options bar, enable **Airbrush mode** — the small spray-can icon. This gives you a softer, continuous-flow application that's easier to keep even across a curved surface. Set opacity to 100% — you're going to deal with the intensity in the next step, not here.

Use `]` to grow your brush until it covers most of the sclera in a single pass, then paint straight across both eyes.

It's going to look terrible. Like someone took correction fluid to the photograph. That's fine — that's where the opacity dial-back comes in.

## Step 6: Dial back the opacity

Select the eye whites layer and find the **Opacity** slider at the top of the Layers panel — not the Fill slider, the Opacity one. Start at 100% and drag left.

This is where the technique actually works. As you drop opacity, the white paint becomes translucent and the original eye color bleeds back through. Somewhere around 15–25% is usually the target — enough to visibly brighten the whites without erasing the texture, veins, and natural color variation that make the eye look real.

The rule: find the opacity where it looks good, then pull it back a little more. Retouchers consistently overdo local whitening. Your eye adapts to whatever's on screen. Take a break, come back, and you'll often find you went too far. A useful sanity check is to toggle the layer's visibility on and off — if you can instantly see the difference with it off, you've probably gone too far.

## The gotcha: layer order

If your eye whites layer ends up *below* the background copy in the stack, you'll see nothing — the background copy covers it completely. Check the layer panel before you start painting and make sure the eye whites layer is topmost. It's easy to accidentally drag a layer down when you're clicking around, and discovering this mistake after you've already done the painting is annoying.

Also: locked transparent pixels only apply to painting on *that* layer while it's selected. If you accidentally switch to a different layer and start painting, nothing stops you. Keep an eye on which layer is highlighted blue.

## Tips beyond the basic

**Teeth use the same method**, with one adjustment: don't use pure white. Teeth that are too white read as fake faster than eyes do. Mix in a very slight warm bias — something around RGB 255/252/240 — and the result holds up better under scrutiny. Same technique otherwise: selection, layer via copy, lock transparent pixels, airbrush, opacity dial-back.

**For glasses or heavy catch-lights**, the Quick Selection tool struggles — it'll grab the glare rather than the sclera. In those cases, switch to Quick Mask mode (`Q`) and paint the selection manually with a soft brush, then exit Quick Mask and proceed from step 3.

**Photoshop Elements** has the same tools under slightly different menus — Layer → New → Layer via Copy is sometimes under Edit → Copy, then Edit → Paste in Place. The layer locking and opacity controls are in the same positions.

## Where this fits today

Photoshop's AI-assisted retouching tools since the 2020s handle eye enhancement with a single slider through Neural Filters or the Subject Select workflow. If you're on a current subscription version, those tools exist and are worth exploring.

But the manual approach here gives you per-eye control that the automatic tools don't always offer — you can be heavier-handed on one eye than the other if the lighting was uneven, or leave a specific area of the sclera alone if there's a detail worth preserving. It also runs on Photoshop versions going back to CS3, including perpetual-license copies that never get subscription-era AI updates.

Knowing how the layers and paint mechanics work also makes you a better user of the automated tools, because you understand what they're actually doing — and when to override them.

## References and further reading

- [Adobe: Quick Selection Tool guide](https://helpx.adobe.com/photoshop/using/making-quick-selections.html) — official documentation on the selection options and Auto Enhance behavior
- [Adobe: Lock layer pixels](https://helpx.adobe.com/photoshop/using/locking-layers.html) — breakdown of all four lock modes and when to use each
- [Adobe: Layer opacity and blending](https://helpx.adobe.com/photoshop/using/blending-modes.html) — how opacity vs. fill interact with blend modes if you want to get more advanced
- [Cambridge in Colour: Portrait Retouching](https://www.cambridgeincolour.com/tutorials/photoshop-retouching.htm) — a solid independent guide to the broader workflow this technique fits into
