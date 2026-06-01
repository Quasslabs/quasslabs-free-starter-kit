# SETUP: humanizer

**Skill:** `humanizer`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. humanizer detects 29 AI-writing patterns and rewrites
to voice-matched human prose; pure in-model text transformation.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/humanizer/SKILL.md
```
Pass any AI-generated text → receives rewritten version with AI-tells removed, matched to
the target voice. Use as the mandatory final pass before any client-facing output.

Note: ug-ug mode: **none** — this skill produces prose and compressing it defeats the purpose.

## Verify it works

1. Pass a paragraph with obvious AI patterns (em-dash overuse, "it's worth noting", etc.).
2. Receive rewritten text that reads as natural human prose.
