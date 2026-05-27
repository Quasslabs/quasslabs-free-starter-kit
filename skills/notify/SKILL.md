# SKILL: notify

**Bot:** operator · task-router · any
**Role:** Send alerts, reports, and checkpoint questions to Taylor via Telegram. The abstraction layer for all agent → human communication. Three message types: red-gate (immediate blocker), report (morning digest or session summary), checkpoint (yellow gate requiring a human decision). Discord and Google Chat wrappers can be added later behind the same interface.
**Ug-ug mode:** full
**Model:** haiku — message formatting is deterministic; no generation needed
**Tool compatibility:** Claude Code · Cursor · Codex
**Status:** beta
**Parallelizable:** yes - each call is an independent stateless HTTP send; no shared mutable state

---

## Model

**Verdict:** `phi4-mini` — message formatting is deterministic template fill; no generation needed.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Deterministic message formatting; no generation |
| Local (installed) | phi4-mini | Template fill within local capability |
| Local (ideal) | phi4-mini | Already installed; ideal for formatting tasks |

---

## When to invoke

- `task-router` finds a 🔴 RED gate → call `notify.red_gate()` immediately
- Session ends → call `notify.report()` with session summary
- Morning digest runs → call `notify.report()` with day brief
- `task-router` finds 🟡 YELLOW gate requiring a decision → call `notify.checkpoint()`
- Any time an agent needs human input before it can continue

---

## One-time setup (Telegram)

**Why Telegram:** free, instant, excellent Bot API, no partial setup to finish. Discord/Google Chat wrappers can be added later.

```bash
# Step 1: Create the bot
# Message @BotFather on Telegram → /newbot → follow prompts → copy token

# Step 2: Get your chat ID
# Message your new bot anything, then:
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
# Find "chat": {"id": <YOUR_CHAT_ID>} in the response

# Step 3: Store in Secrets Manager
aws secretsmanager create-secret --name TELEGRAM_BOT_TOKEN --secret-string "<token>"
aws secretsmanager create-secret --name TELEGRAM_CHAT_ID --secret-string "<chat_id>"

# Or for local use, add to .env:
# TELEGRAM_BOT_TOKEN=<token>
# TELEGRAM_CHAT_ID=<chat_id>

# Step 4: Test
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>&text=notify+skill+ready"
```

---

## Python interface

```python
import os, requests

TELEGRAM_API = "https://api.telegram.org"

def _send(text: str, parse_mode: str = "Markdown") -> bool:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    resp = requests.post(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
        timeout=10
    )
    return resp.status_code == 200


def red_gate(task: str, blocker: str, action_required: str) -> bool:
    msg = f"""🔴 *BLOCKER — {task}*

Cannot proceed without:
• {blocker}

*What to do:*
{action_required}

Reply *DONE* when complete or *SKIP* to continue without."""
    return _send(msg)


def report(title: str, body: str) -> bool:
    msg = f"""📋 *{title}*

{body}"""
    return _send(msg)


def checkpoint(task: str, question: str, options: list[str] = None) -> bool:
    opts = ""
    if options:
        opts = "\n" + "\n".join(f"  {i+1}. {o}" for i, o in enumerate(options))
    msg = f"""🟡 *CHECKPOINT — {task}*

{question}{opts}

Reply with your choice or any instruction to continue."""
    return _send(msg)
```

---

## Message formats

### 🔴 Red gate (immediate blocker)

```
🔴 BLOCKER — [Task name]

Cannot proceed without:
• [Specific thing missing — e.g. "REVENUECAT_KEY not in Secrets Manager"]

What to do:
[Exact step — e.g. "Log into RevenueCat → API Keys → copy secret key → add to
Secrets Manager as REVENUECAT_KEY (us-east-1)"]

Reply DONE when complete or SKIP to continue without.
```

### 📋 Report (morning digest / session summary)

```
📋 [Report title]

[Body — bullet list of completed items, open items, flags, next steps]
```

### 🟡 Checkpoint (decision needed)

```
🟡 CHECKPOINT — [Task name]

[Question requiring human input]
  1. [Option A]
  2. [Option B]

Reply with your choice or any instruction to continue.
```

---

## Standard report format (morning digest)

When used by the daily digest skill, structure the report body as:

```
✅ Done since last session:
• [item]

🔧 In progress:
• [item] — [status]

🔴 Blocked (needs you):
• [blocker + what to do]

🟡 Assumptions made (review when you can):
• [assumption]

📬 Emails prepped for review: [N]
🎫 Jira items updated: [N]

Next priority: [first thing to tackle when you start]
```

---

## Key rules / constraints

- **Red gates send immediately.** Do not buffer until a report.
- **One message per red gate.** Do not combine multiple blockers into one message — each needs a clear DONE/SKIP response.
- **Reports use Markdown.** Telegram supports `*bold*`, `_italic_`, `` `code` ``. Keep formatting simple.
- **Never include secrets in messages.** Reference secret names (e.g. "REVENUECAT_KEY"), not values.
- **If Telegram send fails:** log to `<logs>/...` with timestamp + message content. Do not silently drop.

---

## Adding Discord / Google Chat later

The `_send()` function is the only thing that changes. All call sites (`red_gate`, `report`, `checkpoint`) stay the same. Add a `NOTIFY_CHANNEL` env var (`telegram` | `discord` | `google_chat`) and dispatch accordingly:

```python
def _send(text: str, **kwargs) -> bool:
    channel = os.environ.get("NOTIFY_CHANNEL", "telegram")
    if channel == "telegram":
        return _send_telegram(text)
    elif channel == "discord":
        return _send_discord(text)
    elif channel == "google_chat":
        return _send_google_chat(text)
```

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `https://api.telegram.org/*` | Send messages via the Telegram Bot API |
| MCP | `mcp__keepassxc-secrets__*` | Read `Telegram/bot-token` + `Telegram/chat-id` from the vault |
| Filesystem | `<logs>/...` (write) | Append failed sends so they are not silently dropped |

## Handoffs

| Triggered by | Skill |
|---|---|
| Red gate detected | `skills/task-router/SKILL.md` |
| Morning report | `skills/daily-digest/SKILL.md` (future) |
| Session complete | `skills/lifecycle/session-handover/SKILL.md` |

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `_send_telegram` | All message types — HTTP POST to Telegram Bot API | yes | ✅ |
| `red_gate` | Immediate blocker alert — format + send one blocking message | yes | ✅ |
| `report` | Digest or session summary — format + send structured report | yes | ✅ |
| `checkpoint` | Decision prompt — format + send options list, await reply | yes | ✅ |
| `_send_discord` | Future channel — HTTP POST to Discord webhook | yes | ✅ |
| `_send_google_chat` | Future channel — HTTP POST to Google Chat webhook | yes | ✅ |
| `log_failed_send` | Fallback — write failed message to `<logs>/...` | yes | ❌ |

`log_failed_send` requires local filesystem write — not Lambda-compatible as written. All send functions are stateless HTTP calls and are strong Lambda candidates; the entire notify skill should run as a Lambda invoked by task-router, session-handover, and daily-digest.

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `message_type` | string | yes | `red_gate` \| `report` \| `checkpoint` |
| `task` | string | yes | Name of the task or session the message is about |
| `body` | string | yes | Main message content — blocker description, report body, or checkpoint question |
| `action_required` | string | no | `red_gate` only — exact step the human must take |
| `options` | string[] | no | `checkpoint` only — list of choices to present |
| `channel` | string | no | `telegram` (default) \| `discord` \| `google_chat` |

**Output:**
```json
{
  "status": "ok | error",
  "message_type": "red_gate | report | checkpoint",
  "delivered": true,
  "channel": "telegram",
  "telegram_message_id": 12345,
  "error": null
}
