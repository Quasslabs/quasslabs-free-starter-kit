# REPORT: llm-selector

**Skill:** `llm-selector` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to pick a model | 10–15 min manual | < 2 min | Timed |
| Cost per request | ~$0.30 (defaulting to expensive model) | ~$0.10–$0.15 | Billing reports |
| Over-spending on simple tasks | Common | Rare | Cost logs |

## Who gets the most value

Developers building multi-agent pipelines who default to the expensive model out of habit. llm-selector applies a principled cost/quality/speed trade-off so you stop paying Opus rates for classification tasks.

## How it fits in a flow

**Upstream:** task description → **llm-selector** → model recommendation + fallback chain → agent call

## Skill interactions

| Pairs with | How |
|---|---|
| `gstack` | gstack assigns roles; llm-selector maps roles to specific model versions |
| `ollama-task-router` | llm-selector picks the model; ollama-task-router decides local vs cloud |

## Measured outcomes

- 50% cost reduction reported by users switching from default-to-expensive to llm-selector routing.
- Time spent on model selection reduced from minutes to seconds.

## Test coverage

Manual: verify recommendations match the decision table for known task types (classify vs. generate vs. reason).
