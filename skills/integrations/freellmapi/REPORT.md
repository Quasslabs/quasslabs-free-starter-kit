# REPORT: integrations/freellmapi

**Skill:** `integrations/freellmapi` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Cost for non-sensitive LLM calls | Paid cloud ($0.01–$0.10/call) | $0 (free-tier providers) | Cost comparison |
| Providers available via one endpoint | 1 | ~14 (with failover) | Provider count |
| Setup time for multi-provider access | Hours (per-provider API keys) | ~15 min (one proxy) | Timed |

## Who gets the most value

Developers doing research, classification, or generation tasks that don't involve sensitive data and don't need guaranteed SLAs. freellmapi gets you Gemini / Groq / Cerebras quality for $0 on eligible tasks.

## How it fits in a flow

**In the routing chain:** local Ollama → **freellmapi (free-cloud)** → paid cloud (Claude/GPT)

Use for non-sensitive tasks where local models are underpowered and you don't want to burn paid API credits.

**HARD RULE:** Never send PII, credentials, client data, or anything sensitive through freellmapi or any free-tier provider. These providers may train on inputs.

## Skill interactions

| Pairs with | How |
|---|---|
| `ollama-task-router` | router decides local vs cloud; freellmapi is the free-cloud rung |
| `llm-selector` | selector picks the provider tier; freellmapi is the $0 option |

## Measured outcomes

- $0 cost on eligible non-sensitive tasks vs. paid cloud.
- 14 providers with automatic failover means high availability.

## Test coverage

1. `curl http://localhost:3001/v1/models` → returns model list (proxy running).
2. POST a non-sensitive completion → response returned within 10s.
