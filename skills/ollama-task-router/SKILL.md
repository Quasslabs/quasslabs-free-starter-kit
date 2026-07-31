# SKILL: ollama-task-router

**Bot:** any · local/cloud routing
**Role:** Classify a task as best-run on a local Ollama model or a paid cloud API. Returns target + model + reason. Uses `_lib_llm.call_llm_json` for the classification call.
**Ug-ug mode:** lite
**Model:** phi4-mini
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
- Annotating plan steps with local-vs-cloud
- "Which steps can run locally?"
- Slash trigger: `/ollama-task-router`

## Routing rules (default catalog)

| Task type | Target | Model |
|---|---|---|
| Classify / extract / route | local | phi4-mini |
| Code gen / refactor | local | qwen2.5-coder:7b |
| Multi-step reasoning | local | qwen2.5:7b |
| Long-form narrative draft | cloud | claude-sonnet |
| High-stakes judgment | cloud | claude-opus |

## Steps

1. `route(task)` builds a structured prompt asking phi4-mini to pick target + model + reason.
2. `_lib_llm.call_llm_json` returns parsed JSON.
3. Caller maps to its own dispatch layer.

## Input

| Field | Type | Required |
|---|---|---|
| `task` | string | yes |

## Output

```json
{ "target": "local|cloud", "model": "phi4-mini", "reason": "..." }
```

## Handoffs

- `task-router` — orchestrates the full pre-flight
- `llm-selector` — picks the exact cloud model when target=cloud

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `http://localhost:11434/api/generate` | Local Ollama |

## Lambda candidates

`route()` — stateless once the Ollama endpoint is reachable.

## Value

Routing locally-runnable tasks to a local model removes their per-call cloud cost (down to local power-only). Tests verify the function returns the locked schema and handles monkeypatched LLM responses.
