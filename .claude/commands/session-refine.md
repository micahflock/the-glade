Refine an existing session draft based on a new planning transcript.

## Core rule — no invention

Same rule as /session-generate: copy from the transcript verbatim, flag gaps with markers, do not elaborate. Creative content happens only on explicit ask.

Be surgical. Preserve everything the transcript doesn't touch. This is an edit, not a rewrite.

- Flavor text, read-aloud, NPC dialogue: copy from the transcript verbatim (or as close as possible). Do not polish, expand, or rewrite.
- Skill checks, DCs, combat stats, branching outcomes, item effects: add or change only what the transcript specifies.
- Do not pull from campaign memory to fill gaps.

## Markers

- `[MORE DETAIL: what's missing]` — a gap the DM needs to fill in before running.
- `[SLOP CHECK: what was assumed]` — a structural placeholder that needs DM review.
- `[OPEN: description]` — a decision discussed in the transcript but not concluded.

## Steps

1. Read the existing session draft the user has pasted into this conversation.
2. Read the new voice transcript the user has pasted into this conversation.
3. Read `memory/campaign_state.yaml` to confirm the current session number (XX).
4. Update the draft to reflect the transcript:
   - Apply changed decisions, added beats, removed beats, updated dialogue.
   - Copy new flavor text, read-aloud, and dialogue verbatim from the transcript.
   - Add skill checks, DCs, or branches only if the transcript specifies them; otherwise leave existing slots alone or mark with `[MORE DETAIL: ...]`.
   - Clear an existing `[MORE DETAIL]` or `[OPEN]` marker only if the transcript resolves it.
   - Add `[OPEN: ...]` for decisions the transcript raises but doesn't conclude.
5. Leave everything the transcript doesn't touch exactly as it was.
6. Write the updated draft to `sessions/sXX_draft.md`, overwriting the previous version.
7. Tell the user the file is ready and print the full updated markdown in chat for easy copy.

The output should follow the same structure as the existing draft. A short, accurate edit is the goal; silently rewriting untouched sections is the failure mode.
