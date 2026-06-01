# SETUP: integrations/freellmapi

**Skill:** `integrations/freellmapi`
**Setup tier:** involved (self-hosted proxy server)
**Last verified:** 2026-05-31

freellmapi is a self-hosted OpenAI-compatible proxy that aggregates ~14 free-tier LLM
providers (Gemini, Groq, Cerebras, OpenRouter, GitHub Models, etc.) with automatic failover.

## Dependencies

| Dep | Install | Notes |
|---|---|---|
| Node.js | 18+ | present on most dev machines |
| npm | bundled with Node | for `npm install` + `npm run build` |

```bash
git clone https://github.com/tashfeenahmed/freellmapi
cd freellmapi
cp .env.example .env        # edit: set ENCRYPTION_KEY + DASHBOARD_ORIGINS (for :5599 dashboard)
npm install
npm run build -w server
```

## Credentials / vault

No API key required for the proxy itself. Add providers after starting:
```bash
# Add a provider (no auth needed for this endpoint)
curl -X POST http://localhost:3001/api/keys -H "Content-Type: application/json" -d '{"platform":"google"}'
```

Set an encryption key (optional but recommended):
```bash
ENCRYPTION_KEY=<random-string> node server/dist/index.js
```

## How to run

```bash
# from inside the freellmapi/ directory you cloned into:
cd server
node dist/index.js
# Proxy now at http://localhost:3001/v1 (OpenAI-compatible)
```

Call with `model='auto'` (not a specific model name) for automatic provider failover.

## Verify it works

1. `curl http://localhost:3001/v1/models` → returns list of available models.
2. `curl http://localhost:3001/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"auto","messages":[{"role":"user","content":"hello"}]}'` → response from a free provider.
