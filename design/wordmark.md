# The Glade — Wordmark Direction

A creative brief for Claude Design to generate the wordmark. Pair with `brand-brief.md` (tone) and `design-system.md` (palette/type).

---

## What it has to do

1. Sit on a stat block, an NPC card, a session recap header, and a player handout — at sizes from **24px favicon** to **300px hero** — without redrawing.
2. Read first as a *title*, second as a *creature*. The bug element is integrated, not stuck on.
3. Work in pure monochrome (a single ink on a single ground) before any color is added. If it doesn't work in chitin-on-loam, it doesn't work.

---

## The concept

**A wordmark, not a logo-mark.** "THE GLADE" set in display type, with one bug element integrated into the lettering and one structural ornament beneath. No badge, no shield, no circular emblem.

### Lettering

- **Type:** IM Fell English Regular, all caps for "GLADE", with "THE" set smaller and tucked above-left in italic small caps.
- **Spirit:** old field-guide title page — slightly inky, inconsistent stroke, like the press was tired.
- **Treatment:** no extra effects. No outer glow, no gradient. The character of IM Fell English carries it.

### The bug element

One bug, integrated into a letter. **Two viable directions** — pick one for primary, keep the other as a secondary mark:

**Primary — the G fiddlehead-stag-beetle.**
The terminal of the **G** curls inward into a stag beetle's mandibles. Looked at quickly, it reads as decorative serif flourish; on a closer look, the curl resolves into a beetle's head with two opposing mandibles. The body of the beetle is implied, not drawn — the letterform *is* the body.

**Secondary — the moth above the E.**
A small, symmetric moth perched on the crossbar of the final **E**, wings folded, antennae feathered. Used for square / icon-only contexts (favicon, social avatar) where the full wordmark won't fit.

### The structural ornament

A single horizontal **spider-silk thread** beneath the wordmark, with one **dewdrop** centered and a tiny **knot** at the right end. The thread is `--accent` (usually `amber`) at 60% opacity. It anchors the wordmark to the page without enclosing it.

### Optional tagline lockup

When room allows, beneath the silk thread, set a tagline in EB Garamond italic small caps, tracked +0.12em:

> *a forest at insect scale*

Two-line lockup, centered. Tagline is omitted at sizes below ~120px width.

---

## Color treatment

| Context                          | Wordmark color        | Ground            | Silk thread accent |
|----------------------------------|-----------------------|-------------------|--------------------|
| Default (dark)                   | `chitin` `#E8DFCB`    | `loam` `#0F1410`  | `amber` `#C77B2E` 60% |
| Light / handout                  | `loam-ink` `#1A1F18`  | `bone` `#F5EFE0`  | `amber` `#C77B2E` 60% |
| Single-color print (engraved)    | 100% K                | none              | 100% K, hairline    |
| Inverted / hero                  | `amber` `#C77B2E`     | `loam` `#0F1410`  | `chitin` 30%        |

**Never:** rainbow, multi-accent, embossed, or set on a busy texture without a ground panel.

---

## Sizes & responsive behavior

- **24px favicon:** moth-on-E secondary mark only, monochrome.
- **48–96px:** wordmark only — drop the silk thread and the tagline.
- **120–240px:** wordmark + silk thread, no tagline.
- **240px and up:** full lockup — wordmark + silk thread + tagline.

---

## Things to try and things to avoid

**Try:**
- A single dewdrop on the silk catching a tiny highlight — the only "shiny" element in the entire identity.
- Letting the **G**'s mandible curl be slightly asymmetric, the way an actual stag beetle's mandibles are.
- Setting "THE" small enough that it reads as a lichen growth tucked into the **G**'s upper-left, not as equal-weight type.

**Avoid:**
- Drawing a full beetle floating next to the word — the beetle has to *be* the letter.
- Drop shadows, outer glows, or any "metal" texture on the type.
- A circular badge enclosing the wordmark. The Glade has no horizon and no edges; the wordmark shouldn't either.
- Cute / cartoon bug eyes on the beetle. No eyes at all is better than wrong eyes.
- Using two accent colors in the wordmark. One ground, one ink, one accent at low opacity.

---

## How to brief Claude Design

A working prompt for the wordmark generation step:

> Generate a wordmark for a tabletop campaign called **The Glade** — a dark fantasy world at insect scale, sitting between Miyazaki whimsy and Del Toro horror.
>
> Set "THE GLADE" in IM Fell English, all caps, with "THE" small and italic tucked above-left of "GLADE". The terminal of the **G** curls inward into a stag beetle's mandibles — the curl reads as both serif flourish and beetle head. Beneath the wordmark, a thin horizontal spider-silk thread in warm amber (#C77B2E, 60% opacity), with a single dewdrop centered and a small knot at the right end.
>
> Default treatment: warm bone-white (#E8DFCB) on near-black moss (#0F1410). No gradients, no drop shadows, no outer glow. Inky, slightly imperfect line — like an old field-guide title page that has been read often.
>
> Provide three responsive sizes: hero (full wordmark + silk + tagline "a forest at insect scale" in EB Garamond italic small caps), standard (wordmark + silk only), and icon (the moth-on-the-final-E secondary mark, monochrome, square).
