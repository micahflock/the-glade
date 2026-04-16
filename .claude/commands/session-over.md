Close out a completed session and update all campaign memory.

## Inputs (all optional except session notes)
- **Session notes:** the final notes used to run the session (required — paste into chat)
- **DM notes:** taken during play (paste if available)
- **Player notes:** taken during play (paste if available)  
- **Debrief transcript:** post-session DM conversation (paste if available)

## Phase 1 — Reconcile and Surface (do this first, then stop and wait)

1. Read sessions/sXX_draft.md if it exists, where XX is the current session
2. Compare the final session notes against all other inputs
3. Identify any direct contradictions between the session notes and 
   the DM/player notes (not additions — only things that contradict)
4. Present a summary in this format:

---
RECONCILIATION REPORT — Session [X]

CONTRADICTIONS FOUND (proposed changes to session notes):
- [what the session notes say] → [what the notes/debrief say happened instead]
  Reason: [which input contradicts this]

NO CHANGES (session notes preserved):
- [list major beats confirmed or uncontradicted]

PROPOSED MEMORY UPDATES:
- NPC_Registry.yaml: [list changes — status, disposition, new NPCs]
- party/[character].yaml: [list changes per PC — inventory, quest state, levels]
- Open_Questions.md: [list resolved items, new questions raised]
- campaign_state.yaml: [current location, active threads, next session setup]

DM/PLAYER NOTES SUMMARY:
[2-3 paragraph summary of what was in the notes beyond the session beats]

Does this look right? Say "commit" to write everything, or tell me what to change.
---

## Phase 2 — Commit (only after user confirms)

1. Write the reconciled session notes to sessions/final/s0X_final.md
2. Write DM/player notes summary to sessions/notes/s0X_notes.md
3. Update memory/NPC_Registry.yaml
4. Update relevant party/*.yaml files (one per affected PC)
5. Update memory/Open_Questions.md
6. Update memory/campaign_state.yaml
7. Append a one-paragraph summary to sessions/session_log.md
8. Confirm each file written. Flag anything you were uncertain about.

## Key Rules
- Preserve session notes unless there is a direct factual contradiction
- Additions and elaborations from notes do NOT override session notes — 
  they go in the notes archive only
- When in doubt about whether something is a contradiction, flag it 
  for DM review rather than deciding unilaterally
- Mark any memory updates you're less than confident about with [DM CHECK]
