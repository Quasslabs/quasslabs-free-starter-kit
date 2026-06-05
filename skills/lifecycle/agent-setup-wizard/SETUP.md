# SETUP: lifecycle/agent-setup-wizard

**Skill:** `lifecycle/agent-setup-wizard`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. agent-setup-wizard generates `CLAUDE.md`, `AGENTS.md`,
and `.cursorrules` for new projects; file-writes only, no external deps.

## Dependencies

stdlib only — no install.

## Credentials / vault

None. Reads `skills/CORE-SKILL-KIT.json` for the 24 foundational skills list.

## How to run

```
Invoke skill: skills/lifecycle/agent-setup-wizard/SKILL.md
```
Run at new project start. Generates: CLAUDE.md (≤200 lines) + AGENTS.md + .cursorrules
+ _context/ files. Pre-selects 24 core skills.

## Verify it works

1. Invoke in a new empty directory → CLAUDE.md created with skills list.
2. AGENTS.md exists with memory + ug-ug configuration.
