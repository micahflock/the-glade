# /update-character

# Update an existing character YAML with new information.

# Handles two distinct scenarios: photo-based updates (level ups, sheet rewrites)

# and text-based targeted updates (mid-session tracking, inventory changes, etc.)

## Inputs

Paste into chat alongside this command:

- Character name or callsign (always required)
- Either: new photo(s) of the updated sheet (for level ups / sheet rewrites)
- Or: plain text describing the change (for targeted updates)
- Both may be provided together

## Determine Update Mode

**Photo provided → Sheet Diff Mode**
**Text only → Targeted Update Mode**

-----

## Sheet Diff Mode (photo provided)

Use this when the player has updated their physical sheet — typically after a level up.

### Phase 1 — Diff and Flag (stop after this and wait for confirmation)

1. Read the existing party/[name_slug].yaml
1. Read all provided photos carefully
1. Identify every field that has changed, been added, or been removed
1. Produce this report:

-----

SHEET DIFF REPORT — [Character Name]

CHANGED FIELDS:

- [field]([value]): [old value] → [new value]

NEW FIELDS (present on updated sheet, absent before):

- 

REMOVED FIELDS (present before, absent on updated sheet):

- [field]([value]): [previous value] — confirm intentional?

FLAGGED:

- [field]([value]): [reason — illegible / arithmetic inconsistency / unexpected change]
  Options: [interpretations if applicable]

## UNCHANGED: [count] fields confirmed unchanged — not listed for brevity

Stop. Wait for DM to confirm before writing anything.

### Phase 2 — Write (only after confirmation)

Apply confirmed changes to party/[name_slug].yaml.

- Preserve all existing notes and flags unless explicitly superseded
- Add a comment on any corrected arithmetic: # Sheet showed X — corrected
- Update the file header comment with today's date and reason
  e.g. # Updated: Level 3 → 4 import
- Report each field changed

-----

## Targeted Update Mode (text description only)

Use this for specific known changes: HP damage, spell slot expenditure,
inventory additions or removals, condition tracking, or any other
mid-campaign update that doesn't require reading a new sheet.

### Phase 1 — Confirm Scope (stop after this and wait for confirmation)

1. Read the existing party/[name_slug].yaml
1. Interpret the requested change
1. Produce this report:

-----

TARGETED UPDATE — [Character Name]

PROPOSED CHANGES:

- [field]([value]): [old value] → [new value]
  Reason: [restate the instruction that drove this change]

QUESTIONS (if the instruction is ambiguous):

- [question]

NO CHANGES TO:

- [any fields the instruction might have implied but shouldn't change]

-----

Stop. Confirm before writing.

### Phase 2 — Write (only after confirmation)

Apply confirmed changes only. Do not touch any field not listed in the
confirmed proposal.

-----

## Key Rules

- Never update sessions/final/ files — character sheets only
- hp_current floor is 0 — never write a negative value
- spell_slots current floor is 0 per slot level
- If a level-up photo is missing a field that existed before
  (e.g. a spell the player forgot to copy over), flag it —
  do not silently drop it from the file
- Preserve all [UNCLEAR] and [DM CHECK] flags unless the update
  explicitly resolves them — note the resolution in a comment
- After any write, append a one-line entry to the file header:
  
  # [date] — [brief description of what changed]
