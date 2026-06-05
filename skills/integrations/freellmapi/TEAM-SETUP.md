# Free LLM API — Team Setup Guide

Self-host a free-cloud LLM tier on your own machine. Zero cost. No credit card for most providers. Useful for benchmarking models, running throwaway experiments, and reducing paid cloud spend.

**Repos:**
- Proxy: https://github.com/tashfeenahmed/freellmapi (MIT, Node/TS)
- Provider list: https://github.com/cheahjs/free-llm-api-resources

---

## What it is

An OpenAI-compatible proxy that sits in front of ~14 free-tier LLM providers (Gemini, Groq, Cerebras, Mistral, OpenRouter, GitHub Models, …). It:
- Routes requests to whichever provider has capacity
- Automatically skips rate-limited providers and retries on the next one
- Gives you a single endpoint + bearer token, no per-provider key management in your code

**Where it fits in the inference chain:**
```
Local Ollama → Mac mini Ollama → free-cloud (this) → paid Anthropic/OpenAI
```

Use free-cloud for experiments and benchmarks. Use paid cloud for production work.

---

## Hard rule — non-sensitive content only

Free providers may train on inputs. Treat this as a public channel.

**Never send through freellmapi:**
- API keys, passwords, credentials of any kind
- Client names, project names, billing or worklog data
- PII (emails, phone numbers, SSNs)
- Internal business context

This is enforced in code (allowlist + pattern refusal), but the rule stands regardless.

---

## Prerequisites

- Node 20+ — check: `node --version`
- npm
- A free account on at least one provider (Gemini is fastest — no credit card)

---

## One-time install

```bash
# 1. Clone to wherever you keep tools
git clone https://github.com/tashfeenahmed/freellmapi ~/tools/freellmapi
cd ~/tools/freellmapi

# 2. Install dependencies
npm install

# 3. Generate an encryption key (used to store your provider keys at rest)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
# Copy the output — you'll use it in the next step

# 4. Create .env in the install directory
cat > .env << 'EOF'
ENCRYPTION_KEY=<paste-generated-key-here>
PORT=3001
DASHBOARD_ORIGINS=http://127.0.0.1:5599,http://localhost:5599
EOF
```

---

## Start the proxy

```bash
cd ~/tools/freellmapi

# Terminal 1 — proxy (keep running)
npm run dev -w server
# Healthy when you see: "injected env (3)" and a single :3001 listener

# Terminal 2 — admin dashboard (only needed to add/manage provider keys)
npm run dev -w client -- --host 127.0.0.1 --port 5599
# Open: http://127.0.0.1:5599
```

---

## Add free-tier provider keys

You need at least one provider key to use freellmapi. **Start with Gemini** — it has the highest free limits, doesn't require a credit card, and is the most stable.

---

### Step 1 — Get a free API key

#### Google Gemini (recommended first)

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with any Google account
3. Click **Create API key**
4. Select "Create API key in new project" (or pick an existing one)
5. Copy the key — it starts with `AIza`

Free limits: 1,500 requests/day, 1M tokens/minute. No credit card required.

---

#### Groq

1. Go to **https://console.groq.com/keys**
2. Create a free account (email + password, no card)
3. Click **Create API Key**
4. Give it a name (e.g. "freellmapi"), click Create
5. Copy the key immediately — it is only shown once. It starts with `gsk_`

Free limits: 14,400 requests/day across multiple models. Note: Groq may rotate or revoke free keys periodically — if it stops working, generate a new one.

---

#### Cerebras

1. Go to **https://cloud.cerebras.ai**
2. Sign up for a free account
3. Navigate to **API Keys** in the sidebar
4. Click **Create API Key**, copy the result

Free limits: generous (Cerebras publishes current limits at that URL). No credit card required.

---

#### OpenRouter

1. Go to **https://openrouter.ai**
2. Sign up and log in
3. Go to **https://openrouter.ai/keys**
4. Click **Create Key**, name it, copy the result. It starts with `sk-or-`

Free tier: $5 credit on signup, then pay-as-you-go. Many models have a free tier with rate limits — check the model list at openrouter.ai/models (filter "Free").

---

#### GitHub Models

1. Go to **https://github.com/marketplace/models**
2. Sign in with your GitHub account (no extra signup)
3. Click any model → **Get API key** or navigate to **https://github.com/settings/tokens**
4. Generate a **Personal Access Token (classic)** with no special scopes needed — the token itself is the credential
5. Copy the token — it starts with `ghp_`

Free limits: rate-limited per model; available to any GitHub account.

---

### Step 2 — Secure your keys

Provider API keys are credentials. Treat them like passwords.

**Do:**
- Store each key in a password manager (1Password, KeePassXC, Bitwarden)
- Keep them in `.env` files that are in `.gitignore`

**Never:**
- Paste a key into Slack, Teams, email, or a shared doc
- Commit `.env` to a git repo
- Share a key across team members — each person gets their own

The proxy encrypts your provider keys at rest using the `ENCRYPTION_KEY` in `.env`. This protects them on disk, but the keys are still sensitive — secure the source.

---

### Step 3 — Add keys to the proxy dashboard

The proxy stores your provider keys so your code never has to handle them directly.

1. Make sure the proxy and dashboard are running (see "Start the proxy" above)
2. Open **http://127.0.0.1:5599** in your browser
3. In the dashboard, go to **API Keys** or **Providers**
4. For each provider key you got in Step 1:
   - Select the matching platform from the dropdown (e.g. "google", "groq", "cerebras")
   - Paste your key into the field
   - Click **Save** or **Add**
5. The key is now encrypted and stored locally — the proxy will use it automatically

You can add multiple providers. The proxy will failover between them automatically if one hits a rate limit.

---

### Provider summary

| Provider | Free limits | Sign-up URL | Key format |
|---|---|---|---|
| Google Gemini | 1,500 req/day, 1M tok/min | https://aistudio.google.com/apikey | `AIza...` |
| Groq | 14,400 req/day | https://console.groq.com/keys | `gsk_...` |
| Cerebras | High limits | https://cloud.cerebras.ai | varies |
| OpenRouter | $5 free credit | https://openrouter.ai/keys | `sk-or-...` |
| GitHub Models | Free for GitHub users | https://github.com/settings/tokens | `ghp_...` |

For more free providers: https://github.com/cheahjs/free-llm-api-resources

---

## Wire into your code

Get your unified bearer token from the dashboard → Settings tab.

Set two environment variables:
```bash
export FREELLMAPI_URL=http://localhost:3001/v1
export FREELLMAPI_KEY=<unified-bearer-from-dashboard-settings>
```

Add to your shell profile (`.zshrc`, `.bashrc`) or project `.env`.

### Python usage (via shared lib)

If your team uses the shared `_lib_llm.py` routing library:

```python
from _lib_llm import call_free_cloud

# task_type must be: bench | experiment | scratch | public
result = call_free_cloud(
    prompt="Summarize ULID vs UUID in one sentence.",
    model="auto",       # recommended — proxy picks best available
    task_type="bench",
)

if result == "":
    print("Free-cloud unavailable — check proxy is running and FREELLMAPI_KEY is set")
```

### Direct OpenAI-compatible usage (any language)

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="<your-FREELLMAPI_KEY>",
)

response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Say hello."}],
)
print(response.choices[0].message.content)
```

### curl

```bash
curl http://localhost:3001/v1/chat/completions \
  -H "Authorization: Bearer $FREELLMAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "Say hello."}]}'
```

---

## Health check

```bash
# List available models
curl -s http://localhost:3001/v1/models \
  -H "Authorization: Bearer $FREELLMAPI_KEY" | python -m json.tool

# Quick Python verify
python -c "
import urllib.request, json, os
req = urllib.request.Request(
    'http://localhost:3001/v1/models',
    headers={'Authorization': f'Bearer {os.getenv(\"FREELLMAPI_KEY\", \"\")}'}
)
with urllib.request.urlopen(req, timeout=3) as r:
    print('UP — models:', len(json.loads(r.read()).get('data',[])))
"
```

---

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| Returns empty / 404 | Multiple proxy processes running | `lsof -i :3001` (Mac/Linux) or `netstat -ano \| findstr :3001` (Windows) → kill extras, start one |
| `Invalid API key` | FREELLMAPI_KEY not set or wrong | Check env var is set in current shell; get value from dashboard Settings |
| `model_not_found` | Specific model ID not in catalog | Use `model="auto"` or check `/v1/models` for valid IDs |
| Dashboard CORS error | .env missing DASHBOARD_ORIGINS | Add `DASHBOARD_ORIGINS=http://127.0.0.1:5599,http://localhost:5599` to .env |
| Groq 403 | Free key revoked (Groq rotates these) | Regenerate at console.groq.com/keys |

---

## Operational tips

- **Don't run 24/7** — start the proxy when you need it, stop when done
- **One process only** — the OS will round-robin between multiple instances and cause intermittent failures
- **Gemini is the most stable free tier** — use it as your primary; add others as backups
- **Provider failover is automatic** — if Groq is rate-limited, the proxy routes to Gemini without you doing anything
