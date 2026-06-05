---
name: freellmapi
description: "Use when accessing the free-cloud LLM tier — benchmarking models, running throwaway experiments, or testing prompts against multiple providers without spending cloud budget. Also use when a team member asks how to set up freellmapi, how to add a provider key, or why call_free_cloud() is returning empty string."
metadata:
  version: 1.0.0
---

# SKILL: freellmapi

**Bot:** any
**Role:** Self-hosted OpenAI-compatible proxy aggregating ~14 free-tier LLM providers (Gemini, Groq, Cerebras, Mistral, GitHub Models, OpenRouter, …) with automatic failover. The free-cloud rung in the LLM fallback chain.
**Ug-ug mode:** full
**Model:** haiku — routing decisions are deterministic; no deep reasoning required
**Tool compatibility:** Claude Code · Cursor
**Status:** beta
**Parallelizable:** yes — per-call stateless; proxy handles concurrency internally

---

## Fallback chain position

```
local Ollama (Windows) → Mac mini Ollama → free-cloud (this) → paid cloud (Anthropic)
```

freellmapi sits BELOW local inference and ABOVE paid cloud. Use it for:
- Model benchmarking (`llm-bench` skill)
- Throwaway one-off prompts
- Comparing provider output quality at $0

---

## HARD RULE — non-sensitive content only

Free providers MAY train on inputs. This tier is a public channel.

**Never send:**
- Vault / credentials / API keys
- Client names, worklog content, billing data
- PII (emails, SSNs, phone numbers)
- Bedrock prompts, internal engagement context

Enforced in code by `_lib_llm.call_free_cloud()` — allowlisted task types + sensitive-pattern refusal. The rule stands regardless: treat free-cloud as public.

---

## When to invoke

- "Run this prompt through the free tier"
- "Benchmark X model vs Y"
- "Why is call_free_cloud returning empty string?"
- Team member needs to set up freellmapi
- Adding a new free-tier provider key
- Checking which models are available

---

## Repos

| Repo | Purpose |
|---|---|
| `tashfeenahmed/freellmapi` (MIT) | The proxy — what you install and run |
| `cheahjs/free-llm-api-resources` | Curated list of free-tier LLM providers — use this to find new providers to add |

---

## Setup (one-time per machine)

### Prerequisites
- Node 20+ (`node --version`)
- npm
- Free-tier account on ≥1 provider (Gemini is fastest signup — no credit card)

### Steps

```bash
# 1. Clone
git clone https://github.com/tashfeenahmed/freellmapi <your-install-dir>
cd <your-install-dir>

# 2. Install
npm install

# 3. Create .env (required — proxy won't start correctly without it)
#    ENCRYPTION_KEY encrypts stored provider keys at rest
#    Generate via: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
cat > .env << 'EOF'
ENCRYPTION_KEY=<generated-key>
PORT=3001
DASHBOARD_ORIGINS=http://127.0.0.1:5599,http://localhost:5599
EOF

# 4. Start proxy
npm run dev -w server
# Proxy is now at http://localhost:3001/v1
# Healthy startup shows: "injected env (3)" + single listener on :3001

# 5. Start dashboard (separate terminal, to add provider keys)
npm run dev -w client -- --host 127.0.0.1 --port 5599
# Dashboard: http://127.0.0.1:5599
```

### Add provider keys (via dashboard or API)

Open `http://127.0.0.1:5599` and paste free-tier keys. Recommended first providers:

| Provider | Free tier | Signup |
|---|---|---|
| Google Gemini | 1,500 RPD, 1M TPM | aistudio.google.com |
| Groq | 14,400 RPD | console.groq.com |
| Cerebras | High limits | cloud.cerebras.ai |
| OpenRouter | $5 free credit | openrouter.ai |
| GitHub Models | Free for GH users | github.com/marketplace/models |

Or add via API (no auth required, CORS-gated to localhost):
```bash
curl -X POST http://localhost:3001/api/keys \
  -H "Content-Type: application/json" \
  -d '{"platform": "google", "key": "<your-gemini-key>", "label": "gemini-main"}'
```

### Set env vars (for _lib_llm integration)

```bash
# Get unified bearer token from dashboard Settings tab
FREELLMAPI_URL=http://localhost:3001/v1
FREELLMAPI_KEY=<unified-bearer-from-dashboard>
```

Set in user environment (Windows: System Properties → Environment Variables) or project `.env`.

---

## Usage from Python

Via `_lib_llm.call_free_cloud()` (standard entry point — handles all guards):

```python
from _lib_llm import call_free_cloud

# task_type MUST be one of: bench | experiment | scratch | public
result = call_free_cloud(
    prompt="Summarize ULID vs UUID in one sentence.",
    model="auto",          # recommended — lets proxy pick best available
    task_type="bench",
)
# Returns "" if guard refused or proxy is down — caller falls back to local
```

**model values:**
- `"auto"` — proxy picks the best available (recommended)
- Check `GET /v1/models` for specific model IDs in your build

---

## Health check

```bash
# Check proxy is up
curl -s http://localhost:3001/v1/models \
  -H "Authorization: Bearer $FREELLMAPI_KEY" | python -m json.tool | head -20

# From Python
from _lib_llm import call_free_cloud
out = call_free_cloud("Say OK.", model="auto", task_type="bench")
print(repr(out))  # "OK" = working; "" = guard refused or proxy down
```

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `call_free_cloud` returns `""` | Guard refused (wrong task_type or sensitive content) | Check task_type is in {bench, experiment, scratch, public}; check prompt for sensitive patterns |
| `Cannot POST /v1/chat/completions` (404) | Duplicate `npm run dev` processes on :3001 | `netstat -ano \| findstr :3001` → `taskkill /PID <each> /F` → start ONE instance |
| `Invalid API key` (401) | Stale process answering, or FREELLMAPI_KEY not set | Kill duplicates; verify env var is set |
| `model_not_found` (400) | Model ID not in this build's catalog | Use `model="auto"` or check `/v1/models` |
| `.env` not found | Proxy started from wrong directory | `cd` to install dir before `npm run dev` |
| Dashboard CORS error | DASHBOARD_ORIGINS not set in .env | Add `DASHBOARD_ORIGINS=http://127.0.0.1:5599,http://localhost:5599` to .env |
| Groq 403 | Groq key revoked (free keys expire/rotate) | Regenerate at console.groq.com/keys and re-add |

---

## Operational notes

- **Keep proxy off by default** — start only when benchmarking or experimenting; not a persistent service
- **Single instance rule** — Windows allows multiple processes on :3001; only one should run
- **Provider failover** — proxy automatically skips rate-limited providers; no manual intervention needed
- **New providers** — check `cheahjs/free-llm-api-resources` for updated free-tier options; add via dashboard or API

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `http://localhost:3001/*` | Proxy API calls |
| Network | `http://127.0.0.1:5599/*` | Dashboard access |
| Filesystem | `<install-dir>/.env` | Read encryption key + config |

## Handoffs

| Next step | Where |
|---|---|
| Model benchmarking | `skills/llm-bench/SKILL.md` |
| Full LLM routing | `<routines>/_lib_llm.py` — `call_free_cloud()` |
| Provider resource list | https://github.com/cheahjs/free-llm-api-resources |
