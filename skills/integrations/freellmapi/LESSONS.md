# LESSONS: freellmapi

## Duplicate processes cause intermittent 404/401

Windows allows multiple `npm run dev` instances to bind `:3001`. The OS round-robins requests between them. A stale process without the `/v1` route answers some calls → intermittent `Cannot POST /v1/chat/completions` (404) or `Invalid API key` (401) on alternate requests.

Fix: `netstat -ano | findstr :3001` → `taskkill /PID <each> /F` → start exactly ONE process.

Healthy startup shows: `injected env (3)` in stdout + single listener.

---

## .env is required — proxy behaves incorrectly without it

No `.env` → `ENCRYPTION_KEY` unset → dashboard CORS rejects `:5599` (only `:5173` allowed by default). Dashboard appears to load but key-add calls fail silently.

`.env` minimum:
```
ENCRYPTION_KEY=<32-byte hex>
PORT=3001
DASHBOARD_ORIGINS=http://127.0.0.1:5599,http://localhost:5599
```

Generate key: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`

---

## Use model="auto", not specific model IDs

`gemini-2.0-flash`, `llama-3.3-70b-versatile`, and other well-known names may not be in this build's model catalog → `400 model_not_found`.

`model="auto"` lets the proxy pick the best available provider. Check `/v1/models` for the actual catalog IDs in your build if you need to target a specific model.

---

## FREELLMAPI_KEY is the unified bearer — don't confuse with provider keys

There are two types of keys:
1. **Provider keys** — per-provider secrets (Gemini key, Groq key, etc.) — stored encrypted in the proxy, never exposed
2. **Unified bearer token** — a single token the proxy issues — this is `FREELLMAPI_KEY` env var

`ENCRYPTION_KEY` in `.env` encrypts provider keys at rest. Changing `ENCRYPTION_KEY` does NOT change the unified bearer token (which is plaintext in `settings.unified_api_key`).

---

## Groq free keys expire / get revoked

Groq free API keys are rotated or revoked periodically. A working key today may return `403` next week with no warning. If Groq calls start failing: regenerate at `console.groq.com/keys`, update the dashboard. Gemini free keys are more stable — use Gemini as the primary provider.

---

## Sensitive pattern guard: "client" blocks legitimate prompts

`_lib_llm._SENSITIVE_PATTERNS` includes `\bclient\b` as a sensitive marker (blocks business-engagement context). This can accidentally refuse prompts that legitimately contain the word "client" in a non-sensitive sense (e.g., "HTTP client", "Redis client").

Workaround: rephrase ("HTTP connection", "Redis connection") or use `allow_sensitive_override=True` for vetted non-sensitive prompts that happen to contain the word.

---

## call_free_cloud task_type must be exactly in the allowlist

`task_type` is checked against `{"bench", "experiment", "scratch", "public"}` — case-sensitive, exact match. Common mistakes:
- `"benchmark"` → refused (use `"bench"`)
- `"test"` → refused (use `"experiment"`)
- `"general"` → refused (use `"scratch"`)

When refused, `call_free_cloud` returns `""` and prints the reason to stdout. Always check stdout if getting empty returns.

---

## Keep proxy off by default — it's not a persistent service

freellmapi is for benchmarking and throwaway experiments. Running it 24/7 is unnecessary and leaves a port open. Start it when needed, stop when done.

For scheduled benchmark routines, the calling script should check `is_freellmapi_available()` first and skip gracefully if the proxy isn't running — don't rely on it always being up.

---

## cheahjs/free-llm-api-resources is the canonical list of new providers

When a provider's free tier gets rate-limited or revoked, the best place to find replacements is: https://github.com/cheahjs/free-llm-api-resources

This repo is actively maintained and tracks which providers offer free tiers, their limits, and whether they require credit cards. Cross-check against freellmapi's supported platform list before signing up.
