Implement a deliberate DM decision as a clean edit across all campaign files.

## When to Use This Command
- Removing a mechanic, lore element, or system from canon
- Retconning something established in memory files
- Adding a new rule or lore decision made outside of play
- Renaming an NPC, location, or item consistently across files
- Resolving an Open_Questions.md item with a firm decision

## Phase 1 — Find and Surface (do this first, then stop and wait)

1. Read the DM's instruction — what is being changed, added, or removed
2. Read every file in memory/ and .claude/commands/
3. Find every reference to the subject of the edit, direct or indirect
4. Present findings in this format:

---
SCRIBE REPORT

DECISION: [restate the DM's instruction in one sentence]

REFERENCES FOUND:
- memory/Homebrew_Rules.md line ~XX: [quote the relevant passage]
  Proposed action: [remove / replace with: "..."]
- memory/Open_Questions.md line ~XX: [quote]
  Proposed action: [mark resolved: "Decision: not using this system"]
- [etc.]

FILES WITH NO REFERENCES: [list clean files]

NOTES:
[anything ambiguous — e.g. "The session log mentions T+ timestamps 
in the Session 2 entry. These are historical record — recommend 
leaving them as-is rather than retroactively editing closed sessions."]

Confirm to proceed, or tell me to adjust any proposed action.
---

## Phase 2 — Commit (only after explicit confirmation)

1. Make each edit exactly as proposed and confirmed
2. For removals from Open_Questions.md, add a resolution note 
   rather than deleting the line:
   - Before: `- [ ] Date-Time System: confirm T+ format`
   - After:  `- [x] Date-Time System: removed from canon (DM decision)`
3. Report each file edited and what changed
4. Flag anything you were uncertain about with [DM CHECK]

## Key Rules
- Final session files in sessions/final/ are immutable — 
  never edit them. Note any references found there but leave them alone.
- Closed session entries in session_log.md are historical record — 
  leave them as-is, note their existence in the report
- If a reference is load-bearing (removing it would break a command's 
  logic), flag it prominently rather than silently deleting it
- When in doubt, propose a resolution note rather than a hard delete
