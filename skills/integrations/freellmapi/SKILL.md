# SKILL: freellmapi

**Bot:** any
**Role:** Self-hosted OpenAI-compatible proxy aggregating ~14 free-tier LLM providers (Gemini, Groq, Cerebras, Mistral, GitHub Models, OpenRouter, …) with automatic failover. The free-cloud rung in the LLM fallback chain — sits between your local Ollama and paid cloud APIs.
**Ug-ug mode:** full
**Model:** haiku — routing decisions are deterministic
**Tool compatibility:** Claude Code · Cursor
**Status:** beta
**Parallelizable:** yes — per-call stateless

## Fallback chain position

```
local Ollama → free-cloud (this) → paid cloud (Anthropic/OpenAI)
```

Use freellmapi for: model benchmarking, throwaway prompts, comparing providers at $0.

## HARD RULE — non-sensitive content only

Free providers may train on inputs. Never send credentials, PII, client data, or billing information through this tier.

## When to invoke

- "Try this prompt against Gemini and Groq without spending money"
- "Run a quick benchmark across free providers"
- "I want a free cloud fallback when Ollama is down"

## Setup

1. Clone [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) to a local folder
2. Copy `.env.example` → `.env`, set `ENCRYPTION_KEY` + `DASHBOARD_ORIGINS`
3. `npm install && npm start` — runs on port 3001
4. Add provider keys via `POST /api/keys {platform: 'google'}` (no auth needed)
5. Use `model='auto'` in calls — do NOT use `gemini-2.0-flash` directly

## Calling it

```python
import requests
resp = requests.post("http://localhost:3001/v1/chat/completions", json={
    "model": "auto",
    "messages": [{"role": "user", "content": "your prompt"}]
})
```

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `http://localhost:3001/*` | freellmapi local server |
| Bash | `npm start` in freellmapi folder | Start the proxy |

## Handoffs

- Cost-sensitive routing: `ollama-task-router` → freellmapi → paid cloud
- Benchmarking: run the same prompt via freellmapi across providers, compare results manually
