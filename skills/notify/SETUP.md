# SETUP: notify

**Skill:** `notify`
**Setup tier:** light (Telegram bot token + chat ID)
**Last verified:** 2026-05-31

## Dependencies

| Dep | Version | Install | Notes |
|---|---|---|---|
| requests (Python) | any | `pip install requests` | HTTP POST to Telegram API |
| Python | 3.x | present | runtime only |

## Credentials / vault

| Secret | Vault entry | How used |
|---|---|---|
| Telegram bot token | `Telegram/bot-token` (KeePass ai-hub.kdbx) | `get_secret("Telegram/bot-token")` |
| Telegram chat ID | `Telegram/chat-id` (KeePass ai-hub.kdbx) | `get_secret("Telegram/chat-id")` |

Alternatively set as Windows env vars `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.
Run `telegram-setup` skill first if Telegram is not yet wired.

## .claude / harness wiring

None required beyond vault access.

## How to run

```python
# From <routines>/_lib_ollama.py
from _lib_ollama import notify_telegram
notify_telegram("Subject", "Body text", "report")   # report | red_gate | checkpoint
```

## Verify it works

1. `python -c "from _lib_ollama import notify_telegram; notify_telegram('Test', 'notify wired', 'report')"`
2. Telegram message arrives within 5 seconds.
