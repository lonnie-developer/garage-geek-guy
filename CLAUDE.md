# Notes for Claude — Garage Geek Guy blog

This file is for Claude (and any AI assistant) working in this repo. It captures the conventions and judgments that aren't obvious from reading the code. For the broader project setup, see [SETUP.md](./SETUP.md).

## Session bootstrap (first interaction in a fresh Cowork session)

Do these once at the start of a new session, before doing real work. They're cheap and one-shot.

**1. Install yt-dlp** (used for pulling video metadata, transcripts, and thumbnails — needed for any new post):

```bash
pip install --quiet --break-system-packages --no-warn-script-location yt-dlp Pillow
# yt-dlp will be at /sessions/<session-id>/.local/bin/yt-dlp
# Either prepend that to PATH or invoke with the full path
```

**yt-dlp JS runtime fix (important — required for subtitle download):** The sandbox does not have Deno installed, and yt-dlp ≥ 2025 requires a JS runtime for YouTube extraction. Without it, `--write-auto-subs` silently produces no VTT files. The fix is to pass the `node` runtime explicitly on every yt-dlp call that fetches subtitles or metadata:

```bash
NODE=$(which node)   # node is at /usr/bin/node in the sandbox
YTDLP="/sessions/<session-id>/.local/bin/yt-dlp"

$YTDLP --js-runtimes "node:$NODE" --skip-download --write-auto-subs \
  --sub-lang en --sub-format vtt \
  --output "/tmp/{slug}" \
  "https://www.youtube.com/watch?v={VIDEO_ID}"
```

**If yt-dlp fails to produce VTT files, stop and check with Lonnie — do not proceed to write posts without transcripts.** The `--js-runtimes "node:..."` flag must appear on every invocation that downloads subtitles. The warning `No supported JavaScript runtime could be found` means the flag was omitted or incorrectly formatted.

**2. Configure git auth using the persisted PAT.** The token lives in the user's persistent Claude memory store. Read it with the Read tool from the path indicated in `MEMORY.md` (the entry titled "GitHub PAT for garage-geek-guy"), then:

```bash
git config --global user.name "Lonnie Honeycutt"
git config --global user.email "lonnie.honeycutt@gmail.com"
git config --global credential.helper store
python3 -c "
import os
home = os.path.expanduser('~')
path = os.path.join(home, '.git-credentials')
token = '<TOKEN_FROM_MEMORY_FILE>'
with open(path, 'w') as f:
    f.write(f'https://lonnie-developer:{token}@github.com\n')
os.chmod(path, 0o600)
"
# Verify with: cd to repo, git fetch origin
```

**3. Verify the sandbox understands the project.** Quick sanity check:

```bash
cd "/sessions/<session-id>/mnt/Blog project"
git status
git log --oneline -5
```

If the bootstrap fails (PAT expired, file moved, etc.), tell Lonnie what's wrong and ask for a fresh PAT — don't silently degrade.

**4. Sandbox filesystem limitation — build and git must run from /tmp.**

The bash sandbox cannot write to the workspace's `.git/` directory or `node_modules/.vite/deps/`. Running `npm run build` or any `git` command directly in the mounted workspace folder will fail with permission errors. The workaround is to copy the project to `/tmp` first, then do all build and git operations there:

```bash
cp -r "/sessions/<session-id>/mnt/Blog project" /tmp/blog-build
cd /tmp/blog-build

# Build to verify
npm run build

# Stage, commit, and push
git add <files>
git commit -m "..."
git push origin main
```

The Write/Edit file tools bypass this restriction and can write directly to the workspace folder — use them for creating and editing post files. Only `npm run build` and `git` commands need the /tmp workaround.

After bootstrap, you can pull a video transcript, draft a post, commit, and push — all from the sandbox, no GUI needed.

## What this project is

The blog is the written companion to the [Garage Geek Guy YouTube channel](https://www.youtube.com/@garagegeekguy) — Lonnie Honeycutt's channel covering hands-on electronics, Arduino, microcontrollers, and DIY projects from the workshop. Each post is the written form of a video: video embedded at the top, then a polished tutorial-style writeup that adds context, links, and historical backstory the video doesn't cover.

The goal is to convert the channel's ~115 technical videos into well-researched blog posts, working backward through the catalog. New videos get a post within a few days of upload.

## Voice — the most important thing to get right

The voice is **a knowledgeable friend at the bench**. Specifically:

**Lean toward** — first-person plural for shared discovery ("we'll desolder these three leads"), occasional first-person singular for asides ("the first thing I do is photograph the gear stack"), short declarative sentences mixed with longer explanatory ones, dry occasional humor (the magic-smoke jokes, the "any two of three" framing), specific over abstract ("a $10 servo from eBay" not "an inexpensive hobby servo"), naming gotchas before they bite the reader.

**Avoid** — corporate marketing voice ("In today's fast-paced robotics landscape..."), textbook formality ("The MG995 servo motor, manufactured by TowerPro..."), bullet-list overload (use prose for explanations; bullets for lists of *items*, not lists of *thoughts*), hedging ("you might want to consider possibly..."), unnecessary jargon, AI-tells like "delve," "robust," "leverage."

**Calibration sample.** The TowerPro MG995 post (`hack-towerpro-mg995-continuous-rotation.md`) is the locked reference. When in doubt, match its rhythm and density. It opens with a hook framing ("there's a particular flavor of cheapness..."), uses occasional asides for color, gets specific quickly, and builds gradually from context → mechanism → execution → broader fit.

**A note on the channel's history.** The earlier videos (pre-rebrand) were uploaded under "MeanPC.com." If a post is from that era, a brief italicized note acknowledging it adds authenticity ("*this build is from 2012, when the channel was still meanPC.com — same Lonnie, same garage, same workbench*"). Don't make a big deal of it; one sentence suffices.

## Post structure template

Roughly the shape used in the MG995 post. Adapt as the topic demands; don't impose this on a post that doesn't need it.

1. **Hook (1-2 paragraphs).** A framing that earns attention. Often: a tradeoff, a counterintuitive fact, a question the reader didn't know they had.
2. **What this post will cover (1 short paragraph).** Explicit promise: "this post walks through X, Y, and Z." Helps SEO and reader orientation.
3. **Optional: era/history note** if the video is meaningfully old.
4. **Background section (the part itself / the technique itself).** Specs, history, why this exists, who made it, what's notable.
5. **Why this matters / why hack/build/use it.** The motivation section. Often a chance to bring in broader context (Boe-Bot history for the servo hack, Hayes modem history for an AT-command post, etc.). 1-2 paragraphs of "the larger story this fits into."
6. **What you'll need / parts list.** Concrete, with model numbers and rough prices.
7. **The build / mechanism / walkthrough.** The actual content. Break into named subsections for skimmability.
8. **The gotcha.** Most builds have one specific thing nobody warns you about. Surface it as its own thing — bold-headed paragraph or short subsection. The MG995 post's "calibration nobody tells you about" is the model.
9. **Tips beyond the basic.** Edge cases, scaling considerations, what to do if you're using this for a different goal.
10. **Where this fits today (and where it doesn't).** Honest framing — for what use cases is this still the right answer? When should you reach for something else? Names of better alternatives.
11. **References and further reading.** 5-10 bullet points: datasheets, canonical forum threads, library docs, related Wikipedia pages. Mix of "definitive" sources (datasheets, manufacturer pages) and "community" sources (Hackaday, Adafruit guides, Parallax forums).

**Length target:** 1500-2500 words for a typical 15-30 minute video. Longer for big build series, shorter for a 5-minute demo.

## Frontmatter — required and optional

```yaml
---
title: 'Match the YouTube title closely; punch it up only if it gains clarity'
description: 'One-sentence hook that doubles as OG description. Aim for 150-250 chars.'
pubDate: 'August 19 2012'                   # Original YouTube upload date — backdate exactly
youtubeId: 'cnOKG0fvZ4w'                    # The 11-char video ID
heroImage: '../../assets/posts/{slug}/thumbnail.jpg'
tags: ['arduino', 'servo', 'tutorial']      # 3-7 lowercase, hyphenated tags
---
```

**Slug naming:** lowercase, hyphenated, action-verb-led when possible. `hack-towerpro-mg995-continuous-rotation` not `MG995_servo_hack`. Matches the URL the post will live at.

## Image policy

**No AI-generated images.** This was tried; we course-corrected. AI images of specific electronic components are unreliable and add an "off" feeling that undermines the post's authenticity.

**Allowed:**
- The YouTube thumbnail, downloaded via `yt-dlp` and used as `heroImage` for OG/social cards. The post page itself shows the YouTube embed instead — `heroImage` is OG-only.
- Self-made diagrams (SVG schematics, wiring diagrams, simple charts) when they materially help the reader understand something the video doesn't make clear. Make these only when they add real value.
- Real bench photos — if Lonnie supplies them for a specific post, drop them into `src/assets/posts/{slug}/` and reference with relative markdown paths.

**Not allowed:**
- AI-generated photos of bench setups, components, hands-with-tools, etc.
- Stock photography
- Generic "Arduino" or "robotics" stock images

## Workflow for a new transcript-derived post

```
1. Pick a video from the technical-content manifest in this repo:
   - `data/technical-candidates.tsv` — filtered list of build/teach posts
   - `data/videos.tsv` — full channel catalog if the candidate filter missed something
   Run `python3 scripts/queue-status.py` to see how many are left and what's next.

2. Pull metadata + transcript with yt-dlp:
   NODE=$(which node)
   YTDLP="/sessions/<session-id>/.local/bin/yt-dlp"
   $YTDLP --js-runtimes "node:$NODE" \
     --skip-download --write-auto-subs --sub-lang en --sub-format vtt \
     --print "ID: %(id)s" --print "TITLE: %(title)s" --print "UPLOAD: %(upload_date)s" \
     --print "DURATION: %(duration)s" --print "TAGS: %(tags)s" \
     --print "DESC_BEGIN" --print "%(description)s" --print "DESC_END" \
     --output "/tmp/{slug}" \
     "https://www.youtube.com/watch?v={VIDEO_ID}"
   # The --js-runtimes flag is required or subtitles will silently fail to download.
   # Verify: ls /tmp/{slug}.en.vtt — if missing, stop and check with Lonnie.

3. Pull thumbnail:
   $YTDLP --js-runtimes "node:$NODE" \
     --skip-download --write-thumbnail --convert-thumbnails jpg \
     --output "src/assets/posts/{slug}/thumbnail" \
     "https://www.youtube.com/watch?v={VIDEO_ID}"

   NOTE: --convert-thumbnails jpg does not work reliably in the sandbox (ffmpeg
   missing). yt-dlp will download a .webp file regardless. Convert it manually
   with PIL immediately after, then move on — the .webp will be left behind but
   is covered by .gitignore so it won't pollute the repo:

   python3 -c "
   from PIL import Image
   img = Image.open('src/assets/posts/{slug}/thumbnail.webp')
   img.convert('RGB').save('src/assets/posts/{slug}/thumbnail.jpg', 'JPEG', quality=90)
   print('Converted')
   "

4. Clean the .vtt transcript (Python snippet that strips inline timing tags
   and dedupes lines is in the MG995 working notes)

5. Web-research the broader context — usually 2-3 searches:
   - The component/technique itself (specs, history, who made it)
   - The "why this matters" angle (related techniques, parallel products, foundational projects)
   - Specific authoritative references (datasheets, forum threads, library docs)

6. Draft the post in src/content/blog/{slug}.md following the structure above.

7. Build to verify — use the /tmp copy (see sandbox limitation note in bootstrap):
   cp -r "/sessions/<session-id>/mnt/Blog project" /tmp/blog-build
   cd /tmp/blog-build && npm run build   # must pass cleanly

8. Commit and push from /tmp/blog-build (same sandbox limitation):
   git add <new files>
   git commit -m "..."
   git push origin main
```

## Conventions and small things

- **Heading style:** sentence case (`## What you'll need`), not title case.
- **External links inline.** Don't dump them all into a references section — work them into the prose where they're contextually relevant. The references section at the bottom catches the canonical sources that didn't fit elsewhere.
- **Code blocks** for any commands or code longer than a single inline `var`. Use language hints (` ```bash `, ` ```cpp `, ` ```yaml `) so syntax highlighting works.
- **Affiliate links:** none currently. If we ever add them, only on actual parts the post recommends — datasheets and reference docs stay non-affiliate.
- **Em-dashes** are used liberally — they fit the conversational rhythm. Don't replace them with commas just to "fix" them.
- **Numbers and units:** specific values (`2 A stall current`, `0.15 s/60°`) trump rounded ones. Get them from datasheets, not memory.

## Things that have already been tried and ruled out

- **AI-generated photo placeholders** (one round, then removed) — felt off, undermined authenticity.
- **Image placeholder divs in markdown** (CSS class `.img-placeholder` in `global.css`) — kept in the codebase as an unused utility in case we want it again, but not used in any current post.
- **GitHub web file uploads** — works but tedious for ongoing posts; GitHub Desktop or CLI push is the path.

## Picking candidates from the queue

Order doesn't matter — the goal is to get all 110+ videos done, not to do them in any particular sequence. Just pick from the unpublished list and work through them.

A few things that affect which videos make good standalone posts:

**Multi-part series** (e.g., "How to build an Arduino Lite Brite Clock — Part 3 of 6") make awkward standalone posts because readers land mid-project without context. Options: write all parts in a single session so you can batch them, or consolidate the series into one overview post that links to the individual videos. Don't write just one episode in a series and leave the rest for later — it reads oddly.

**Obvious non-technical outliers** — a handful of videos slipped past the candidate filter that aren't really tutorials (e.g., a floral pick machine demo, a camera-leveling tip). If a video clearly doesn't fit the Arduino/electronics/DIY scope of the blog, skip it and note it for Lonnie to remove from `data/technical-candidates.tsv` manually.

**Everything else** — just pick and go. Longer videos generally yield richer transcripts and more content to work with, but a tight 5-minute demo can make a clean short post too.

## What's reusable / what's the manifest

The manifest lives in the repo as the single source of truth — it persists across sessions and is diffable across refreshes.

- `data/videos.tsv` — every video on the channel (~740 rows, sorted by id)
- `data/technical-candidates.tsv` — filtered subset that could become posts (~114 rows)
- `scripts/refresh-manifest.py` — regenerates both files; filter rules (INCLUDE_PATTERNS / EXCLUDE_PATTERNS) live at the top of this script
- `scripts/queue-status.py` — derives published/remaining counts from blog frontmatter, no separate "published" list to keep in sync
- `data/README.md` — explains the structure and refresh workflow

When a published post references a video that the candidate filter missed, `queue-status.py` flags it and suggests tightening the filter rules.

Per-video transcripts and metadata are pulled on demand at draft time (see workflow above) and are NOT committed to the repo — they're large and only needed once.

## When in doubt, match the pilot

If you're picking up this project mid-stream and uncertain about voice, structure, depth, or length — the [TowerPro MG995 post](src/content/blog/hack-towerpro-mg995-continuous-rotation.md) is the calibration reference. It's been read and approved by Lonnie. Match its rhythm.
