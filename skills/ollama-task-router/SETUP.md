# SETUP: ollama-task-router

**Skill:** `ollama-task-router`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. ollama-task-router annotates a plan with LOCAL vs CLOUD
routing decisions; pure in-model decision table.

## Dependencies

stdlib only — no install. Ollama must be running if you want to verify the routed local calls:
- `ollama serve` (or Ollama Desktop) → `http://localhost:11434`

## Credentials / vault
None.

## How to run
```
Invoke skill: skills/ollama-task-router/SKILL.md
```
Provide: task list or skill step list → receives annotated version with LOCAL/CLOUD tags + cost estimate.

## Verify it works
1. Invoke with a 3-step plan → each step tagged LOCAL (phi4-mini/qwen2.5-coder:7b) or CLOUD (sonnet/haiku).
