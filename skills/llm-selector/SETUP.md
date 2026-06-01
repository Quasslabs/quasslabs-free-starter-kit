# SETUP: llm-selector

**Skill:** `llm-selector`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. llm-selector picks the right LLM for a task from
the decision table; pure in-model routing.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## How to run

```
Invoke skill: skills/llm-selector/SKILL.md
```
Provide: task description + constraints (cost/latency/local) → recommended model + rationale.

## Verify it works

Invoke with "classify intent from a fixed 20-class list" → recommends a small/fast local model.
