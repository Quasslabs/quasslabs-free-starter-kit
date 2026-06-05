# SETUP: meta/skill-builder

**Skill:** `meta/skill-builder`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. skill-builder drafts new skill triads (SKILL.md +
FUNCTIONS.md + LESSONS.md) using in-model generation and file writes.

## Dependencies

stdlib only — no install.

## Credentials / vault

None. Optionally uses Ollama for local drafting:
- `qwen2.5:7b` — adequate for skill drafts (installed)
- `qwen2.5-coder:7b` — for code-heavy FUNCTIONS.md (installed)

## How to run

```
Invoke skill: skills/meta/skill-builder/SKILL.md
```
Provide: skill name + purpose description + bot context. Outputs the triad files.

## Verify it works

1. Invoke with a skill description → three files created: SKILL.md + FUNCTIONS.md + LESSONS.md.
2. Run `skill-linter` on the generated SKILL.md → 0 ERRORs.
