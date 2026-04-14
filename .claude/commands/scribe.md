Implement a deliberate DM decision as a clean edit across all campaign files.

## When to Use This Command
- Removing a mechanic, lore element, or system from canon
- Retconning something established in memory files
- Adding a new rule or lore decision made outside of play
- Renaming an NPC, location, or item consistently across files
- Resolving an Open_Questions.md item with a firm decision

## Phase 1 — Find and Surface (launch agents, then stop and wait)

Read the DM's instruction, then launch all three agents below in a single
message (run_in_background: true for each). Do not proceed until all
three have returned.

---

**Agent 1 — Memory Targets**
The DM's instruction is: [restate the instruction here]
Read these files: memory/NPC_Registry.yaml, memory/Party_Sheet.yaml,
memory/campaign_state.yaml, memory/Homebrew_Rules.md, memory/World_Codex.md.
Find every reference to the subject — direct or indirect (alternate names,
pronouns referring back, mechanical systems derived from it, etc.).
For each reference found, quote the relevant passage and line number.
For each file with no references, say so explicitly.
Label your response: MEMORY TARGETS

---

**Agent 2 — Open Questions**
The DM's instruction is: [restate the instruction here]
Read memory/Open_Questions.md.
Find every item related to the subject — including items that would be
resolved, contradicted, or affected by this decision.
Quote each item and its line number.
Suggest for each: mark resolved, update wording, or leave as-is.
Label your response: OPEN QUESTIONS

---

**Agent 3 — Session History and Commands (read-only)**
The DM's instruction is: [restate the instruction here]
Read every file in sessions/final/, sessions/session_log.md,
and .claude/commands/.
Find every reference to the subject.
For session files and session_log.md: note references only —
  these files are immutable and must not be edited.
For command files: flag any reference that is load-bearing
  (removing or changing it would break the command's logic).
Label your response: SESSION HISTORY AND COMMANDS

---

Once all three agents return, compile their findings into this format:

---
SCRIBE REPORT

DECISION: [restate the DM's instruction in one sentence]

PROPOSED EDITS (writable files):
- memory/Homebrew_Rules.md line ~XX: [quote]
  Action: [remove / replace with: "..."]
- memory/Open_Questions.md line ~XX: [quote]
  Action: [mark resolved: "Decision: ..."]
- [etc.]

NOTED REFERENCES (immutable — no edits):
- sessions/final/s01_final.md line ~XX: [quote]
  Note: historical record, leaving as-is

LOAD-BEARING FLAGS:
- [any command file references that would break if changed]

FILES WITH NO REFERENCES: [list]

NOTES:
[anything ambiguous — conflicting references, uncertain scope, etc.]

Confirm to proceed, or tell me to adjust any proposed action.
---

## Phase 2 — Commit (only after explicit confirmation)

Make each edit exactly as proposed and confirmed. Write directly —
do not delegate edits to agents.

1. Make each edit to writable files
2. For Open_Questions.md resolutions, add a resolution note rather
   than deleting the line:
   - Before: `- [ ] Some question`
   - After:  `- [x] Some question — [Decision: ...]`
3. Report each file edited and what changed
4. Flag anything uncertain with [DM CHECK]

## Key Rules
- Final session files and session_log.md are immutable — note them, never edit them
- If a reference is load-bearing in a command file, flag it prominently
- When in doubt, propose a resolution note rather than a hard delete
