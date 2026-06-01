# SETUP: developer/zoom-out

**Skill:** `developer/zoom-out`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. zoom-out is a one-prompt escape hatch when stuck
inside a single file; produces a module-map summary via in-model analysis.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/developer/zoom-out/SKILL.md
```
Say "zoom out" or "stuck in this file" → receives a module-map summary using strict domain
vocabulary (Module / Interface / Depth / Seam / Adapter).

Note: `disable-model-invocation: true` — human-trigger only, not auto-chained.

## Verify it works

1. Invoke with a codebase description → returns module-map with component relationships.
