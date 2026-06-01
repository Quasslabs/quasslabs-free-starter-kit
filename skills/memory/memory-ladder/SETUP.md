# SETUP: memory/memory-ladder

**Skill:** `memory/memory-ladder`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. memory-ladder is a 7-layer file-based memory backend;
it reads/writes Markdown files in the project's `_context/` and `memory/` directories.

## Dependencies

stdlib only — no install. File-based: reads/writes `.md` files only.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/memory/memory-ladder/SKILL.md
```
Can be invoked directly, or via `memory/recommender` / `memory/advisor` if you have
those skills installed. (**`memory/recommender` and `memory/advisor` are not included
in this free kit** — memory-ladder works standalone; the recommender/advisor are part of
the extended memory subsystem in the full hub.)

## Verify it works

1. Invoke with `mode: load, slug: <project>` → returns memory layers as structured JSON.
2. Confirm `_context/` directory exists in the target project after invocation.
