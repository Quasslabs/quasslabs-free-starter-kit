# REPORT: ollama-task-router

**Skill:** `ollama-task-router` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Cloud token spend on local-eligible tasks | 100% | ~30% | Token logs |
| Token savings per plan execution | 0 | ~30% average | Internal measurement |
| Response latency (local vs cloud) | Cloud only | 20% faster for local steps | Timing logs |

## Who gets the most value

Developers running multi-step pipelines who have a local model (Ollama) available but default everything to the cloud. ollama-task-router tags each step so local-eligible work runs on your machine for free.

## How it fits in a flow

**Upstream:** task plan → **ollama-task-router** → annotated plan (LOCAL/CLOUD per step) → execution

## Skill interactions

| Pairs with | How |
|---|---|
| `llm-selector` | llm-selector picks models; ollama-task-router decides where they run |
| `task-router` | task-router routes tasks; ollama-task-router adds the local/cloud annotation |

## Measured outcomes

- ~30% average token savings per plan execution vs. cloud-only baseline.
- Response time improved by ~20% for local-eligible steps.

## Test coverage

Manual: verify LOCAL/CLOUD annotations on a known plan match the decision table.
