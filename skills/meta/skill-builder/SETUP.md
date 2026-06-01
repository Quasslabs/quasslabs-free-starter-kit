# SETUP: meta/skill-builder

**Skill:** `meta/skill-builder`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. skill-builder drafts new skill triads (SKILL.md +
FUNCTIONS.md + LESSONS.md) using in-model generation and file writes.

## Dependencies

stdlib only — no install. Optionally uses a local LLM for drafting:
- Ollama with `qwen2.5:7b` or similar for local generation ($0/call)

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/meta/skill-builder/SKILL.md
```
Provide: skill name + purpose description + bot context → outputs three files: SKILL.md + FUNCTIONS.md + LESSONS.md.

## Verify it works

1. Invoke with a skill description → three files created with correct headers.
2. Run `meta/skill-linter` on the generated SKILL.md → 0 ERRORs.
