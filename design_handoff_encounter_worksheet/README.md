# Handoff — Encounter Worksheet redesign

## What this is

A redesign of the offline D&D 5e combat-encounter worksheet that the `/encounter-worksheet`
slash command produces via `scripts/build_encounter.py`. The reference HTML in
`reference/encounter-worksheet.html` is the **target output** — a self-contained, JS-driven
page seeded with an `ENCOUNTER = {...}` JSON object. Your job is to update
`scripts/build_encounter.py` (and the slash command markdown if needed) so that
running `python3 scripts/build_encounter.py encounters/<slug>.json` emits a page that
matches this reference.

## Fidelity

**High-fidelity.** Copy the CSS and JavaScript from the reference HTML **verbatim** —
no aesthetic reinterpretation. The Python script's job is only to:

1. Render the static document shell (head, fonts, topbar, panel layout, modal).
2. Inline the entire `<style>` block and `<script>` blocks unchanged.
3. Replace the `var ENCOUNTER = {…}` literal with the JSON contents of the spec file.
4. Patch the `<title>` and the encounter name in `<h1 id="encounter-name">` from spec data.

Everything else — interactivity, parsing, layout — lives in the inlined JS/CSS.

## The JSON spec — unchanged

The `encounters/<slug>.json` schema documented in the original slash command is unchanged.
The HTML expects this object as the `ENCOUNTER` global. See
`reference/original-slash-command.md` for the full schema, but the salient fields are:

- `name`, `slug`
- `combatants[]` — one entry per individual. Fields used: `id`, `kind` (`"npc"` | `"pc"`),
  `name`, `ac`, `hp_max`, `hp_current`, `speed`, `initiative` (NPCs only — PCs use null),
  `init_mod` (PCs), `group`, `notes`.
- `npc_blocks[]` — one per creature type. Fields used: `title`, `stats`, `defenses`,
  `sections[]` (each `{label, entries[{name, text}]}`).
- `pc_blocks[]` — one per PC. Fields used: `header`, `abilities`, `saves`, `attacks`,
  `spells`, `features`.
- `notes[]` — `{label, text}` pairs, surfaced in a topbar **Notes** modal.

## What changed visually from the previous version

If you are diffing against the previous output, here is what is new:

1. **Two-pane iPad-landscape layout.** Initiative tracker on the left (`minmax(0,1fr)`),
   sticky active-reference panel on the right (`minmax(560px, 46%)`). The old
   "Full NPC Reference / Party Reference / Encounter Details" collapsibles below the
   tracker are removed — that information lives entirely in the side panel now.
2. **Encounter notes moved to a topbar button + modal.** The `<button id="notes-btn">`
   opens `<div class="modal-shade" id="notes-modal">`. Notes only render when
   `ENCOUNTER.notes` is non-empty (the button hides itself otherwise).
3. **Initiative rows are slimmer.** Five-column grid:
   `48px [init] | minmax(220px, auto) [info] | minmax(0,1fr) [pills] | 96px [hp] | auto [controls]`.
   - Condition pills now flow in their own grid column to the right of the meta line
     (`<div class="row-pills">…</div>` as a sibling of `.info`, NOT a child) so they
     fill the previously-empty horizontal space instead of stacking below the name.
   - **Do not add `:empty { display: none }` to `.row-pills`** — hiding the cell breaks
     grid auto-placement of the trailing columns.
   - The `Cond` button no longer shows a count badge; the inline pills already convey it.
4. **Active-reference header.** Name + caption on the left, supplementary info on the
   right (senses, passive Perception, AC type, saves prof / spell DC for PCs). AC, HP,
   and Speed are intentionally NOT repeated here — those values are already on the row.
   The header is a flex container with `flex-wrap: wrap` so the supp `<dl>` drops below
   the title cleanly when there is no room beside it.
5. **Actions tab — table-style attack cards.** Each entry parsed from
   `npc_blocks[].sections[].entries[].text` runs through `parseAttackEntry()` in JS.
   If it matches the 5e "Melee/Ranged Weapon/Spell Attack: +N to hit, reach/range X,
   one target. Hit: D (XdY+Z) type. …" pattern, it renders as `<div class="attack-card">`
   with three table columns (`TO HIT` / `RANGE` / `ON HIT`) plus an extras line.
   Non-attack entries (Multiattack, area effects, traits) fall back to `<div class="action-entry">`.
6. **Actions tab badge** counts only non-trait entries (traits are surfaced on Stats).
7. **PC attacks use the same attack-card layout.** `attacks` strings in `pc_blocks[]`
   are parsed by `parsePcAttackLine()` (`"Longbow +9, 1d8+4 piercing (150/600) [Archery]"`
   → TO HIT / RANGE / DAMAGE columns + tag). Entries that don't parse as attacks
   ("EXTRA ATTACK (Ranger 5): attack twice…", "Spell save DC 13") fall through to
   `<div class="action-entry">`.
8. **Tactics tab restyled** — bold accent label header above body text in `var(--font-body)`
   at 14px / line-height 1.55, no italic plate.
9. **Senses appears once** — in the header supp panel; the `Defenses` section in the
   Stats body no longer repeats it.
10. **Tweaks panel** still provides accent / row density / base font size. State persists
    in `localStorage` under `encounter:<slug>` (HP, conditions, round, active turn,
    recharge, pinned row) and `encounter-tweaks:<slug>` (accent, density, font size).

## Reference matching

The lookup that pins a row's stat block in the active panel is unchanged: NPC combatant
name strips `\s*\[X\]$` and `\s+\d+$`; PC combatant name strips trailing `(…)`; both
match against the prefix of `npc_block.title` or `pc_block.header` split on em/en/hyphen
or open-paren. So `"Mantis Nymph 3 [B]"` → `"Mantis Nymph"` matches `"Mantis Nymph — Small Monstrosity (mantis)…"`.
This means your existing block titles do not need to change; just keep the format
documented in the original slash command.

## Files in this handoff

- `reference/encounter-worksheet.html` — the **complete** target HTML, with the
  `ENCOUNTER` object pre-seeded with the "Orchid Embrace" sample encounter.
  Copy the entire `<style>…</style>` block and both `<script>` blocks
  verbatim into the builder's output. Substitute only the `ENCOUNTER = {…}` literal,
  the `<title>`, and `<h1 id="encounter-name">` content.
- `reference/original-slash-command.md` — the existing slash command. Most of it
  (Phase 1 parsing, JSON schema, reference-matching rules) is still valid. The
  only Phase 2 step that needs revisiting is Step 3 (build the HTML) — the script's
  output format is what this redesign changes.

## Implementation notes

- The reference file is ~2,500 lines and entirely self-contained. The simplest
  builder is: read a template HTML (the reference, with the `ENCOUNTER` literal
  replaced by a sentinel like `/*__ENCOUNTER_JSON__*/`), then in Python substitute
  `json.dumps(spec, ensure_ascii=False)` into the sentinel and rewrite the title.
- Keep the SVG parchment noise overlay (inline `data:image/svg+xml` in `body::before`).
  Removing it makes the page feel flat.
- The fonts are loaded from Google Fonts (`<link rel="stylesheet">`). The slash
  command's original "no CDN, no deps, offline-first" claim is **broken** by this —
  if true offline use matters, embed the WOFF2s as base64 or self-host them.
- `localStorage` persistence keys on `ENCOUNTER.slug`. Rebuilding from a spec
  preserves a DM's in-progress combat state across rebuilds of the same encounter.

## State management

All client-side. Two `localStorage` keys per encounter:

| key                                 | shape                                                          |
|-------------------------------------|----------------------------------------------------------------|
| `encounter:<slug>`                  | `{ round, activeId, focusOverride, activeTab, actedThisRound[], rechargeSpent{}, condPanelOpen, combatants[] }` |
| `encounter-tweaks:<slug>`           | `{ accent, density, fontSize }`                                |

The reset button (top-right) clears the first key only; tweaks survive a reset.

## Design tokens (reference only — copy from the CSS verbatim, do not retype)

| token             | value      |
|-------------------|------------|
| `--night-0`       | `#100B05`  |
| `--night-1`       | `#1B1308`  |
| `--night-2`       | `#241A0E`  |
| `--ink`           | `#EBDCB5`  |
| `--accent` (ochre)| `#D69A45`  |
| `--vermilion`     | `#C44A30`  |
| `--moss`          | `#8A9A4A`  |
| `--lapis`         | `#5A7FA3`  |
| `--cochineal`     | `#B04050`  |
| `--umber`         | `#A06A3A`  |
| font-display      | `IM Fell English, EB Garamond, Georgia, serif` |
| font-label        | `IM Fell English SC, EB Garamond, Georgia, serif` |
| font-body         | `Lora, Iowan Old Style, Georgia, serif` |
| font-mono         | `JetBrains Mono, ui-monospace, "SF Mono", Menlo, monospace` |
| font-hand         | `Special Elite, "Courier Prime", "Courier New", monospace` |

(Six accent classes — `.accent-ochre`, `.accent-vermilion`, `.accent-moss`,
`.accent-lapis`, `.accent-cochineal`, `.accent-umber` — set `--accent` and
`--accent-deep` on `<html>`.)
