# SETUP: lifecycle/chat-primer

**Skill:** `lifecycle/chat-primer`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. chat-primer runs a session-start ritual: checks for
HANDOVER.md, confirms ug-ug mode, pings Ollama, and emits a SESSION READY card.

## Dependencies

stdlib only — no install. Optional: Ollama running locally for the availability check.

## Credentials / vault

None. Reads project context files (CLAUDE.md, HANDOVER.md, _context/*); writes nothing.

## How to run

```
Invoke skill: skills/lifecycle/chat-primer/SKILL.md
```
Auto-triggers at new chat start in any project that has a CLAUDE.md. Or invoke manually
with "new session" / "resume from handover".

## Verify it works

1. Invoke in a project with CLAUDE.md → emits SESSION READY card showing: ug-ug status,
   memory state, vault status, Ollama status, open items, next action.
