#!/usr/bin/env python3
"""
Refresh the in-repo video manifest from the Garage Geek Guy YouTube channel.

Writes two files into ../data/:
  - videos.tsv               every video on the channel
  - technical-candidates.tsv subset that passes the technical-content filter

Both files are sorted by video ID for stable git diffs. Run this whenever the
channel has new uploads (or the filter rules change), then commit the diff.

Schema (both files, with header row):
  id<TAB>title<TAB>duration_seconds

Notes on what is NOT in the manifest, deliberately:
  - upload_date / pubDate: yt-dlp's --flat-playlist does not return it; pulling
    per-video metadata for all 740 videos would take ~10 minutes. The
    post-drafting workflow pulls upload_date on demand for the one video being
    written about, which is enough.
  - description, tags, view_count: too much churn, too little payoff.

Requires yt-dlp installed and on PATH (or at ~/.local/bin/yt-dlp). The session
bootstrap in CLAUDE.md handles installation.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@garagegeekguy/videos"

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
ALL_VIDEOS_FILE = DATA_DIR / "videos.tsv"
TECH_CANDIDATES_FILE = DATA_DIR / "technical-candidates.tsv"

HEADER = "id\ttitle\tduration_seconds\n"

# ---------------------------------------------------------------------------
# Technical-content filter
# ---------------------------------------------------------------------------
# A video is a "technical candidate" if its title matches at least one INCLUDE
# pattern AND no EXCLUDE pattern. The bar to clear is "could plausibly become a
# tutorial-style post with parts list, build steps, and a gotcha section" — not
# "mentions a piece of technology." That's why toy demos and collectibles are
# filtered out even when they match a keyword like "robot" or "electronic".
#
# When you tweak these, re-run the script and review the diff. Borderline cases
# are fine — the queue-status script lists candidates and you pick by hand.

INCLUDE_PATTERNS = [
    # microcontrollers and dev boards
    r"\barduino\b", r"\braspberry pi\b", r"\bpicaxe\b", r"\batmega\b", r"\batmel\b",
    r"\besp\d+\b", r"\bbasic ?stamp\b", r"\bboe[- ]?bot\b", r"\bpropeller chip\b",
    r"\bmsp430\b", r"\blaunchpad\b", r"\bbeagle ?bone\b", r"\bteensy\b",
    r"\bmicrocontroller\b", r"\bmicroprocessor\b",
    # benchwork
    r"\bbreadboard\b", r"\bsoldering?\b", r"\bdesolder", r"\bpcb\b",
    r"\boscilloscope\b", r"\bmultimeter\b", r"\blogic analy[sz]er\b",
    # components
    r"\bservo\b", r"\bstepper motor\b", r"\bdc motor\b", r"\bencoder\b",
    r"\boled\b", r"\b7[- ]?segment\b",
    r"\brelay\b", r"\bregulator\b", r"\bpower supply\b",
    r"\bi2c\b", r"\bspi\b", r"\buart\b", r"\bxbee\b", r"\bzigbee\b", r"\bnrf24",
    # actions that signal a build/teach post
    r"\bhack\b", r"\bteardown\b", r"\bdiy\b", r"\bbuild\b", r"\bproject\b",
    r"\btutorial\b", r"\bhow[- ]?to\b",
    r"\b3d print", r"\bcnc\b",
    # specific topics that have produced posts or are clear candidates
    r"\bham radio\b", r"\bcb radio\b", r"\bat command\b", r"\bmodem\b",
    r"\bschematic\b", r"\bcircuit\b", r"\bfirmware\b", r"\bsketch\b",
    r"\brobot\b", r"\bdrone\b", r"\bquadcopter\b",
]

# Filtered OUT even when a title matches an include pattern. The channel has a
# large vintage-toy / collectibles bucket where titles often contain words like
# "robot" or "electronic" but the video is a hands-on demo of a finished
# product, not a buildable project.
EXCLUDE_PATTERNS = [
    r"\bunboxing\b",
    r"\btrading cards?\b", r"\bcard (lot|set)\b", r"\bbombshells\b", r"\bdonruss\b",
    r"\bmusic box\b", r"\bsnow globe\b",
    r"\bplayset\b", r"\bplush\b", r"\baction figure\b", r"\bvoice[- ]changing\b",
    r"\bminifigures?\b", r"\blego (chrome|star wars|minifig)",
    r"\btoy demo\b", r"\bfigure demo\b",
    r"\b(transformers? optimus|gobots|tonka|hasbro|fisher[- ]?price|disney)\b.*\bdemo\b",
]


def technical_filter(title: str) -> bool:
    """Return True if the title looks like a build/teach post candidate."""
    if any(re.search(p, title, re.IGNORECASE) for p in EXCLUDE_PATTERNS):
        return False
    return any(re.search(p, title, re.IGNORECASE) for p in INCLUDE_PATTERNS)


# ---------------------------------------------------------------------------
# yt-dlp invocation
# ---------------------------------------------------------------------------

def find_ytdlp() -> str:
    on_path = shutil.which("yt-dlp")
    if on_path:
        return on_path
    local = Path.home() / ".local" / "bin" / "yt-dlp"
    if local.exists():
        return str(local)
    sys.exit(
        "yt-dlp not found. Install with: "
        "pip install --break-system-packages yt-dlp"
    )


def fetch_videos() -> list[tuple[str, str, str]]:
    """Return list of (id, title, duration_seconds) for every video on the channel."""
    cmd = [
        find_ytdlp(),
        "--flat-playlist",
        # Use a delimiter that will not appear inside titles. The earlier
        # \t-in-template approach produced literal "\t" characters because
        # yt-dlp does not interpret backslash escapes in --print. We use the
        # ASCII unit-separator (0x1F) instead and split on it in Python.
        "--print", "%(id)s\x1f%(title)s\x1f%(duration)s",
        CHANNEL_URL,
    ]
    print(f"[refresh] running: yt-dlp --flat-playlist {CHANNEL_URL}", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    rows: list[tuple[str, str, str]] = []
    for line in proc.stdout.splitlines():
        if not line:
            continue
        parts = line.split("\x1f")
        if len(parts) != 3:
            print(f"[refresh] skipping malformed row: {line!r}", file=sys.stderr)
            continue
        vid, title, dur = parts
        # Normalize: strip whitespace, replace any embedded tabs/newlines in the
        # title (rare but possible) so the TSV stays well-formed.
        title = re.sub(r"\s+", " ", title).strip()
        rows.append((vid, title, dur))
    return rows


def write_tsv(path: Path, rows: list[tuple[str, str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows_sorted = sorted(rows, key=lambda r: r[0])
    with path.open("w", encoding="utf-8") as f:
        f.write(HEADER)
        for vid, title, dur in rows_sorted:
            f.write(f"{vid}\t{title}\t{dur}\n")


def main() -> int:
    rows = fetch_videos()
    if not rows:
        print("[refresh] no videos returned — aborting (will not overwrite manifest)", file=sys.stderr)
        return 1

    write_tsv(ALL_VIDEOS_FILE, rows)
    tech = [r for r in rows if technical_filter(r[1])]
    write_tsv(TECH_CANDIDATES_FILE, tech)

    print(f"[refresh] wrote {len(rows)} rows to {ALL_VIDEOS_FILE.relative_to(REPO_ROOT)}")
    print(f"[refresh] wrote {len(tech)} rows to {TECH_CANDIDATES_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
