# SETUP: task-router

**Skill:** `task-router`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. task-router is a pure LLM routing skill; it classifies
tasks and assigns models from a decision table with no external deps.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/task-router/SKILL.md
```
Run as Step 0 before any skill execution to get a routing card: model assignments + red/yellow gates.

## Verify it works

Invoke with a task description → receives routing card (model per sub-task + gate classification).
