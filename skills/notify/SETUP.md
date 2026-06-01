# SETUP: notify

**Skill:** `notify`
**Setup tier:** light (Telegram bot token + chat ID)
**Last verified:** 2026-05-31

## Dependencies

| Dep | Version | Install | Notes |
|---|---|---|---|
| requests (Python) | any | `pip install requests` | HTTP POST to Telegram API |

## Credentials / vault

| Secret | Where to store | How used |
|---|---|---|
| Telegram bot token | env var `TELEGRAM_BOT_TOKEN` | Auth header for Telegram API |
| Telegram chat ID | env var `TELEGRAM_CHAT_ID` | Destination for messages |

Create a bot via [@BotFather](https://t.me/BotFather), send yourself a message, then call
`https://api.telegram.org/bot<TOKEN>/getUpdates` to find your chat ID.

## How to run

```python
import os, requests
requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    json={"chat_id": os.environ["TELEGRAM_CHAT_ID"], "text": "Test message"}
)
```

Or invoke the skill for the abstraction layer (red_gate / report / checkpoint types).

## Verify it works

1. Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as env vars.
2. Run the snippet above → message arrives in Telegram within 5 seconds.
