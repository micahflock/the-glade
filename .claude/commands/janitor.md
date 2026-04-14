Audit the campaign project using parallel background agents.
Read-only — produce a report only, write nothing.

## Step 1 — Launch Agents in Parallel

Use the Agent tool to launch all four agents below in a single message
(set run_in_background: true for each). Do not proceed until all four
have returned.

---

**Agent 1 — Commands Audit**
Read every file in .claude/commands/ and CLAUDE.md.
Report back:
- Any memory/ file referenced that does not exist on disk
- Any command referenced by another command that does not exist
- Any command in .claude/commands/ not mentioned in CLAUDE.md
- Any two commands with significantly overlapping responsibilities
Label your response: COMMANDS AUDIT

---

**Agent 2 — Memory File Health**
Read every file in memory/.
Report back:
- Any file over ~300 lines (candidate for splitting)
- Any memory file not referenced by CLAUDE.md or any command file
- Any expected field missing from campaign_state.yaml
  (required: current_session, active_draft, active_location,
  party block, active_threads, memory_files)
- Any field in campaign_state.yaml that looks stale or placeholder
Label your response: MEMORY AUDIT

---

**Agent 3 — Session Continuity**
Read memory/campaign_state.yaml and every file in sessions/final/.
Report back:
- The current session number from campaign_state.yaml
- Whether sessions/final/ contains a final file for every session
  number below the current session (flag any gaps)
- Any final session file that references an NPC or location name
  not present in memory/NPC_Registry.yaml or memory/World_Codex.md
  (cross-reference those files too)
Label your response: SESSION CONTINUITY AUDIT

---

**Agent 4 — Open Questions Staleness**
Read memory/Open_Questions.md and every file in sessions/final/.
Report back:
- Any item in Open_Questions.md that appears to have been resolved
  in a final session file but is not marked resolved
- Any item marked resolved that has no corresponding session evidence
- Any category in Open_Questions.md with no items (structural bloat)
Label your response: OPEN QUESTIONS AUDIT

---

## Step 2 — Synthesize and Report

Once all four agents have returned, compile their findings into this format:

---
JANITOR REPORT

HARD ISSUES: [X found]
[broken references, missing sessions, missing required fields]
→ file: issue — suggested fix

SOFT SUGGESTIONS: [X found]
[stale fields, file size, command overlap, unresolved questions]
→ file: observation — why it might matter

CLEAN CHECKS:
[list any audit categories that returned nothing to flag]
---

Do not fix anything. Wait for instruction.
