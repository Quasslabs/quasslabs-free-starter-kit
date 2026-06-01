# SETUP: developer/tdd

**Skill:** `developer/tdd`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. tdd is a pure guidance skill for red-green-refactor
TDD discipline; no code execution, no external deps.

## Dependencies

stdlib only — no install. The tests it guides you to write use your project's existing framework
(pytest, jest, vitest, etc.).

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/developer/tdd/SKILL.md
```
Say "TDD this feature" or "write test first" → receives structured red-green-refactor plan
with vertical-slice discipline.

## Verify it works

1. Invoke with a feature description → returns: failing test stub → implementation step → refactor step.
