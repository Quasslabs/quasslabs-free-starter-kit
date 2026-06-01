# SETUP: lifecycle/agent-setup-wizard

**Skill:** `lifecycle/agent-setup-wizard`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. agent-setup-wizard generates `CLAUDE.md`, `AGENTS.md`,
and `.cursorrules` for new projects; file-writes only, no external deps.

## Dependencies

stdlib only — no install.

## How to run

```
Invoke skill: skills/lifecycle/agent-setup-wizard/SKILL.md
```
Run at new project start. Outputs: CLAUDE.md (≤200 lines) + AGENTS.md + .cursorrules + _context/ files.

## Verify it works

1. Invoke in a new empty directory → CLAUDE.md created with skills list and project context.
2. AGENTS.md exists with memory + output-mode configuration.
