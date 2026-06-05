# SETUP: memory/memory-ladder

**Skill:** `memory/memory-ladder`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. memory-ladder is a 7-layer file-based memory backend;
it reads/writes Markdown files in the project's `_context/` + `memory/` directories.

## Dependencies

stdlib only — no install. File-based: reads/writes `.md` files only.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/memory/memory-ladder/SKILL.md
```
Typically invoked by `memory/recommender` or `memory/advisor` after they select
memory-ladder as the backend for a project.

## Verify it works

1. Invoke with `mode: load, slug: <project>` → returns memory layers as structured JSON.
2. Confirm `_context/` directory exists in the target project.
