# The Glade — Design System Spec

The technical spec for setting up a design system in Claude Design. Pair with `brand-brief.md` (tone) and `wordmark.md` (logo).

Primary medium: **screen** (laptop and tablet at the table). Default theme: **dark**. A light/parchment variant is defined where it matters but is secondary.

---

## 1. Color palette

The palette has three layers: **grounds** (backgrounds and surfaces), **inks** (text and line), and **zone accents** (one chosen per page to encode mood and meaning). Each accent maps to a region or threat in the campaign world — color is functional, not just pretty.

### Grounds (dark default)

| Token            | Hex       | Role                                                  |
|------------------|-----------|-------------------------------------------------------|
| `loam`           | `#0F1410` | Page background. Near-black with a green undertone — the forest floor at night. |
| `moss-deep`      | `#1B2A24` | Primary surface (cards, panels).                      |
| `bark`           | `#2E2A24` | Warm-dark alternate surface (sidebars, inset panels). |
| `chamber`        | `#101814` | Deepest recess (combat actions inset, "lair" panels). |
| `silk-divider`   | `#3A3F38` | Hairline borders, dividers, table rules.              |

### Grounds (light / parchment variant — for occasional handouts)

| Token            | Hex       | Role                              |
|------------------|-----------|-----------------------------------|
| `bone`           | `#F5EFE0` | Page background, parchment.       |
| `chitin-light`   | `#E8DFCB` | Surface tint above bone.          |
| `spider-silk`    | `#D7D2C2` | Borders, dividers, watermark.     |

### Inks (text and line)

| Token         | Hex       | Role                                                  |
|---------------|-----------|-------------------------------------------------------|
| `chitin`      | `#E8DFCB` | Primary text on dark grounds. Warm bone-white.        |
| `chitin-dim`  | `#A89F89` | Secondary text, captions, labels.                     |
| `chitin-mute` | `#6E6856` | Tertiary text, footnotes, watermarks.                 |
| `loam-ink`    | `#1A1F18` | Primary text on light/parchment grounds.              |

### Zone accents — pick one per page

Each accent has both a "core" (use for ornament, rules, key callouts) and a "wash" (use for backgrounds, fills, large areas at low opacity). Color is keyed to the campaign's seasonal rings and major threats.

| Accent        | Core hex   | Wash hex   | Means                                                       | Use on                                  |
|---------------|------------|------------|-------------------------------------------------------------|-----------------------------------------|
| `amber`       | `#C77B2E`  | `#3B2415`  | Warmth, value, magic, the Antennington mine, civilization. | Default brand accent. Wordmark. NPC cards for friendly faces. Treasure. |
| `frost`       | `#9CC9C5`  | `#1F2E2E`  | The Bloom. Winter zone. Stillness, absence, the unnatural cold. | Anything in the winter zone. The Bloom itself. Encounters with eerie quiet. |
| `pitch`       | `#8B2A1F`  | `#2A1411`  | Blood, danger, Life Pitch currency, combat.                | Encounter sheets in active combat. HP indicators. Damage callouts. |
| `cordyceps`   | `#6B4A8C`  | `#1F1830`  | Corruption, fungal control, the fall zone, the big bad.    | Cordyceps-infected creatures. The fall zone. Spell-corruption effects. |
| `pollen`      | `#D9B84A`  | `#33280F`  | Whimsy, joy, the spring zone (where it's still safe), pollen drifts. | Friendly NPC cards. Spring-zone material. Comic-relief moments. |
| `lichen`      | `#7A8C5A`  | `#1E261A`  | Neutral midtone. Lore, history, the world before the Bloom. | Codex pages. Background lore. Default if no zone applies. |

**Pairing rule:** one accent per page, period. If a creature is cordyceps-infected *and* in the winter zone, the page picks one based on which fact is more important to the encounter. Never two accents at equal weight.

### Semantic tokens (UI roles)

| Token      | Maps to       | Used for                                |
|------------|---------------|-----------------------------------------|
| `--bg`     | `loam`        | Page background.                        |
| `--surface`| `moss-deep`   | Cards, panels.                          |
| `--surface-warm` | `bark`  | Inset panels, sidebars.                 |
| `--ink`    | `chitin`      | Body text.                              |
| `--ink-dim`| `chitin-dim`  | Secondary text.                         |
| `--rule`   | `silk-divider`| Borders and dividers.                   |
| `--accent` | (chosen zone) | Primary accent on the page.             |
| `--accent-wash` | (chosen zone wash) | Tinted backgrounds, callout fills.|
| `--danger` | `pitch.core`  | HP at zero, crit, lethal damage.        |
| `--good`   | `pollen.core` | Healing, allies, treasure found.        |

---

## 2. Typography

All four type families are free Google Fonts so they're easy to source in Claude Design.

| Role               | Family                | Weight          | Notes                                           |
|--------------------|-----------------------|-----------------|-------------------------------------------------|
| **Display / wordmark** | **IM Fell English**   | Regular, Italic | Slightly inky, almost-handlettered, woodcut feel. Gothic-storybook sweet spot. |
| **Headings**       | **EB Garamond**       | 400, 600, 700, italic | Old-world serif. H1–H3, creature names, section titles. Use small caps for level-2 headings. |
| **Body**           | **Lora**              | 400, 500, italic | Humanist serif, very screen-readable at 14–16px. Narrative text, descriptions, flavor. |
| **UI / labels**    | **Inter**             | 500, 600         | Clean sans for stat-block labels (HP, AC, SAVE), tabs, tags, badges. |
| **Numerals / dice**| **JetBrains Mono**    | 500              | Tabular figures for stat values (AC 14, +5, 2d6+3). Mono ensures alignment in dense blocks. |

### Type scale (screen, base 16px)

| Level     | Family / weight             | Size / line-height | Use                                  |
|-----------|-----------------------------|--------------------|--------------------------------------|
| Display   | IM Fell English Regular     | 56 / 1.05          | Wordmark, cover titles.              |
| H1        | EB Garamond 700             | 36 / 1.15          | Page title (creature name, encounter title). |
| H2        | EB Garamond 600 small caps  | 22 / 1.2           | Section headings.                    |
| H3        | EB Garamond 600             | 18 / 1.3           | Subsection (Actions, Reactions).     |
| Eyebrow   | Inter 600 tracked +0.08em uppercase | 11 / 1.2 | Tags above titles, label rows.       |
| Body      | Lora 400                    | 15 / 1.55          | Default reading text.                |
| Flavor    | Lora 400 italic             | 14 / 1.5           | Pull-quotes, in-world voice, NPC lines. |
| Stat label| Inter 600                   | 11 / 1.2 uppercase | "AC", "HP", "SPEED".                 |
| Stat value| JetBrains Mono 500          | 16 / 1.2           | "14", "47 (8d8 + 11)", "+5".         |
| Caption   | Lora 400                    | 12 / 1.4           | Footnotes, page meta.                |

### Typographic flourishes

- **Drop caps** on the first paragraph of long-form narrative (session recaps, NPC bios). Use IM Fell English at 4× line-height in `--accent` color.
- **Small caps** for level-2 headings and for the first 2–3 words of italicized flavor text leading a section.
- **Old-style figures** in body text (Lora supports them). **Tabular lining** figures in stat blocks (JetBrains Mono).
- **Drop caps occasionally substitute a beetle silhouette** for the initial letter — see motifs.

---

## 3. Iconography & motifs

A small library of motifs, used structurally (not decoratively). All should render cleanly at 16px and at 200px.

### Structural motifs

- **Hexagonal honeycomb cell** — frame for HP/AC roundels, portrait crops, stat tokens. Single cell, not a full grid.
- **Spider-silk thread** — hairline divider. A horizontal thread with a single dewdrop centered, optionally a tiny knot at one end. Color: `silk-divider` or `--accent` at 60% opacity.
- **Fiddlehead curl** — section-break ornament. A single unfurling fern frond, used at the center of dividers or as corner ornaments.
- **Beetle elytra outline** — the "shield" shape for character/creature card frames. Symmetric oval halves split by a vertical seam down the center.
- **Wing veining** — semi-transparent layer behind portraits or section titles. Reference: dragonfly or cicada wings, traced at ~12% opacity.
- **Frost crystal lacework** — for winter-zone material, used as a corner overlay or watermark.
- **Mushroom gill / fungal lattice** — for cordyceps / fall-zone material.
- **Pollen drift** — a scattering of tiny circles, used in spring-zone or whimsical pages.

### Icon set (semantic, ~16–24px)

| Icon              | Use                                     |
|-------------------|-----------------------------------------|
| Mandible pair     | Combat / actions                        |
| Antenna pair      | Perception / senses                     |
| Six-leg silhouette| Speed / movement                        |
| Curled wing       | Flying speed (boosted-jump rules)       |
| Drop of pitch (red bead) | HP / Life Pitch currency         |
| Amber chip        | Treasure / value                        |
| Spider silk knot  | Bind / restraint / web                  |
| Mushroom spot     | Cordyceps / corruption                  |
| Snowflake (six-arm)| Bloom / cold                           |
| Honeycomb cell    | Generic stat / token                    |

Style: **single-weight engraved line** (1.25–1.5px stroke at 24px), rounded joins, no fills. Like a Haeckel plate at icon scale.

### What to avoid

- No heraldry-clipart (no flat shields, swords, dragons).
- No 3D bevels, drop shadows, gradients on icons. Flat ink only.
- No emoji-style colored glyphs.
- No generic "fantasy frame" PNG borders. Frames are constructed from our motifs.

---

## 4. Layout primitives

### Spacing scale (4-px base)

`4, 8, 12, 16, 24, 32, 48, 64, 96` — pick from this set, never in between.

### Radii

- **Sharp** (`0`): default for cards and panels — gothic precision.
- **Soft** (`2px`): for tags, badges, inline pills.
- **Round** (`9999px`): for HP/AC roundels and icon chips only.

### Borders

- Default border: 1px `silk-divider`.
- Accent border (when a panel needs to read as the page's focal element): 1px `--accent` at 80% opacity, plus a 1px inner offset border at 20% to suggest a double-rule.
- No drop shadows. Depth comes from value contrast between `loam` / `moss-deep` / `bark`, not from blur.

### Density

DM-facing material is **dense but airy** — a stat block fits a lot of information, but every section is separated by at least 16px and a divider. Never crowd to fit.

---

## 5. Component patterns

The two primary components — designed to be the smoke test for the system.

### 5.1 Stat block / encounter sheet

**Goal:** a DM mid-combat finds AC, HP, key actions, and one tactical hook in under five seconds.

**Structure (top to bottom):**

1. **Eyebrow row** — Inter 600 small uppercase, tracked: `ZONE · ROLE · CR`. Color: `chitin-dim`. Example: `WINTER · SKIRMISHER · CR 3`.
2. **Title** — EB Garamond 700, creature name. Below it, italic Lora epithet: *"the wrenched-door bandit."*
3. **Accent rule** — 1px `--accent` line, full width, with a centered fiddlehead glyph in `--accent`.
4. **Top stat strip** — three honeycomb roundels: AC, HP, SPEED. Roundel = `bark` ground, `--accent` 1px border, JetBrains Mono value, Inter label below.
5. **Ability scores row** — six tight columns (STR/DEX/CON/INT/WIS/CHA). Inter label, JetBrains Mono value with modifier.
6. **Saves / skills / senses / languages** — single-paragraph block, Lora 14, with bold Inter labels inline.
7. **Traits** — H3 section, then bulleted list. Trait name in EB Garamond 600 italic, body in Lora.
8. **Actions** — H3 section. Each action: name in EB Garamond 600 italic, then attack/damage line in Lora, with all dice notation in JetBrains Mono. Inset on `chamber` ground (the deepest recess) to read as a separate compartment.
9. **Tactics footnote** — single italic Lora paragraph at the bottom, `chitin-dim`, prefixed with a small mandible icon. *"Opens with a thrown firepot. Will retreat below 1/3 HP."*

**Frame:** `moss-deep` card on `loam` page. 1px `--accent` border. Honeycomb cell as a watermark in the bottom-right corner at 6% opacity.

**Default accent:** `pitch` (combat). Override with `cordyceps` for infected creatures, `frost` for Bloom-touched, `amber` for hireable bugs.

### 5.2 NPC / creature card

**Goal:** a DM glances at a card and instantly knows *who* this is, *what they want*, and *how to play them* in 30 seconds.

**Layout:** two-column on tablet; portrait left (~40%), info right (~60%).

**Left column:**
- Portrait in a beetle-elytra frame — `bark` ground inside, 1px `--accent` border.
- Below the portrait: a **disposition strip** — three small chips in a row: `FACTION · DISPOSITION · STATUS`. Disposition uses color (pollen = friendly, frost = wary, pitch = hostile, lichen = neutral). Status icons: a small dot (alive), an "x" (dead), a "?" (missing).

**Right column:**
- **Eyebrow:** species and pronouns. `LEAFCUTTER ANT · SHE/HER`.
- **Name:** EB Garamond 700.
- **Epithet:** italic Lora. *"a worker who'd rather carry leaves than corpses."*
- **Voice quote:** a single italic line in IM Fell English, indented and offset by a left-side spider-silk thread. The line they'd say if you tapped the card.
- **Hooks** (3 short bullets): Inter labels (WANT / FEAR / HOOK), Lora bodies. Tight.
- **Notes:** a small free-form Lora paragraph at the bottom for DM-only context.

**Frame:** `moss-deep` card on `loam`. Pollen drift watermark in upper-left corner if disposition is friendly; frost lacework if wary; mushroom-gill if cordyceps-touched; nothing if neutral.

---

## 6. Light / parchment variant (handouts only)

When a page needs to feel like an in-world document (a torn note from Antennington, a Royal Jelly Society memo):

- Page: `bone`. Surface: `chitin-light`.
- Text: `loam-ink`.
- Accent: usually `amber` or `pitch` — readable on cream.
- Add a subtle paper grain (3–5% noise) and a single deckle-edge tear on one side.
- Wordmark or RJS sigil watermark in `spider-silk` at 8% opacity.

This variant is **secondary**. The dark default is the canonical look.

---

## 7. Accessibility & legibility floors

- Body text contrast: minimum 7:1 against its ground. `chitin` on `loam` ≈ 12:1 — good.
- Stat values must clear 7:1 even when colored with an accent — verify each accent against `moss-deep` before approving.
- Minimum interactive type size: 14px. Minimum stat-value size: 14px.
- Don't rely on color alone for status — pair every disposition color with an icon or text label.
- Italic flavor text never carries critical mechanical information.

---

## 8. What to feed Claude Design

When setting up the system in Claude Design, attach:

1. This file (`design-system.md`) and `brand-brief.md`.
2. The wordmark spec (`wordmark.md`) once approved.
3. A reference image set:
   - 2–3 Hollow Knight environment shots (deep-wood, City of Tears).
   - 1–2 Maria Sibylla Merian or Haeckel plates (creature-illustration tone).
   - 1 Mörk Borg or Mothership spread (zine layout confidence).
   - 1 Pan's Labyrinth still (warm-gothic candlelight palette).
4. Once the system generates a first stat block and NPC card, iterate on those two artifacts specifically — they are the smoke test.
