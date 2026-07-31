# SKILL: skill-linter

**Bot:** any · meta
**Role:** Slim SKILL.md validator. Checks required header fields and required body sections; returns a list of issues. Slim wrapper — the full hub linter is a separate tool.
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
- User says "lint this skill", "validate SKILL.md"
- Slash trigger: `/skill-linter`
- Before promoting a skill from wip to ready

## Steps

1. Read the target SKILL.md.
2. Check required header fields: Bot, Role, Ug-ug mode, Model, Status, Parallelizable.
3. Check required body sections: `## When to invoke`, `## Handoffs`.
4. Return list of issues; exit 0 if clean, 1 otherwise.

## Input

- `path` — path to a SKILL.md file

## Output

- list of issue strings (empty = pass)

## Handoffs

- `skill-builder` — when issues indicate missing scaffolding; re-draft the skill

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<target>/SKILL.md` | Read the file under lint |

## Lambda candidates

`lint(path)` — pure file read + regex check; trivial Lambda candidate.

## Notes

This is the SLIM wrapper shipped with the kit. The full hub linter (with strict-commercial mode, evals gate, vendor-leak scan, etc.) is a separate internal tool.
