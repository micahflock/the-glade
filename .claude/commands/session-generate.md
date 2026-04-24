Generate a first-draft session notes document from a planning transcript.

## Core rule — no invention

This command turns a transcript into structured notes. It does not generate content.

- Flavor text, read-aloud, NPC dialogue: copy from the transcript verbatim (or as close as possible). Do not polish, expand, or rewrite.
- Skill checks, DCs, combat stats, branching outcomes, item effects: include only what the transcript specifies.
- Do not pull from campaign memory to fill gaps.
- Where a category is structurally called for but the transcript is silent, insert a marker (see below) instead of writing content.

Creative elaboration is a separate step. If the DMs want flavor text drafted, dialogue written, DCs proposed, or branches fleshed out, they will ask for it explicitly.

## Markers

Use these inline, where the missing content would have gone:

- `[MORE DETAIL: what's missing]` — a gap the DM needs to fill in before running.
- `[SLOP CHECK: what was assumed]` — a structural placeholder (e.g. a best-guess section title) that needs DM review.

## Steps

1. Read the voice transcript the user has pasted into this conversation.
2. Read `memory/campaign_state.yaml` to get the current session number (XX).
3. Extract the session's structure: the major beats, in rough chronological order as the transcript presents them.
4. For each beat, pull from the transcript only:
   - Setup / framing
   - Flavor text and read-aloud — verbatim
   - NPC dialogue and information to convey — verbatim
   - Skill checks the DM called for, with DCs if given
   - Combat encounter notes
   - Branching outcomes for player decisions
5. Where the transcript is silent on any of the above for a beat that needs it, insert a `[MORE DETAIL: ...]` marker in that slot.
6. Write the output to `sessions/sXX_draft.md`.

## Output skeleton

Use this shape. Only include subsections the transcript supports; omit others rather than inventing filler.

---

# [Session title — from transcript, or `[MORE DETAIL: session title]`]

## 1. [Beat name]

**Setup:** [from transcript, or `[MORE DETAIL: ...]`]

**Read-aloud:** [verbatim from transcript, or `[MORE DETAIL: flavor text for this moment]`]

**NPC — [name]:** [dialogue and info verbatim, or `[MORE DETAIL: ...]`]

**Skill check:** [check + DC from transcript; if DC not given, write the check and append `[MORE DETAIL: DC]`]

**Branches:** [from transcript, or `[MORE DETAIL: ...]`]

---

## 2. [Next beat]
...

---

The transcript may be rough, rambling, or incomplete — that's fine. The draft should be skeletal. A short, accurate scaffold is the goal; a polished-looking document built on invented content is the failure mode.
