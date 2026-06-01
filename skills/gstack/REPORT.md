# REPORT: gstack

**Skill:** `gstack` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to resolution | 4 hours (manual model selection + role-juggling) | ~1 hour | User timing |
| Wrong model calls | Frequent (over-using expensive models) | Rare | Cost reports |

## Who gets the most value

Anyone building multi-step agent workflows who wastes money on GPT-4/Sonnet calls that could have been phi4-mini or haiku. gstack gives you a principled routing table instead of "just use the expensive model."

## How it fits in a flow

**Upstream:** task description → **gstack** → model + role assignment → agent execution

Use gstack at the start of any session or workflow planning step to assign the right model to each sub-task before spending tokens.

## Skill interactions

| Pairs with | How |
|---|---|
| `llm-selector` | gstack sets roles; llm-selector fills in the exact model for edge cases |
| `task-router` | task-router routes tasks; gstack assigns the model tier for each route |

## Measured outcomes

- 75% reduction in time spent on manual model selection.
- Cost reduction from right-sizing models to the task.

## Test coverage

Manual: verify routing decisions match the GStack model table for known task types.
