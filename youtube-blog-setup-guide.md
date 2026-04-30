# YouTube Channel → Blog Setup Guide
### Instructions for an AI Agent

---

> ⚠️ **ARCHIVED — DO NOT FOLLOW THIS DOCUMENT FOR ROUTINE WORK.**
>
> This was the bootstrap guide used to *initially scaffold* the Garage Geek Guy blog from scratch in April 2026. The site is built. The Astro project is set up. Cloudflare Pages is connected. None of the Phase 0 / Phase 1 / Phase 2 instructions below need to be re-run.
>
> **For ongoing work on this blog, read these instead:**
> - [`CLAUDE.md`](./CLAUDE.md) — session bootstrap, post workflow, voice notes, sandbox quirks
> - [`SETUP.md`](./SETUP.md) — operations reference, accounts, troubleshooting
> - [`README.md`](./README.md) — project overview
>
> This file is kept only as a record of how the project was originally created, in case the same template is ever applied to a different YouTube channel. Treat it as historical reference, not as a procedure.

---

This document tells you, an AI assistant, how to build a fully automated YouTube-to-blog pipeline from scratch for any YouTube channel. You are creating an Astro static site hosted on Cloudflare Pages that publishes written companion posts for YouTube videos, derived from video transcripts.

**The only question you need to ask to get started:**

> "What is the URL to your YouTube channel?"

Everything else can be derived from that URL or gathered with light follow-up questions as needed during setup. The sections below are written for you — the AI — as procedural instructions.

---

## Phase 0: Gather information

**Ask the user:** "What is the URL to your YouTube channel?"

From the channel URL, visit the channel (or use a web search) to collect:

- **Channel name** — the display name (e.g., "Garage Geek Guy")
- **Channel handle** — the `@handle` (e.g., `@garagegeekguy`)
- **Channel description** — what the channel is about (1-2 sentences)
- **Video count** — roughly how many videos exist
- **Content type** — what kind of content (tutorials, reviews, vlogs, builds, cooking, etc.)

Then ask the user these follow-up questions (you can ask all at once, one message):

1. **Repo/site name:** "What would you like to name the blog? This becomes the GitHub repo name and the site URL slug (e.g., `garage-geek-guy` → `garage-geek-guy.pages.dev`). Lowercase, hyphens only."
2. **Author name:** "How should posts be bylined? Can be your name, initials, or a brand abbreviation (e.g., `GGG`, `Alex`, `TechWithTom`)."
3. **GitHub username:** "What is your GitHub username? (This is where the repo will be created.)"
4. **Site tagline:** "One-line tagline for the site — shown under the site title on the homepage. Keep it short and specific (e.g., `Hands-on electronics and DIY from the workshop.`)."
5. **Accent color:** "Do you have a brand color in mind for the site? (Optional — if you say no, I'll use a clean default. Hex or color name both work.)"

Once you have all of the above, proceed. Do not wait — build the project now.

---

## Phase 1: Scaffold the Astro project

### 1.1 Create the project directory and initialize

The user will need Node.js ≥ 22 installed. Run this to scaffold a blank Astro project:

```bash
npm create astro@latest {REPO_SLUG} -- --template blog --no-install --no-git
cd {REPO_SLUG}
npm install
```

> **Note:** The Astro blog starter template gives you the right bones. You'll replace its placeholder content with the customized files below.

Alternatively, if scaffolding interactively isn't possible (e.g., you're building the files directly), create the directory and write each file listed in Phase 2 manually. The full file tree is specified there.

### 1.2 Replace `package.json`

```json
{
  "name": "{REPO_SLUG}",
  "type": "module",
  "version": "0.0.1",
  "private": true,
  "engines": {
    "node": ">=22.12.0"
  },
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "@astrojs/mdx": "^5.0.4",
    "@astrojs/rss": "^4.0.18",
    "@astrojs/sitemap": "^3.7.2",
    "astro": "^6.1.10",
    "sharp": "^0.34.3"
  }
}
```

Run `npm install` after writing this file.

---

## Phase 2: Write all source files

Replace all placeholders in curly braces with the values gathered in Phase 0.

| Placeholder | Example value |
|---|---|
| `{REPO_SLUG}` | `garage-geek-guy` |
| `{SITE_TITLE}` | `Garage Geek Guy` |
| `{SITE_DESCRIPTION}` | `Electronics, Arduino, and DIY projects from the workshop. Companion blog to the Garage Geek Guy YouTube channel.` |
| `{SITE_TAGLINE}` | `Hands-on electronics and DIY from the workshop.` |
| `{AUTHOR}` | `GGG` |
| `{CHANNEL_NAME}` | `Garage Geek Guy` |
| `{CHANNEL_URL}` | `https://www.youtube.com/@garagegeekguy` |
| `{CHANNEL_HANDLE}` | `@garagegeekguy` |
| `{ACCENT_COLOR}` | `#FFD600` |
| `{PAGES_DEV_URL}` | `https://{REPO_SLUG}.pages.dev` |
| `{ABOUT_DATE}` | Today's date in format `Month DD YYYY` |

### `astro.config.mjs`

```js
// @ts-check
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  // Update this to your custom domain once you have one.
  site: '{PAGES_DEV_URL}',
  integrations: [mdx(), sitemap()],
  fonts: [
    {
      provider: fontProviders.local(),
      name: 'Atkinson',
      cssVariable: '--font-atkinson',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          {
            src: ['./src/assets/fonts/atkinson-regular.woff'],
            weight: 400,
            style: 'normal',
            display: 'swap',
          },
          {
            src: ['./src/assets/fonts/atkinson-bold.woff'],
            weight: 700,
            style: 'normal',
            display: 'swap',
          },
        ],
      },
    },
  ],
});
```

### `tsconfig.json`

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

### `.gitignore`

```
# build output
dist/
.output/

# generated types
.astro/

# dependencies
node_modules/

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# environment variables
.env
.env.*
!.env.example

# macOS
.DS_Store

# thumbnails downloaded by yt-dlp (webp originals not committed)
*.webp

# credentials — never commit these
.git-credentials
*.pat
*.token
.netrc
secrets/
```

### `src/consts.ts`

```ts
// Site-wide constants.
// Edit these values to update the site title, description, and channel links everywhere.

export const SITE_TITLE = '{SITE_TITLE}';
export const SITE_DESCRIPTION = '{SITE_DESCRIPTION}';
export const SITE_TAGLINE = '{SITE_TAGLINE}';

export const AUTHOR = '{AUTHOR}';
export const CHANNEL_NAME = '{CHANNEL_NAME}';
export const CHANNEL_URL = '{CHANNEL_URL}';
export const CHANNEL_HANDLE = '{CHANNEL_HANDLE}';
```

### `src/content.config.ts`

```ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      heroImage: z.optional(image()),
      // Optional YouTube video ID for embedding the source video.
      // Example: for https://www.youtube.com/watch?v=dQw4w9WgXcQ set youtubeId: 'dQw4w9WgXcQ'
      youtubeId: z.string().optional(),
      // Optional tags for categorizing posts.
      tags: z.array(z.string()).optional(),
    }),
});

export const collections = { blog };
```

### `src/styles/global.css`

Use the user's accent color for `--accent`. If none provided, use `#0ea5e9` (a clean sky blue that works on dark backgrounds).

```css
:root {
  --accent: {ACCENT_COLOR};
  --accent-dark: color-mix(in srgb, {ACCENT_COLOR} 70%, black);
  --accent-soft: color-mix(in srgb, {ACCENT_COLOR} 15%, transparent);

  --bg: #0f0f10;
  --surface: #18181a;
  --surface-2: #232325;
  --border: #2c2c2f;

  --text: #ececec;
  --text-muted: #a3a3a8;
  --text-faint: #6f6f74;

  --black: 236, 236, 236;
  --gray: 163, 163, 168;
  --gray-light: 44, 44, 47;
  --gray-dark: 236, 236, 236;
  --gray-gradient: rgba(24, 24, 26, 0.6), var(--bg);
  --box-shadow:
    0 2px 6px rgba(0, 0, 0, 0.45),
    0 8px 24px rgba(0, 0, 0, 0.5),
    0 16px 32px rgba(0, 0, 0, 0.55);
}

body {
  font-family: var(--font-atkinson);
  margin: 0;
  padding: 0;
  text-align: left;
  background: var(--bg);
  background-image:
    radial-gradient(at 0% 0%, var(--accent-soft) 0px, transparent 50%),
    radial-gradient(at 100% 0%, color-mix(in srgb, var(--accent) 3%, transparent) 0px, transparent 50%);
  background-attachment: fixed;
  word-wrap: break-word;
  overflow-wrap: break-word;
  color: var(--text);
  font-size: 20px;
  line-height: 1.7;
}
main {
  width: 720px;
  max-width: calc(100% - 2em);
  margin: auto;
  padding: 3em 1em;
}
h1, h2, h3, h4, h5, h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text);
  line-height: 1.2;
}
h1 { font-size: 3.052em; }
h2 { font-size: 2.441em; }
h3 { font-size: 1.953em; }
h4 { font-size: 1.563em; }
h5 { font-size: 1.25em; }
strong, b { font-weight: 700; color: #fff; }
a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.15s ease, color 0.15s ease;
}
a:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
p { margin-bottom: 1em; color: var(--text); }
.prose p { margin-bottom: 1.5em; }
textarea { width: 100%; font-size: 16px; }
input { font-size: 16px; }
table { width: 100%; }
img { max-width: 100%; height: auto; border-radius: 8px; }
code {
  padding: 2px 6px;
  background-color: var(--surface);
  color: var(--accent);
  border: 1px solid var(--border);
  border-radius: 3px;
  font-size: 0.9em;
}
pre {
  padding: 1.5em;
  border-radius: 8px;
  background-color: var(--surface) !important;
  border: 1px solid var(--border);
  overflow-x: auto;
}
pre > code { all: unset; color: var(--text); }
blockquote {
  border-left: 4px solid var(--accent);
  background: var(--surface);
  padding: 1em 1.5em;
  margin: 1.5em 0;
  font-size: 1.1em;
  border-radius: 0 8px 8px 0;
  color: var(--text-muted);
}
hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }
::selection { background: var(--accent); color: #000; }
@media (max-width: 720px) {
  body { font-size: 18px; }
  main { padding: 1em; }
  h1 { font-size: 2.4em; }
}
.sr-only {
  border: 0; padding: 0; margin: 0;
  position: absolute !important;
  height: 1px; width: 1px; overflow: hidden;
  clip: rect(1px 1px 1px 1px);
  clip-path: inset(50%);
  white-space: nowrap;
}

/* Channel CTA button */
.btn-watch {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  background: var(--accent);
  color: #000;
  padding: 0.7em 1.2em;
  border-radius: 6px;
  font-weight: 700;
  text-decoration: none;
  border: none;
  transition: transform 0.1s ease, box-shadow 0.15s ease;
}
.btn-watch:hover {
  color: #000;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px var(--accent-soft);
  border-bottom-color: transparent;
}

/* YouTube embed — responsive 16:9 */
.youtube-embed {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
  margin: 0 0 1.5em 0;
}
.youtube-embed iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

/* Tag pills */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  list-style: none;
  padding: 0;
  margin: 0.5em 0 0 0;
}
.tag-list li {
  background: var(--surface);
  color: var(--text-muted);
  padding: 0.2em 0.7em;
  border-radius: 999px;
  font-size: 0.8em;
  border: 1px solid var(--border);
}

/* Image placeholder utility — use when a real photo isn't ready yet */
.img-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2.5em 1.5em;
  margin: 1.5em 0;
  background: var(--surface);
  border: 2px dashed var(--accent);
  border-radius: 10px;
  color: var(--text-muted);
  font-size: 0.95em;
  line-height: 1.5;
}
.img-placeholder::before {
  content: "📷  IMAGE PLACEHOLDER";
  display: block;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.05em;
  font-size: 0.75em;
  margin-bottom: 0.5em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
```

### `src/components/BaseHead.astro`

```astro
---
import '../styles/global.css';
import type { ImageMetadata } from 'astro';
import { SITE_TITLE, SITE_DESCRIPTION } from '../consts';

interface Props {
  title: string;
  description: string;
  image?: ImageMetadata;
}
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const { title, description, image } = Astro.props;
---

<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<meta name="generator" content={Astro.generator} />
<link rel="canonical" href={canonicalURL} />
<link rel="sitemap" href="/sitemap-index.xml" />
<link rel="alternate" type="application/rss+xml" title={SITE_TITLE} href="/rss.xml" />

<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

<meta property="og:type" content="website" />
<meta property="og:url" content={Astro.url} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
{image && <meta property="og:image" content={new URL(image.src, Astro.url)} />}

<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:url" content={Astro.url} />
<meta property="twitter:title" content={title} />
<meta property="twitter:description" content={description} />
{image && <meta property="twitter:image" content={new URL(image.src, Astro.url)} />}
```

### `src/components/FormattedDate.astro`

```astro
---
interface Props {
  date: Date;
}
const { date } = Astro.props;
---
<time datetime={date.toISOString()}>
  {date.toLocaleDateString('en-us', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })}
</time>
```

### `src/components/HeaderLink.astro`

```astro
---
import type { HTMLAttributes } from 'astro/types';
type Props = HTMLAttributes<'a'>;
const { href, class: className, ...props } = Astro.props;
const { pathname } = Astro.url;
const isActive = href === pathname || href === pathname.replace(/\/$/, '');
---
<a href={href} class:list={[className, { active: isActive }]} {...props}>
  <slot />
</a>
```

### `src/components/Header.astro`

Replace `{SITE_TITLE}`, `{CHANNEL_URL}`, `{BRAND_INITIALS}` (short initials for the header badge, e.g. `GGG`), and `{CHANNEL_LABEL}` (e.g., `YouTube`).

```astro
---
import { SITE_TITLE, CHANNEL_URL } from '../consts';
import HeaderLink from './HeaderLink.astro';
const BRAND_INITIALS = '{BRAND_INITIALS}';
---
<header>
  <nav>
    <a class="brand" href="/">
      <span class="brand-mark" aria-hidden="true">{BRAND_INITIALS}</span>
      <span class="brand-name">{SITE_TITLE}</span>
    </a>
    <div class="internal-links">
      <HeaderLink href="/">Home</HeaderLink>
      <HeaderLink href="/blog">Blog</HeaderLink>
      <HeaderLink href="/about">About</HeaderLink>
    </div>
    <div class="social-links">
      <a href={CHANNEL_URL} target="_blank" rel="noopener" class="yt-link" aria-label="{SITE_TITLE} on YouTube">
        <svg viewBox="0 0 24 24" aria-hidden="true" width="28" height="28">
          <path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
        </svg>
        <span>YouTube</span>
      </a>
    </div>
  </nav>
</header>
<style>
  header {
    margin: 0; padding: 0 1.25em;
    background: rgba(15, 15, 16, 0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 10;
  }
  nav {
    display: flex; align-items: center;
    justify-content: space-between; gap: 1em;
    max-width: 1100px; margin: 0 auto;
  }
  .brand {
    display: flex; align-items: center; gap: 0.6em;
    padding: 0.85em 0; font-weight: 700;
    color: var(--text); border-bottom: none;
  }
  .brand:hover { color: var(--accent); border-bottom-color: transparent; }
  .brand-mark {
    display: inline-flex; align-items: center; justify-content: center;
    width: 2em; height: 2em; background: var(--accent); color: #000;
    border-radius: 6px; font-weight: 800; font-size: 0.85em; letter-spacing: 0.05em;
  }
  .brand-name { font-size: 1.05em; letter-spacing: 0.01em; }
  .internal-links { display: flex; gap: 0.25em; }
  nav a {
    padding: 1em 0.75em; color: var(--text-muted);
    border-bottom: 2px solid transparent; text-decoration: none;
  }
  nav a:hover { color: var(--accent); border-bottom-color: transparent; }
  nav a.active { color: var(--text); border-bottom-color: var(--accent); }
  .social-links { display: flex; }
  .yt-link {
    display: inline-flex; align-items: center; gap: 0.4em;
    padding: 0.4em 0.85em !important; background: transparent;
    border: 1px solid var(--border) !important; border-radius: 6px;
    color: var(--text-muted); font-size: 0.9em; font-weight: 600;
  }
  .yt-link:hover { color: #000 !important; background: var(--accent); border-color: var(--accent) !important; }
  @media (max-width: 720px) {
    .brand-name { display: none; }
    .yt-link span { display: none; }
    .yt-link { padding: 0.4em !important; }
  }
</style>
```

### `src/components/Footer.astro`

```astro
---
import { CHANNEL_URL, CHANNEL_HANDLE, SITE_TITLE } from '../consts';
const year = new Date().getFullYear();
---
<footer>
  <div>
    <a href={CHANNEL_URL} target="_blank" rel="noopener">{CHANNEL_HANDLE} on YouTube</a>
    <span> · </span>
    <a href="/rss.xml">RSS</a>
    <span> · </span>
    <span>© {year} {SITE_TITLE}</span>
  </div>
</footer>
<style>
  footer {
    padding: 2em 1em;
    border-top: 1px solid var(--border);
    text-align: center;
    font-size: 0.9em;
    color: var(--text-faint);
  }
  footer a { color: var(--text-muted); }
  footer a:hover { color: var(--accent); }
</style>
```

### `src/layouts/BlogPost.astro`

```astro
---
import { Image } from 'astro:assets';
import type { CollectionEntry } from 'astro:content';
import BaseHead from '../components/BaseHead.astro';
import Footer from '../components/Footer.astro';
import FormattedDate from '../components/FormattedDate.astro';
import Header from '../components/Header.astro';
import { AUTHOR, CHANNEL_URL } from '../consts';

type Props = CollectionEntry<'blog'>['data'];
const { title, description, pubDate, updatedDate, heroImage, youtubeId, tags } = Astro.props;
const watchUrl = youtubeId
  ? `https://www.youtube.com/watch?v=${youtubeId}`
  : CHANNEL_URL;
---
<html lang="en">
  <head>
    <BaseHead title={title} description={description} image={heroImage} />
    <style>
      main { width: calc(100% - 2em); max-width: 100%; margin: 0; padding: 0; }
      .hero-image { width: 100%; max-width: 1020px; margin: 1.5em auto 0 auto; padding: 0 1em; }
      .hero-image img { display: block; margin: 0 auto; border-radius: 12px; box-shadow: var(--box-shadow); }
      .video-wrap { width: 100%; max-width: 960px; margin: 1.5em auto 0 auto; padding: 0 1em; }
      .prose { width: 720px; max-width: calc(100% - 2em); margin: auto; padding: 1.5em 1em 3em 1em; color: var(--text); }
      .title { margin-bottom: 1.5em; padding: 1em 0; text-align: center; line-height: 1.1; }
      .title h1 { margin: 0 0 0.4em 0; }
      .byline { display: flex; gap: 0.6em; justify-content: center; align-items: center; flex-wrap: wrap; color: var(--text-muted); font-size: 0.95em; margin-bottom: 0.5em; }
      .byline .dot { color: var(--text-faint); }
      .byline .author { font-weight: 700; color: var(--accent); }
      .last-updated-on { font-style: italic; color: var(--text-faint); font-size: 0.9em; margin-top: 0.25em; }
      .cta-row { display: flex; justify-content: center; margin: 2.5em 0 1em 0; }
      .tags-block { margin-top: 1em; display: flex; justify-content: center; }
    </style>
  </head>
  <body>
    <Header />
    <main>
      <article>
        {youtubeId ? (
          <div class="video-wrap">
            <div class="youtube-embed">
              <iframe
                src={`https://www.youtube-nocookie.com/embed/${youtubeId}`}
                title={title} loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen
              />
            </div>
          </div>
        ) : heroImage ? (
          <div class="hero-image">
            <Image width={1020} height={510} src={heroImage} alt="" />
          </div>
        ) : null}
        <div class="prose">
          <div class="title">
            <h1>{title}</h1>
            <div class="byline">
              <span class="author">{AUTHOR}</span>
              <span class="dot">·</span>
              <FormattedDate date={pubDate} />
            </div>
            {updatedDate && (
              <div class="last-updated-on">
                Last updated <FormattedDate date={updatedDate} />
              </div>
            )}
            {tags && tags.length > 0 && (
              <div class="tags-block">
                <ul class="tag-list">
                  {tags.map((tag) => <li>#{tag}</li>)}
                </ul>
              </div>
            )}
            <hr />
          </div>
          <slot />
          <div class="cta-row">
            <a class="btn-watch" href={watchUrl} target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" aria-hidden="true" width="20" height="20">
                <path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              {youtubeId ? 'Watch on YouTube' : 'Subscribe on YouTube'}
            </a>
          </div>
        </div>
      </article>
    </main>
    <Footer />
  </body>
</html>
```

### `src/pages/index.astro`

```astro
---
import { getCollection } from 'astro:content';
import BaseHead from '../components/BaseHead.astro';
import Footer from '../components/Footer.astro';
import FormattedDate from '../components/FormattedDate.astro';
import Header from '../components/Header.astro';
import { SITE_DESCRIPTION, SITE_TITLE, SITE_TAGLINE, CHANNEL_URL, CHANNEL_HANDLE } from '../consts';

const BRAND_INITIALS = '{BRAND_INITIALS}';

const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
const recentPosts = posts.slice(0, 6);
---
<!doctype html>
<html lang="en">
  <head>
    <BaseHead title={SITE_TITLE} description={SITE_DESCRIPTION} />
    <style>
      .hero { text-align: center; padding: 4em 1em 3em 1em; border-bottom: 1px solid var(--border); background: radial-gradient(ellipse at top, var(--accent-soft), transparent 60%); }
      .hero-mark { display: inline-flex; align-items: center; justify-content: center; width: 5em; height: 5em; background: var(--accent); color: #000; border-radius: 14px; font-weight: 800; font-size: 1.4em; letter-spacing: 0.04em; margin-bottom: 0.8em; box-shadow: 0 8px 32px var(--accent-soft); }
      .hero h1 { font-size: 3em; margin: 0 0 0.3em 0; }
      .hero .tagline { color: var(--text-muted); font-size: 1.15em; max-width: 36em; margin: 0 auto 1.5em auto; }
      .hero-cta { display: inline-flex; gap: 0.75em; flex-wrap: wrap; justify-content: center; }
      .btn-secondary { display: inline-flex; align-items: center; gap: 0.5em; background: transparent; color: var(--text); padding: 0.7em 1.2em; border-radius: 6px; font-weight: 600; border: 1px solid var(--border); text-decoration: none; }
      .btn-secondary:hover { color: var(--accent); border-color: var(--accent); }
      .recent { max-width: 1100px; margin: 0 auto; padding: 3em 1em; }
      .recent-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.5em; gap: 1em; flex-wrap: wrap; }
      .recent-header h2 { font-size: 1.8em; margin: 0; }
      .recent-header a { color: var(--text-muted); font-size: 0.95em; }
      .recent-header a:hover { color: var(--accent); }
      .posts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25em; list-style: none; margin: 0; padding: 0; }
      .post-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; transition: transform 0.15s ease, border-color 0.15s ease; }
      .post-card:hover { transform: translateY(-2px); border-color: var(--accent); }
      .post-card a { display: block; padding: 1.25em; color: var(--text); text-decoration: none; border-bottom: none; }
      .post-card h3 { font-size: 1.15em; margin: 0 0 0.4em 0; line-height: 1.3; }
      .post-card .meta { font-size: 0.85em; color: var(--text-muted); margin: 0 0 0.6em 0; }
      .post-card .desc { font-size: 0.95em; color: var(--text-muted); margin: 0; line-height: 1.5; }
      .empty-state { text-align: center; padding: 3em 1em; color: var(--text-muted); background: var(--surface); border: 1px dashed var(--border); border-radius: 10px; }
    </style>
  </head>
  <body>
    <Header />
    <main>
      <section class="hero">
        <div class="hero-mark" aria-hidden="true">{BRAND_INITIALS}</div>
        <h1>{SITE_TITLE}</h1>
        <p class="tagline">{SITE_TAGLINE}</p>
        <div class="hero-cta">
          <a class="btn-watch" href={CHANNEL_URL} target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" aria-hidden="true" width="20" height="20">
              <path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            Subscribe on YouTube
          </a>
          <a class="btn-secondary" href="/blog">Read the blog →</a>
        </div>
      </section>
      <section class="recent">
        <div class="recent-header">
          <h2>Latest posts</h2>
          <a href="/blog">All posts →</a>
        </div>
        {recentPosts.length === 0 ? (
          <div class="empty-state">
            <p>No posts yet — check back soon.</p>
            <p style="font-size: 0.9em; color: var(--text-faint); margin: 0;">
              Latest videos: <a href={CHANNEL_URL} target="_blank" rel="noopener">{CHANNEL_HANDLE}</a>
            </p>
          </div>
        ) : (
          <ul class="posts-grid">
            {recentPosts.map((post) => (
              <li class="post-card">
                <a href={`/blog/${post.id}/`}>
                  <p class="meta"><FormattedDate date={post.data.pubDate} /></p>
                  <h3>{post.data.title}</h3>
                  <p class="desc">{post.data.description}</p>
                </a>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
    <Footer />
  </body>
</html>
```

### `src/pages/blog/index.astro`

```astro
---
import { getCollection } from 'astro:content';
import BaseHead from '../../components/BaseHead.astro';
import Footer from '../../components/Footer.astro';
import FormattedDate from '../../components/FormattedDate.astro';
import Header from '../../components/Header.astro';
import { SITE_TITLE } from '../../consts';

const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
---
<!doctype html>
<html lang="en">
  <head>
    <BaseHead title={`Blog — ${SITE_TITLE}`} description="All posts" />
  </head>
  <body>
    <Header />
    <main>
      <h1>All posts</h1>
      <ul style="list-style:none;padding:0;margin:0;">
        {posts.map((post) => (
          <li style="border-bottom:1px solid var(--border);padding:1.25em 0;">
            <a href={`/blog/${post.id}/`} style="color:var(--text);text-decoration:none;border:none;">
              <p style="font-size:0.85em;color:var(--text-muted);margin:0 0 0.3em 0;">
                <FormattedDate date={post.data.pubDate} />
              </p>
              <h2 style="font-size:1.3em;margin:0 0 0.3em 0;">{post.data.title}</h2>
              <p style="color:var(--text-muted);margin:0;font-size:0.95em;">{post.data.description}</p>
            </a>
          </li>
        ))}
      </ul>
    </main>
    <Footer />
  </body>
</html>
```

### `src/pages/blog/[...slug].astro`

```astro
---
import { getCollection, render } from 'astro:content';
import BlogPost from '../../layouts/BlogPost.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.id },
    props: post,
  }));
}
type Props = Awaited<ReturnType<typeof getStaticPaths>>[number]['props'];
const post = Astro.props;
const { Content } = await render(post);
---
<BlogPost {...post.data}>
  <Content />
</BlogPost>
```

### `src/pages/rss.xml.js`

```js
import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';

export async function GET(context) {
  const posts = await getCollection('blog');
  return rss({
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    site: context.site,
    items: posts.map((post) => ({
      ...post.data,
      link: `/blog/${post.id}/`,
    })),
  });
}
```

### `src/pages/about.astro`

Adapt the content below for the actual channel. Replace anything specific to Garage Geek Guy.

```astro
---
import Layout from '../layouts/BlogPost.astro';
import { CHANNEL_URL, CHANNEL_HANDLE, SITE_TITLE, SITE_DESCRIPTION } from '../consts';
---
<Layout
  title={`About ${SITE_TITLE}`}
  description={SITE_DESCRIPTION}
  pubDate={new Date('{ABOUT_DATE}')}
>
  <p>
    <strong>{SITE_TITLE}</strong> is a YouTube channel and companion blog. {SITE_DESCRIPTION}
  </p>

  <p>
    Each post here is a written companion to a video on the channel — for people who'd rather
    skim a build log, copy a code snippet, or revisit a reference later. The video is always
    embedded at the top of every post, so you can watch, read, or both.
  </p>

  <h2>Subscribe</h2>
  <p>
    New videos on the YouTube channel at <a href={CHANNEL_URL} target="_blank" rel="noopener">{CHANNEL_HANDLE}</a>.
    There's also an <a href="/rss.xml">RSS feed</a> if that's your thing.
  </p>
</Layout>
```

### `src/content/blog/welcome.md`

Write a real welcome post that reflects the actual channel. This placeholder gets the site live until the first proper transcript post is published.

```markdown
---
title: 'Welcome to the {SITE_TITLE} Blog'
description: 'A written companion to the {CHANNEL_NAME} YouTube channel. Build logs, tutorials, and notes from every video.'
pubDate: '{ABOUT_DATE}'
tags: ['welcome']
---

Welcome to the companion blog for [{CHANNEL_NAME}]({CHANNEL_URL}).

Each post here pairs with a video on the channel — embedded at the top, with extra context,
parts lists, code snippets, and links that don't fit in a video description.

New posts come out alongside new videos. Subscribe on YouTube if you want to follow along there,
or add the [RSS feed](/rss.xml) to your reader of choice.
```

### `public/favicon.svg`

A minimal branded favicon using the accent color. Replace the text with the brand initials.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="{ACCENT_COLOR}"/>
  <text x="16" y="22" font-family="system-ui,sans-serif" font-size="14" font-weight="800"
        text-anchor="middle" fill="#000">{BRAND_INITIALS}</text>
</svg>
```

### Fonts

Download Atkinson Hyperlegible (free, open license) from Google Fonts or the official source, and place:
- `src/assets/fonts/atkinson-regular.woff`
- `src/assets/fonts/atkinson-bold.woff`

Direct download URL (Google Fonts API):
```
https://fonts.gstatic.com/s/atkinsonhyperlegible/v11/9Bt23C1KxNDXMspQ1lPyU89-1h6ONRlW45G05LI.woff
https://fonts.gstatic.com/s/atkinsonhyperlegible/v11/9Bt73C1KxNDXMspQ1lPyU89-1h6ONRlW45G-5Lc.woff
```

Or use curl:
```bash
mkdir -p src/assets/fonts
curl -o src/assets/fonts/atkinson-regular.woff \
  "https://fonts.gstatic.com/s/atkinsonhyperlegible/v11/9Bt23C1KxNDXMspQ1lPyU89-1h6ONRlW45G05LI.woff"
curl -o src/assets/fonts/atkinson-bold.woff \
  "https://fonts.gstatic.com/s/atkinsonhyperlegible/v11/9Bt73C1KxNDXMspQ1lPyU89-1h6ONRlW45G-5Lc.woff"
```

---

## Phase 3: Verify the build locally

```bash
npm run build
```

The build must complete without errors before continuing. Common errors and fixes:

- **"Cannot find module 'sharp'"** → run `npm install sharp`
- **TypeScript errors in frontmatter** — check that your welcome post has all required fields (`title`, `description`, `pubDate`)
- **Font file missing** — verify both `.woff` files exist under `src/assets/fonts/`

---

## Phase 4: Create the GitHub repository

1. Go to [github.com/new](https://github.com/new) while signed in as the user's GitHub account.
2. Repository name: `{REPO_SLUG}`
3. Visibility: **Public** (required for Cloudflare Pages free tier to auto-deploy)
4. Do NOT initialize with README or .gitignore (you already have those)
5. Click **Create repository**

Then push the local project:

```bash
cd /path/to/{REPO_SLUG}
git init
git add .
git commit -m "Initial commit — Astro blog scaffold"
git branch -M main
git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_SLUG}.git
git push -u origin main
```

If the push requires authentication, use a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token
2. Scope: only this repo, permissions: **Contents: Read and write** + **Metadata: Read**
3. Use the token as the password when git prompts for credentials

---

## Phase 5: Connect Cloudflare Pages

1. Log in to [dash.cloudflare.com](https://dash.cloudflare.com) with the user's Cloudflare account
2. Go to **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
3. Authorize the GitHub App ("Cloudflare Workers and Pages") — grant access to **only** `{REPO_SLUG}`
4. Select the repo and configure:

| Setting | Value |
|---|---|
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Production branch | `main` |
| Root directory | (leave blank) |

5. Add one environment variable: `NODE_VERSION` = `22`
6. Click **Save and Deploy**

Cloudflare will build and deploy. After ~60 seconds the site will be live at:
`https://{REPO_SLUG}.pages.dev`

> **Important:** Copy that URL back into `astro.config.mjs` as the `site:` value, then commit and push again so the sitemap and RSS feed have the correct canonical URL.

---

## Phase 6: Write the first real post

This is where the ongoing work begins. The pattern for every post:

### Step 1 — Pick a video

Look at the channel's video list. For the first post, pick a video that:
- Has a substantial length (10+ minutes) — more transcript to work with
- Is a tutorial, build log, or how-to — not a vlog or announcement
- Has auto-generated captions enabled (most YouTube videos do)

### Step 2 — Pull transcript and metadata with yt-dlp

Install yt-dlp and Pillow (for thumbnail conversion):

```bash
pip install --quiet --break-system-packages yt-dlp Pillow
```

Pull the transcript and metadata:

```bash
VIDEO_ID="THE_11_CHAR_VIDEO_ID"
SLUG="your-post-slug-here"
NODE=$(which node)
YTDLP=$(which yt-dlp || echo "$HOME/.local/bin/yt-dlp")

# Pull metadata and auto-captions
$YTDLP --js-runtimes "node:$NODE" \
  --skip-download --write-auto-subs --sub-lang en --sub-format vtt \
  --print "ID: %(id)s" \
  --print "TITLE: %(title)s" \
  --print "UPLOAD: %(upload_date)s" \
  --print "DURATION: %(duration)s" \
  --print "TAGS: %(tags)s" \
  --print "DESC_BEGIN" --print "%(description)s" --print "DESC_END" \
  --output "/tmp/$SLUG" \
  "https://www.youtube.com/watch?v=$VIDEO_ID"

# Verify the VTT file was created
ls /tmp/$SLUG.en.vtt
```

> **Critical:** The `--js-runtimes "node:$NODE"` flag is required. Without it, yt-dlp ≥ 2025 silently produces no VTT files. If the VTT file is missing after the command runs, the flag was omitted or `node` wasn't found. Check `which node` — it should return a valid path.

Pull the thumbnail:

```bash
mkdir -p src/assets/posts/$SLUG
$YTDLP --js-runtimes "node:$NODE" \
  --skip-download --write-thumbnail \
  --output "src/assets/posts/$SLUG/thumbnail" \
  "https://www.youtube.com/watch?v=$VIDEO_ID"

# Convert .webp to .jpg (yt-dlp downloads webp regardless of --convert-thumbnails)
python3 -c "
from PIL import Image
img = Image.open('src/assets/posts/$SLUG/thumbnail.webp')
img.convert('RGB').save('src/assets/posts/$SLUG/thumbnail.jpg', 'JPEG', quality=90)
print('Converted thumbnail to JPEG')
"
```

### Step 3 — Clean the transcript

The raw VTT file has duplicate lines and inline timing tags. Clean it with:

```python
import re

with open('/tmp/SLUG.en.vtt', encoding='utf-8') as f:
    raw = f.read()

# Strip inline timing tags like <00:01:23.456><c>word</c>
lines = re.sub(r'<[^>]+>', '', raw).splitlines()

seen = set()
clean = []
for line in lines:
    line = line.strip()
    # Skip VTT headers, timestamps, and blank lines
    if re.match(r'WEBVTT|^\d+$|-->', line) or not line:
        continue
    if line not in seen:
        seen.add(line)
        clean.append(line)

transcript = ' '.join(clean)
print(transcript[:2000])  # preview the first 2000 chars
```

### Step 4 — Research the topic

Before drafting, do 2-3 web searches to find:
- Authoritative reference material (datasheets, official docs, specification pages)
- Historical context or backstory relevant to the topic
- 5-10 good reference links for the "References and further reading" section

### Step 5 — Draft the post

Create `src/content/blog/{SLUG}.md` with this frontmatter:

```yaml
---
title: 'Match or lightly improve on the YouTube title'
description: 'One-sentence hook, 150–250 characters. Doubles as the OG description.'
pubDate: 'Month DD YYYY'      # Use the original YouTube upload date — backdate exactly
youtubeId: '{VIDEO_ID}'
heroImage: '../../assets/posts/{SLUG}/thumbnail.jpg'
tags: ['tag1', 'tag2', 'tag3']
---
```

Then write the post body following the structure below.

### Post structure (adapt as the topic demands)

1. **Hook (1-2 paragraphs).** A framing that earns attention — a tradeoff, a counterintuitive fact, a question the reader didn't know they had.
2. **What this post covers (1 short paragraph).** Explicit promise. Good for SEO and reader orientation.
3. **Background.** What the thing is, specs if applicable, history, why it exists.
4. **Why it matters / why build or use it.** The motivation — bring in broader context where it adds value.
5. **What you'll need.** Parts list with model numbers and rough prices.
6. **The walkthrough.** Break into named subsections. Use short declarative sentences mixed with longer explanatory ones.
7. **The gotcha.** Surface the one thing nobody warns you about. Bold-headed paragraph or short subsection.
8. **Tips beyond the basics.** Edge cases, scaling, variations.
9. **Where this fits today (and where it doesn't).** Honest framing — when is this the right answer? When should you reach for something else?
10. **References and further reading.** 5-10 bullet points: datasheets, forum threads, library docs, Wikipedia. Mix authoritative and community sources.

**Length target:** 1500–2500 words for a typical 10-30 minute video.

### Voice guidelines

These apply regardless of what channel you're writing for. Adapt them to the channel's personality but keep the underlying principles.

**Write like a knowledgeable friend, not a textbook.** First-person plural for shared discovery ("we'll configure this next"), first-person singular for asides ("the first thing I do is..."). Short declarative sentences mixed with longer explanatory ones.

**Be specific.** "A $10 servo from eBay" beats "an inexpensive hobby servo." Use actual model numbers, actual specs from datasheets.

**Name gotchas before they bite.** The best tutorial writing surfaces the thing that trips up beginners before they get there, not after.

**Avoid:** corporate voice ("In today's fast-paced landscape..."), hedging ("you might want to consider possibly..."), bullet-list overload (bullets are for lists of items, not lists of thoughts), AI-tells like "delve," "robust," "leverage."

**Heading style:** sentence case (`## What you'll need`, not `## What You'll Need`).

### Step 6 — Build and verify

```bash
npm run build
```

If the build passes, commit and push:

```bash
git add src/content/blog/{SLUG}.md src/assets/posts/{SLUG}/thumbnail.jpg
git commit -m "Add post: {SLUG}"
git push origin main
```

Cloudflare auto-deploys in ~60 seconds. Verify the post at:
`https://{REPO_SLUG}.pages.dev/blog/{SLUG}/`

---

## Phase 7: Create a CLAUDE.md for the repo

Drop this file into the project root as `CLAUDE.md`. It tells future AI sessions what this project is and how to work in it. Fill in all placeholders.

```markdown
# Notes for AI assistants — {SITE_TITLE} blog

## What this project is

The blog is the written companion to the [{CHANNEL_NAME}]({CHANNEL_URL}) YouTube channel.
Each post is the written form of a video: video embedded at the top, then a polished
tutorial-style writeup that adds context, links, and research the video doesn't cover.

The goal is to convert the channel's video catalog into well-researched blog posts.
New videos get a post within a few days of upload.

## Stack

- **Framework:** Astro (static site generator)
- **Hosting:** Cloudflare Pages (free tier)
- **Repo:** github.com/{GITHUB_USERNAME}/{REPO_SLUG}
- **Live site:** {PAGES_DEV_URL}
- **Local clone:** (wherever the user has it)

## Session bootstrap (do this at the start of every fresh session)

1. Install yt-dlp:
   pip install --quiet --break-system-packages --no-warn-script-location yt-dlp Pillow

2. Configure git auth using the PAT stored in memory (see MEMORY.md).

3. Copy the project to /tmp before any git or build commands:
   cp -r "/path/to/local/clone" /tmp/blog-build
   cd /tmp/blog-build && git pull origin main

## Workflow for a new post

1. Pick a video from the channel.
2. Pull metadata + transcript with yt-dlp (--js-runtimes flag required).
3. Pull thumbnail, convert webp→jpg with PIL.
4. Clean the VTT transcript (strip timing tags, deduplicate lines).
5. Web-research the topic: specs, history, references.
6. Draft at src/content/blog/{slug}.md following the post structure.
7. Build to verify: cd /tmp/blog-build && npm run build
8. Commit and push from /tmp/blog-build.

## Voice

Knowledgeable friend, not textbook. Specific over abstract. Name gotchas before they bite.
Sentence case headings. Em-dashes are fine. Avoid AI-tells (delve, robust, leverage).
See the first published post for the calibration reference.

## Image policy

- YouTube thumbnail downloaded via yt-dlp → heroImage for OG card. ✓
- Self-made diagrams when they genuinely help. ✓
- AI-generated photos of equipment or setups. ✗
- Stock photography. ✗
```

---

## Ongoing workflow summary

For each new video:

1. Get the video URL or ID from the user (or pull the latest from the channel automatically)
2. Run the yt-dlp commands to fetch transcript + thumbnail
3. Research the topic (2-3 web searches)
4. Draft the post in `src/content/blog/{slug}.md`
5. Commit and push → Cloudflare auto-deploys

The entire pipeline from "here's a video URL" to "post is live" typically takes 30-60 minutes of AI work, with no manual steps required beyond approving the push.

---

## Troubleshooting

**yt-dlp produces no VTT file** — the `--js-runtimes "node:..."` flag was omitted or `node` isn't in PATH. Check `which node`, verify the path, and retry.

**Build fails on Cloudflare but passes locally** — Node version mismatch. Add environment variable `NODE_VERSION=22` in Cloudflare Pages settings.

**YouTube embed doesn't load** — confirm `youtubeId` is the 11-character ID from `?v=`, not the full URL.

**yt-dlp rate-limit errors** — wait 15-30 minutes, or add `--sleep-interval 5` for batch runs.

**pubDate sorts incorrectly** — use `Month DD YYYY` format (e.g., `August 19 2012`). Avoid `08/19/2012`.

**Git push fails from sandbox** — the sandbox cannot write to `.git/` in the workspace folder. Always copy to `/tmp` first and push from there.
```
