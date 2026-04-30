# Notes for Claude — Garage Geek Guy blog

This file is for Claude (and any AI assistant) working in this repo. It captures the conventions and judgments that aren't obvious from reading the code. For the broader project setup, see [SETUP.md](./SETUP.md).

## Session bootstrap (first interaction in a fresh Cowork session)

Do these once at the start of a new session, before doing real work. They're cheap and one-shot.

**0. Get your session ID and set up paths.** Every bash call below uses absolute paths to `/sessions/<your-session-id>/...`. Each bash call is independent (no env carryover), so put `SESSION_ID` and `BUILD_DIR` definitions at the top of every multi-step bash block, like this:

```bash
SESSION_ID=$(pwd | awk -F/ '{print $3}')   # current session is the third path component of pwd
echo "SESSION_ID=$SESSION_ID"
# Use $SESSION_ID anywhere you'd otherwise hard-code "kind-cool-hamilton" or similar
```

If you find yourself typing the literal string `<session-id>` into a path, you forgot this step.

**1. Install yt-dlp and Pillow** (used for pulling video metadata, transcripts, and thumbnails — needed for any new post). Idempotent; safe to re-run if you're not sure of state.

```bash
pip install --quiet --break-system-packages --no-warn-script-location yt-dlp Pillow
# yt-dlp lands at /sessions/$SESSION_ID/.local/bin/yt-dlp — invoke with the full path
```

**yt-dlp JS runtime fix (required for subtitle download).** The sandbox has no Deno; yt-dlp ≥ 2025 requires a JS runtime to extract YouTube data. Without it, `--write-auto-subs` silently produces no VTT files. Pass the `node` runtime explicitly on every yt-dlp call:

```bash
SESSION_ID=$(pwd | awk -F/ '{print $3}')
NODE=$(which node)                                       # /usr/bin/node
YTDLP="/sessions/$SESSION_ID/.local/bin/yt-dlp"

$YTDLP --js-runtimes "node:$NODE" --skip-download --write-auto-subs \
  --sub-lang en --sub-format vtt \
  --output "/tmp/{slug}" \
  "https://www.youtube.com/watch?v={VIDEO_ID}"
```

The `NODE`, `YTDLP`, and `SESSION_ID` definitions and the call must run **in a single bash invocation** — variables don't carry across calls.

**If yt-dlp fails to produce VTT files, stop and check with Lonnie — do not proceed to write posts without transcripts.** The warning `No supported JavaScript runtime could be found` means the `--js-runtimes` flag was omitted or formatted wrong.

**2. Configure git auth using the persisted PAT.** The token is stored at the path linked from `MEMORY.md` under the entry titled "GitHub PAT for garage-geek-guy". `MEMORY.md` is loaded into your context automatically, so use the Read tool on the linked file (a markdown file in the same memory directory) to get the token. Then in bash:

```bash
TOKEN="<paste-token-from-memory-file>"
git config --global user.name "Lonnie Honeycutt"
git config --global user.email "lonnie.honeycutt@gmail.com"
git config --global credential.helper store
python3 -c "
import os
path = os.path.expanduser('~/.git-credentials')
with open(path, 'w') as f:
    f.write('https://lonnie-developer:$TOKEN@github.com\n')
os.chmod(path, 0o600)
"
# Verify by trying a fetch from a fresh clone (see step 3)
```

If the bootstrap fails (PAT expired, memory file moved, fetch returns 401), tell Lonnie what's wrong and ask for a fresh PAT — don't silently degrade.

**3. Get a fresh checkout in `/tmp` and verify the project state.**

The workspace's local `.git` is **stale** — it lags origin/main because pushes happen from `/tmp` clones, and the sandbox can't keep the workspace's git state in sync. So `git status` in the workspace will show "your branch is behind by N commits" and report phantom modifications on files that were already committed and pushed. That's an artifact of the workspace `.git` being stale, not a real diff. **Don't trust the workspace's `git status` to decide what needs committing.**

Get an authoritative view by cloning fresh from origin into `/tmp`. Use a timestamped path because `/tmp` accumulates leftover dirs across sandbox sessions, and old dirs owned by `nobody:nogroup` can't be removed:

```bash
BUILD_DIR=/tmp/blog-build-$(date +%s)
git clone --quiet https://github.com/lonnie-developer/garage-geek-guy.git "$BUILD_DIR"
cd "$BUILD_DIR"
git log --oneline -5                # what's actually live
python3 scripts/queue-status.py     # published vs. remaining
echo "$BUILD_DIR" > /tmp/builddir.txt   # remember the path for later bash calls
```

Anything in `$BUILD_DIR` after the clone is already live; don't re-commit it. To check whether an unstaged-looking workspace file is actually a new change, compare against `$BUILD_DIR/<same-path>`.

**4. Sandbox filesystem limitation — what works where.**

The bash sandbox can **read** and **write** files anywhere in the workspace. What it cannot do is **`unlink`** (delete) any file it sees there, even files it just created. Two consequences:

- `npm run build` in the workspace fails. Vite tries to delete `node_modules/.vite/deps/_metadata.json` to refresh its dependency cache — `EPERM: operation not permitted, unlink`. Pagefind also wants to clear out and rewrite `dist/pagefind/`. Build only in `$BUILD_DIR` (a `/tmp` clone), where the sandbox owns the filesystem.
- `cp -r "<workspace>" /tmp/...` is unreliable. The `.git/objects/*` files hit "Resource deadlock avoided" on the macOS-bridged filesystem and the copy aborts mid-tree. **Use `git clone` from origin (step 3), not `cp -r`.**

`git` *commands* run fine in the workspace (`git status`, `git fetch`, `git pull`). They just operate on the stale local `.git` (see step 3). Use them for read-only inspection only; never push or commit from the workspace.

The Write/Edit file tools take a different path — they go through the macOS host, not the bash sandbox — so they CAN edit and create files in the workspace, including overwriting existing ones. Use them for editing posts and components. They cannot delete files either.

**If you need to delete a workspace file** (cleanup, removing cruft) and `rm` returns "Operation not permitted", request delete permission via the `mcp__cowork__allow_cowork_file_delete` tool. The sandbox bash CAN run `rm` once permission is granted.

After bootstrap, the steady-state for any change is: edit files in the workspace via Write/Edit → `cd $BUILD_DIR && cp -r workspace-changed-files . && npm run build && git add ... && git commit && git push`. (Or, in practice, edit in `$BUILD_DIR` directly and let the workspace catch up on its own next session — only the GitHub remote is the source of truth.)

## What this project is

The blog is the written companion to the [Garage Geek Guy YouTube channel](https://www.youtube.com/@garagegeekguy) — Lonnie Honeycutt's channel covering hands-on electronics, Arduino, microcontrollers, and DIY projects from the workshop. Each post is the written form of a video: video embedded at the top, then a polished tutorial-style writeup that adds context, links, and historical backstory the video doesn't cover.

The goal is to convert the channel's ~115 technical videos into well-researched blog posts. New videos get a post within a few days of upload.

**Project status as of 2026-04-29:** the back-catalog conversion is functionally complete. `queue-status.py` reports a small number of remaining "candidates," but on inspection those are filter false positives (TV commercials, sports-card shipping, etc.) — see "Picking candidates from the queue" below. Day-to-day work going forward is one new post per new video, not catch-up.

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

2. Pull metadata + transcript with yt-dlp (single bash call — variables don't carry across calls):
   SESSION_ID=$(pwd | awk -F/ '{print $3}')
   NODE=$(which node)
   YTDLP="/sessions/$SESSION_ID/.local/bin/yt-dlp"
   $YTDLP --js-runtimes "node:$NODE" \
     --skip-download --write-auto-subs --sub-lang en --sub-format vtt \
     --print "ID: %(id)s" --print "TITLE: %(title)s" --print "UPLOAD: %(upload_date)s" \
     --print "DURATION: %(duration)s" --print "TAGS: %(tags)s" \
     --print "DESC_BEGIN" --print "%(description)s" --print "DESC_END" \
     --output "/tmp/{slug}" \
     "https://www.youtube.com/watch?v={VIDEO_ID}"
   # The --js-runtimes flag is required or subtitles will silently fail to download.
   # Verify: ls /tmp/{slug}.en.vtt — if missing, stop and check with Lonnie.

3. Pull thumbnail (same single-call rule):
   SESSION_ID=$(pwd | awk -F/ '{print $3}')
   NODE=$(which node)
   YTDLP="/sessions/$SESSION_ID/.local/bin/yt-dlp"
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

7. Build to verify — clone fresh from origin (see bootstrap step 3):
   BUILD_DIR=/tmp/blog-build-$(date +%s)
   git clone --quiet https://github.com/lonnie-developer/garage-geek-guy.git "$BUILD_DIR"
   cd "$BUILD_DIR"
   # Copy your new/changed files into BUILD_DIR (the workspace edits aren't in
   # this fresh clone yet). For a single new post: just commit the new file
   # straight into BUILD_DIR via git, since the workspace and BUILD_DIR are
   # the same repo at HEAD.
   npm install     # only if not already installed in this BUILD_DIR
   npm run build   # must pass cleanly — see "If the build fails" below

8. Commit and push from BUILD_DIR:
   cd "$BUILD_DIR"
   git add <new files>
   git commit -m "..."
   git push origin main
```

**If the build fails:**
- `EPERM ... unlink ...node_modules/.vite/...` — you're building inside the workspace, not in `$BUILD_DIR`. Re-clone into a fresh `/tmp` path.
- `Pagefind: Indexed 0 pages` — the `<article data-pagefind-body>` wrapper in `src/layouts/BlogPost.astro` got moved or removed. Restore it. Healthy index for this site is "Indexed 107 pages, 6800+ words" as of this writing — if your number is way under that, something dropped out.
- Generic Astro error — read it, don't push, ping Lonnie if you can't resolve it. Don't commit broken posts.

## Conventions and small things

- **Heading style:** sentence case (`## What you'll need`), not title case.
- **External links inline.** Don't dump them all into a references section — work them into the prose where they're contextually relevant. The references section at the bottom catches the canonical sources that didn't fit elsewhere.
- **Code blocks** for any commands or code longer than a single inline `var`. Use language hints (` ```bash `, ` ```cpp `, ` ```yaml `) so syntax highlighting works.
- **Affiliate links:** none currently. If we ever add them, only on actual parts the post recommends — datasheets and reference docs stay non-affiliate.
- **Em-dashes** are used liberally — they fit the conversational rhythm. Don't replace them with commas just to "fix" them.
- **Numbers and units:** specific values (`2 A stall current`, `0.15 s/60°`) trump rounded ones. Get them from datasheets, not memory.

## Search — Pagefind

The blog uses [Pagefind](https://pagefind.app/) for client-side full-text search. A magnifying glass icon in the sticky header opens a modal search overlay. The `/` keyboard shortcut also opens it.

**How it works:** `npm run build` runs `astro build` followed by `pagefind --site dist`. Pagefind crawls the generated HTML and writes a binary search index into `dist/pagefind/`. At runtime, the Header lazy-loads `/pagefind/pagefind-ui.js` and `/pagefind/pagefind-ui.css` the first time the search overlay is opened (so they don't block page load). The JS file is injected via a `<script>` tag — see the IIFE gotcha note below for why a dynamic `import()` does NOT work. No server required — the index is just static files served by Cloudflare Pages.

**Search does not work in `npm run dev`** — expected behavior. The `_pagefind/` directory only exists after a full build. If you open search during dev, the overlay will show a friendly "run `npm run build` to generate it" message instead of crashing.

**Where the search UI lives:** `src/components/Header.astro`. The overlay and its JS are entirely self-contained in that file — no separate search page or component. Pagefind's default CSS variables are overridden inside `#search { ... }` to match the GGG dark palette (`--pagefind-ui-primary: var(--accent)`, etc.).

**Build script in `package.json`:**
```json
"build": "astro build && pagefind --site dist"
```
`pagefind` is a `devDependency` — Cloudflare Pages installs devDeps during CI builds so this works in production deploys without any extra config.

**If you add new post templates or page layouts** that should be excluded from search indexing (e.g. a raw JSON feed, an auto-generated redirect page), add `data-pagefind-ignore` to the `<body>` or the relevant element and Pagefind will skip it.

## Things that have already been tried and ruled out

- **AI-generated photo placeholders** (one round, then removed) — felt off, undermined authenticity.
- **Image placeholder divs in markdown** (CSS class `.img-placeholder` in `global.css`) — kept in the codebase as an unused utility in case we want it again, but not used in any current post.
- **GitHub web file uploads** — works but tedious for ongoing posts; GitHub Desktop or CLI push is the path.
- **Loading Pagefind UI via dynamic `import('/pagefind/pagefind-ui.js')`** — does NOT work. `pagefind-ui.js` is an IIFE that ends with `window.PagefindUI = ...;})()` and has no `export` statements. A dynamic import resolves with an empty namespace, `mod.PagefindUI` is undefined, and `new undefined(...)` throws — falling through to the "Search index not available" fallback even when the index is healthy. The fix (in `src/components/Header.astro`) is to inject a regular `<script src="/pagefind/pagefind-ui.js">` and read `window.PagefindUI` on `script.onload`. Don't refactor this back to `import()`.
- **`cp -r "<workspace>" /tmp/...`** to start a fresh build — fails with "Resource deadlock avoided" partway through `.git/objects/`. Use `git clone` from origin instead (see bootstrap step 3).

## Picking candidates from the queue

**Read this before writing any new post from `queue-status.py` output.** As of 2026-04-29 the back-catalog conversion is functionally done. `queue-status.py` will report a small `Remaining:` count, but on inspection every remaining row is a filter false positive — TV commercials, sports-card shipping, crawfish boil, floral pick machines, game tutorials. **Do not write posts for these.** If the output looks like that, the answer to "what's next?" is "wait for Lonnie to upload a new video."

When a new video is uploaded that should become a post, the trigger is Lonnie. Either he names it directly, or he runs `python3 scripts/refresh-manifest.py` to add it to the candidate file and then names it. Don't pick from the queue without confirmation.

If you do have a real candidate to write up, a few things to keep in mind:

**Multi-part series** (e.g., "How to build an Arduino Lite Brite Clock — Part 3 of 6") make awkward standalone posts because readers land mid-project without context. Options: write all parts in a single session so you can batch them, or consolidate the series into one overview post that links to the individual videos. Don't write just one episode in a series and leave the rest for later — it reads oddly.

**Obvious non-technical outliers** — a handful of videos slipped past the candidate filter that aren't really tutorials (e.g., a floral pick machine demo, a camera-leveling tip). If a video clearly doesn't fit the Arduino/electronics/DIY scope of the blog, skip it and note it for Lonnie to remove from `data/technical-candidates.tsv` manually.

**Everything else** — pick and go. Longer videos generally yield richer transcripts and more content to work with, but a tight 5-minute demo can make a clean short post too.

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
