# SKILL: task-router

**Bot:** any · pre-flight evaluator
**Role:** Step-0 pre-flight that classifies a task, surfaces red gates (immediate human blockers) and yellow notes (assumptions to confirm later), and emits an estimated-cost routing card. Prevents mid-task stalls from missing credentials or unclear requirements.
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
- Before starting any multi-step task or skill sequence
- User says "route this task", "what do I need to unblock this?"
- Slash trigger: `/task-router`

## Gate rules

### RED — full blocker

- External account not created (Stripe, Twilio, etc.)
- API key / secret missing
- Irreversible action pending (prod deploy, force-push)
- Access credential unavailable

### YELLOW — partial blocker

- Config value can be mocked
- Requirement ambiguous (can proceed with stated assumption)
- Later-stage human checkpoint

## Steps

1. `evaluate(task)` runs heuristic rules over the task string.
2. Returns red_gates + yellow_notes + estimated_cost + recommended_skill.
3. Caller emits the routing card before any other skill executes.

## Input

| Field | Type | Required |
|---|---|---|
| `task` | string | yes |

## Output

```json
{
  "red_gates": [],
  "yellow_notes": [],
  "estimated_cost": 0.0,
  "recommended_skill": null
}
```

## Handoffs

- `ollama-task-router` — local-vs-cloud per-step routing
- `llm-selector` — pick the cloud model for cloud-routed steps
- `memory-ladder` — persist routing card across sessions

## Permissions

None (pure-Python heuristic).

## Lambda candidates

`evaluate()` — stateless, deterministic.

## Value

Catches missing credentials + irreversible actions BEFORE the agent burns tokens. Tests cover red-gate detection (API key keywords) + yellow-note flagging (TODO / ambiguous).
