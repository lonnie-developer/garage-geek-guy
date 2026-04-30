# Garage Geek Guy Blog — Setup & Operations

This document captures how the blog is built, deployed, and maintained. It's the "if you (or anyone) walked away for six months and came back, here's how to pick it up" reference.

## Stack at a glance

- **Framework:** [Astro](https://astro.build/) (static site generator)
- **Hosting:** [Cloudflare Pages](https://pages.cloudflare.com/) (free tier)
- **Source:** [github.com/lonnie-developer/garage-geek-guy](https://github.com/lonnie-developer/garage-geek-guy) (public)
- **Live site:** [garage-geek-guy.pages.dev](https://garage-geek-guy.pages.dev/)
- **Local clone:** `/Users/lonniehoneycutt/Documents/Claude/Projects/Blog project` (on Lonnie's Mac)
- **Custom domain:** none yet — running on the `.pages.dev` subdomain

The whole pipeline is: post markdown lands in `src/content/blog/` → push to `main` on GitHub → Cloudflare auto-builds and deploys → live in ~60 seconds. No manual deploy step.

## Accounts and services

| What | Identifier | Notes |
| --- | --- | --- |
| GitHub | `lonnie-developer` | Personal account, owns the repo |
| Cloudflare | `Lonnie.developer@gmail.com` | Free tier; account ID `3e41076dc2d939f4e1827e57d8429172` |
| GitHub App | "Cloudflare Workers and Pages" | Installed with read/write access to *only* `garage-geek-guy` |
| Cost | $0/month | All free-tier; only future cost is a custom domain (~$10/yr) |

## Repository structure

```
Blog project/
├── astro.config.mjs           # Astro build config; site URL set to garage-geek-guy.pages.dev
├── package.json               # Project metadata; name "garage-geek-guy"
├── package-lock.json
├── tsconfig.json
├── README.md                  # Lightweight overview (also useful for first-time GitHub viewers)
├── SETUP.md                   # This file
├── CLAUDE.md                  # Notes for AI assistants working in this repo
├── public/                    # Static assets served as-is (favicon, etc.)
└── src/
    ├── consts.ts              # Site-wide constants: title, channel URL, author byline
    ├── content.config.ts      # Frontmatter schema for blog posts
    ├── styles/global.css      # Theme: dark + electric-yellow GGG accent
    ├── assets/
    │   ├── fonts/             # Atkinson Hyperlegible (preloaded)
    │   ├── blog-placeholder-* # Default OG fallback images
    │   └── posts/{slug}/      # Per-post assets (YouTube thumbnails, etc.)
    ├── components/
    │   ├── BaseHead.astro     # <head> meta, OG cards, canonical, RSS link
    │   ├── Header.astro       # Sticky nav with GGG mark + YouTube CTA
    │   ├── Footer.astro       # Channel link, RSS link, copyright
    │   ├── HeaderLink.astro   # Internal nav link with active-state underline
    │   └── FormattedDate.astro
    ├── layouts/
    │   └── BlogPost.astro     # Post template: YouTube embed → title → byline → tags → body → CTA
    ├── pages/
    │   ├── index.astro        # Homepage with hero + 6 most-recent post cards
    │   ├── about.astro
    │   ├── rss.xml.js         # RSS feed generator
    │   └── blog/
    │       ├── index.astro    # All posts list
    │       └── [...slug].astro
    └── content/
        └── blog/              # Posts live here as `.md` files; filename = URL slug
            └── *.md
```

## How to add a new post

The steady-state workflow for a transcript-derived post:

1. **Pick a video.** From the technical-content manifest (~115 candidates), select one to write up. *(Note: as of April 2026 the back-catalog is essentially done; see `CLAUDE.md` § "Picking candidates from the queue.")*
2. **Pull metadata + transcript** with `yt-dlp` from the sandbox. The exact invocation requires the `--js-runtimes "node:..."` flag (without it, subtitles fail silently) — see `CLAUDE.md` § "Workflow for a new transcript-derived post" for the working command. Don't re-derive it from yt-dlp's docs; the sandbox-specific quirks are worked out there.
3. **Pull the YouTube thumbnail** the same way (see `CLAUDE.md`). The thumbnail downloads as `.webp` because ffmpeg isn't in the sandbox; `CLAUDE.md` shows the PIL one-liner that converts it.
4. **Research backstory.** Web-search the relevant components, history, related techniques, canonical references (datasheets, library docs, foundational forum threads).
5. **Draft the post** at `src/content/blog/{slug}.md` with the frontmatter described below. Match the voice notes in `CLAUDE.md`.
6. **Verify with a build.** Build inside a fresh `/tmp` clone, not the workspace — the sandbox can't replace cached files in the workspace's `node_modules`. See `CLAUDE.md` § "Sandbox filesystem limitation."
7. **Commit and push** from the same `/tmp` clone (see "Auth & push workflow" below).
8. **Cloudflare auto-deploys** in ~60 seconds. Verify at the live URL.

## Post frontmatter schema

Defined in `src/content.config.ts`. Each `.md` file in `src/content/blog/` must have:

```yaml
---
title: 'String'                  # Required. Used for <h1>, <title>, OG card, post listings
description: 'String'            # Required. Used for OG description and post-card excerpt
pubDate: 'August 19 2012'        # Required. Backdate to the original YouTube upload.
                                 # Canonical format: 'Month DD YYYY' in single quotes,
                                 # space-separated, no leading zero on the day.
                                 # The schema uses z.coerce.date() so other formats parse,
                                 # but stick to this one for consistency.
youtubeId: 'cnOKG0fvZ4w'         # Optional. 11-char video ID — embeds video at top of post
heroImage: '../../assets/posts/{slug}/thumbnail.jpg'  # Optional. Used for OG/social card image
tags: ['arduino', 'servo']       # Optional. Renders as #tag pills under the byline
updatedDate: '...'               # Optional. Shown as "Last updated on X" if present
---
```

**Behavior of optional fields:**

- If `youtubeId` is present, the post page shows the YouTube embed at the top *instead of* `heroImage` (they're mutually exclusive in the post layout).
- If `heroImage` is present, it's used as the OG/social-card image when someone shares the URL — even when the post page itself shows the video embed.
- Best practice for transcript-derived posts: set both `youtubeId` (for the in-page embed) AND `heroImage` to the YouTube thumbnail (for the OG card).

## Build settings (Cloudflare Pages)

These are configured once in the Cloudflare dashboard at *Workers & Pages → garage-geek-guy → Settings*:

| Setting | Value |
| --- | --- |
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Production branch | `main` |
| Root directory | (project root, default) |

Auto-deploys are enabled. Every push to `main` triggers a fresh build.

## Branding & voice

**Visual:**
- Dark backgrounds (`#0F0F10` page, `#18181A` surfaces)
- Electric yellow accent `#FFD600` matching the GGG circuit-board logo
- Atkinson Hyperlegible font (high-readability, accessibility-friendly)
- "GGG" in a yellow rounded-square mark serves as the temporary logo

**Author:** byline shows as `GGG` (set in `src/consts.ts`).

**Voice for transcript-derived posts:** see `CLAUDE.md`. Short version: friendly, hands-on, specific. Like a knowledgeable friend at the bench, not a textbook or marketing copy.

## Auth & push workflow

**Two paths exist.** Claude in Cowork mode uses Option B (PAT-based CLI). Option A is for Lonnie working manually at the keyboard. AI agents can ignore Option A.

### Option A — GitHub Desktop (GUI, for Lonnie's manual work)

GitHub Desktop is installed and signed in as `lonnie-developer`. Workflow:

1. Open GitHub Desktop.
2. It shows changed files in the Blog project repo automatically.
3. Type a commit summary, click **Commit to main**.
4. Click **Push origin**.

This is the "no-token-needed" path — GitHub Desktop handles auth via macOS Keychain.

### Option B — Command-line push from the sandbox (Claude in Cowork)

For batch work, Claude pushes directly from the sandbox using a fine-grained Personal Access Token. The token is:

- Scoped to **only** the `garage-geek-guy` repository
- Permissions: **Contents: Read and write** + **Metadata: Read** (auto)
- 90-day expiration; rotate before it lapses
- Working credential at `~/.git-credentials` inside the sandbox (mode 0600), set with `git config --global credential.helper store`
- Persistent backup at `~/Library/Application Support/Claude/.../memory/github_pat_garage_geek_guy.md` on Lonnie's Mac (not in the project repo, not committed anywhere)
- Revocable from [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens) at any time

The persistent backup is the source of truth. If a new Cowork session starts with no credentials configured in the sandbox, Claude reads the memory-stored token and re-bootstraps `~/.git-credentials` automatically — no need to re-paste the PAT.

The project `.gitignore` defensively excludes `.git-credentials`, `*.pat`, `*.token`, `.netrc`, and `secrets/` as a safety net so credential files can never be accidentally committed.

To rotate the token:
1. Generate a new fine-grained PAT at the URL above with the same scope (only `garage-geek-guy`, Contents:read+write).
2. Paste it into chat with Claude.
3. Claude updates both the sandbox credentials file *and* the persistent backup memory file.
4. Revoke the old token from GitHub Settings.

## Local development (rare, but documented)

If you ever want to preview locally without pushing:

```
cd "/Users/lonniehoneycutt/Documents/Claude/Projects/Blog project"
npm install     # first time only
npm run dev     # serves at http://localhost:4321 with hot reload
npm run build   # produces dist/ — same output Cloudflare builds
npm run preview # serves the built site at http://localhost:4321
```

These commands run in Terminal. The point of the rest of the setup is that you don't have to.

## Troubleshooting

**Build fails on Cloudflare but passes locally** — usually a Node version mismatch. The repo's `package.json` declares `engines.node >= 22.12.0`. If Cloudflare's default has drifted, set `NODE_VERSION=22` as a build environment variable in Cloudflare project settings.

**A post's pubDate doesn't sort correctly** — use the canonical format `'Month DD YYYY'` (e.g. `'August 19 2012'`). The schema uses `z.coerce.date()` and accepts other shapes, but mixed formats across posts have caused sort surprises in the past. Stick to one format.

**`npm run build` fails with `EPERM ... unlink ...`** — you're running it inside the workspace folder. The sandbox can't delete files there, and Vite needs to refresh its cache. Build inside a fresh `/tmp` clone instead. See `CLAUDE.md` § "Sandbox filesystem limitation."

**Pagefind reports "Indexed 0 pages" or unexpectedly few pages** — the `<article data-pagefind-body>` wrapper in `src/layouts/BlogPost.astro` was moved or removed. Pagefind only indexes content inside that wrapper. Healthy index for this site is around 107 pages, 6800+ words.

**A YouTube embed fails to load on the live site** — confirm the `youtubeId` is the 11-char ID from the URL (the `v=` parameter), not the full URL or the channel handle.

**`yt-dlp` rate-limit errors** — YouTube throttles bursts. If you hit it, wait 15-30 minutes and retry, or add `--sleep-interval 5` between requests when batching.

**Lost the GitHub Desktop sign-in** — re-sign in via the in-app prompt. The repo will reconnect automatically; no need to re-clone.

## Project history (decisions and why)

| Date | Decision | Why |
| --- | --- | --- |
| 2026-04-28 | Astro + Cloudflare Pages + GitHub | Free was a hard requirement; static site over Hashnode/Blogger/WordPress for best automation hooks, full ownership, no platform risk |
| 2026-04-28 | No custom domain initially | Defer the $10/yr cost; pages.dev subdomain works fine to start |
| 2026-04-28 | YouTube auto-captions for transcripts | Sufficient for our writing process; no need to build a manual transcript pipeline |
| 2026-04-28 | YouTube thumbnail as `heroImage` | Cleaner OG/social cards than a generic placeholder; matches the channel visually |
| 2026-04-28 | First pilot post: TowerPro MG995 servo hack | Strong evergreen content (106k views), clear backstory potential (Boe-Bot history), tests the full template |
| 2026-04-28 | Voice locked: friendly, hands-on, specific | "Knowledgeable friend at the bench" — see CLAUDE.md for full notes |
| 2026-04-28 | PAT-based CLI push for batch work | Faster than GitHub Desktop dance for 30+ post production runs |

## Future improvements (parked)

- Custom domain (resolves OG/canonical URL, looks more "real")
- Replace the text "GGG" mark with the actual circuit-board logo image
- Replace the default Astro favicon with a GGG-branded one
- Replace `blog-placeholder-1.jpg` (the generic OG fallback) with a GGG-branded fallback graphic
- Add tag pages (`/tags/arduino` etc.) listing all posts with that tag
- Newsletter signup integration (Buttondown? Listmonk? — TBD)
