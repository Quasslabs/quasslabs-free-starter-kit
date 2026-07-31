# SKILL: skill-builder

**Bot:** any · meta
**Role:** Draft a new skill from a one-line intent. Checks prior art, emits a SKILL.md header stub + folder layout suggestion.
**Ug-ug mode:** lite
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** yes
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- User says "build a skill", "draft a skill", "scaffold a skill"
- Slash trigger: `/skill-builder`

## Steps

1. Read the intent (name + one-line role).
2. Suggest a slug (kebab-case) and a role label.
3. Emit a SKILL.md header stub conforming to schema v2.1.
4. Emit a folder layout (SKILL.md, FUNCTIONS.md, LESSONS.md, INSTALL.md, SETUP.md, REPORT.md, manifest.json, commands, src, tests).
5. Hand off to `skill-linter` once filled in.

## Input

- `name` — proposed skill slug
- `role` — one-line description

## Output

- `header` — dict matching SKILL.md schema v2.1
- `layout` — list of files to create

## Handoffs

- `skill-linter` — validate the drafted SKILL.md once header + sections are filled in

## Permissions

None.

## Lambda candidates

None — drafting helper only.
