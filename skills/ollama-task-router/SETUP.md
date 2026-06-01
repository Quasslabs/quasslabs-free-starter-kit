# SETUP: ollama-task-router

**Skill:** `ollama-task-router`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. ollama-task-router annotates a plan with LOCAL vs CLOUD
routing decisions; pure in-model decision table.

## Dependencies

stdlib only — no install. Ollama must be running if you want to execute the routed local calls:
- `ollama serve` → `http://localhost:11434`

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/ollama-task-router/SKILL.md
```
Provide: task list or skill steps → each step tagged LOCAL (small model) or CLOUD (large model) + cost estimate.

## Verify it works

Invoke with a 3-step plan → each step tagged LOCAL or CLOUD with model recommendation.
