# The Glade — Design

Resources for setting up the Claude Design system for The Glade campaign.

| File                  | What it is                                                       | Feed to Claude Design |
|-----------------------|------------------------------------------------------------------|-----------------------|
| `brand-brief.md`      | Tone, voice, audience, mood references. The "why."               | Yes, first.           |
| `design-system.md`    | Palette (hex), typography, motifs, components. The "how."        | Yes, alongside brief. |
| `wordmark.md`         | Wordmark concept, sizes, working prompt. The "mark."             | Yes, after the system is approved. |

## Setup workflow

1. Review `brand-brief.md` — adjust tone or references before any design work starts.
2. Review `design-system.md` — sign off on palette, type, and the two component patterns (stat block, NPC card).
3. In Claude Design, attach the brief + system spec, plus the reference image set listed at the bottom of `design-system.md`.
4. First test: have Claude Design produce a **stat block** and an **NPC card**. These two artifacts are the smoke test for the whole system.
5. Once those two read correctly, generate the wordmark using the prompt at the bottom of `wordmark.md`.
6. Iterate.

## Theme summary

Dark fantasy at insect scale. Miyazaki whimsy on one end, Del Toro horror on the other. Default sits dead center, leaning slightly gothic. Bugs are real bugs, not anthropomorphized. Color encodes seasonal zones (amber, frost, pitch, cordyceps, pollen, lichen). Screen-first, dark-default. One accent per page.
