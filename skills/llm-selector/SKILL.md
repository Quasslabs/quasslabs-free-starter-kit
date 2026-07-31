# SKILL: llm-selector

**Bot:** any · model picker
**Role:** Pick the optimal model for a task type, return a fallback chain, and report estimated cost per 1k tokens. Pure lookup table — no LLM call.
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
- "Which model should I use for X?"
- Cost-tuning a skill before deploy
- Slash trigger: `/llm-selector`

## Task-type catalog

| Task type | Primary | Fallback chain | $/1k (primary) |
|---|---|---|---|
| `classify` | phi4-mini | qwen2.5:7b, claude-haiku | 0.0 |
| `extract` | phi4-mini | qwen2.5:7b, claude-haiku | 0.0 |
| `code` | qwen2.5-coder:7b | claude-sonnet | 0.0 |
| `reason` | qwen2.5:7b | claude-sonnet, claude-opus | 0.0 |
| `draft` | claude-sonnet | claude-haiku | 0.003 |
| `judge` | claude-opus | claude-sonnet | 0.015 |

(Costs are local=0 for Ollama models; cloud rates approximate input+output blend.)

## Steps

1. `select(task_type, budget=0.0)` looks up the catalog.
2. Returns primary + fallback list + estimated cost.
3. If `budget > 0` and primary cost exceeds it, fall back to next tier.

## Input

| Field | Type | Required |
|---|---|---|
| `task_type` | string | yes |
| `budget` | float | no (default 0.0 = no constraint) |

## Output

```json
{
  "primary": "model_id",
  "fallback": ["..."],
  "estimated_cost_per_1k": 0.0
}
```

## Handoffs

- `ollama-task-router` — local-vs-cloud upstream decision
- `task-router` — pre-flight orchestrator

## Permissions

None.

## Lambda candidates

`select()` — stateless catalog lookup.

## Value

Never default to Opus when Haiku works. The catalog encodes the right tier per task type; tests cover classify (local), code (local), draft (cloud), and budget-constrained downgrade.
