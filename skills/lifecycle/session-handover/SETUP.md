# SETUP: lifecycle/session-handover

**Skill:** `lifecycle/session-handover`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. session-handover writes `HANDOVER.md` + a chat paste
block; uses only file writes and in-model summarization.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/lifecycle/session-handover/SKILL.md
```
Invoke at ~50% context usage or before session end. Outputs `HANDOVER.md` in the project root.

## Verify it works

1. Invoke in a project directory → HANDOVER.md created/updated.
2. File contains: completed[], open_items[], decisions[], files_modified[], next_action.
