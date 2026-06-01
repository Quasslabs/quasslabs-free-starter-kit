# SETUP: developer/improve-codebase-architecture

**Skill:** `developer/improve-codebase-architecture`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. improve-codebase-architecture surfaces architectural
friction via a strict glossary (Module/Interface/Depth/Seam/Adapter) and a deletion-test
heuristic; pure in-model analysis.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/developer/improve-codebase-architecture/SKILL.md
```
Say "can we simplify this?" or "refactor this" → receives architectural friction report with
specific deepening opportunities.

## Verify it works

1. Invoke with a codebase description → returns friction points categorized by Module/Seam/Depth.
