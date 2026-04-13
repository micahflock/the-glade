Audit the campaign project for structural issues and optimization 
opportunities. Read-only — produce a report only, write nothing.

## What to Read
Read every file in: .claude/commands/, memory/, sessions/final/,
and CLAUDE.md. Also read memory/campaign_state.yaml for the current session number.

## Hard Checks (report all findings, even if none)

**Broken references:**
- For each command file, identify any memory/ files it references 
  that don't exist on disk
- For each command file, identify any other commands it references 
  that don't exist
- Check CLAUDE.md for references to files that don't exist
- Check memory/campaign_state.yaml for expected fields missing 
  (current_session, active_location, etc.)

**Session continuity:**
- Confirm sessions/final/ contains a final file for every session 
  number below current_session in memory/campaign_state.yaml
- Flag any gaps

**Orphaned files:**
- List any files in memory/ that are not referenced by CLAUDE.md 
  or any command

## Soft Checks (flag only if genuinely worth surfacing)

**Memory file health:**
- Flag any memory file over ~300 lines as a candidate for splitting
- Flag any field in memory/campaign_state.yaml unchanged across the last 
  3 final session notes

**Command overlap:**
- Flag any two commands that appear to have significantly overlapping 
  responsibilities

**Open questions:**
- Scan Open_Questions.md and cross-reference sessions/final/ —
  flag any items that appear to have been resolved in play but 
  not marked resolved

## Output Format

---
JANITOR REPORT

HARD ISSUES: [X found]
[list each with: file → issue → suggested fix]

SOFT SUGGESTIONS: [X found]  
[list each with: file → observation → why it might matter]

NOTHING TO REPORT:
[list check categories that came back clean]
---

Do not fix anything. Wait for instruction.
