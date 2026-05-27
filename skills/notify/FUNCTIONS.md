# Functions — notify

## Pure functions (Lambda candidates)

None — notify is a thin wrapper around the Telegram Bot API. No stateful processing.

## Key implementation

**`notify_telegram(title, body, level)`** — `<routines>/_lib_ollama.py` lines 81–109

```python
def notify_telegram(title: str, body: str, level: str = "report") -> bool
```

| Property | Value |
|---|---|
| Env deps | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| KeePass paths | `Telegram/bot-token`, `Telegram/chat-id` |
| Setup skill | `skills/telegram-setup/SKILL.md` |
| HTTP endpoint | `POST https://api.telegram.org/bot{token}/sendMessage` |
| Payload | `{chat_id, text, parse_mode: "Markdown"}` |
| Timeout | 10 seconds |
| Fail behavior | Silent — returns `False` if env vars missing or network error |

## Level enum

| Level | Meaning | When to use |
|---|---|---|
| `report` | Informational digest | Morning summary, nightly run results, worklog suggestions |
| `checkpoint` | Question requiring human decision | Approval gates, "post these worklogs?", stale ticket alerts |
| `red_gate` | Immediate blocker | Script failure, auth error, data integrity problem |

## Callers (routines that use notify_telegram())

All 11 files import from `<routines>/_lib_ollama.py`:
- `daily-digest.py` — morning digest report
- `pr-gemini-poll.py` — PR review checkpoint
- `pr-review.py` — PR result report
- `fathom-sync.py` — sync completion report
- `monthly-taxbot.py` — tax run completion report
- `morning-startup.py` — startup checkpoint
- `weekly-report.py` — weekly summary report
- `night-tasks.py` — nightly run report
- `morning-debrief.py` — morning debrief report
- `evening-maintenance.py` — maintenance report
- `delphina-at` (future) — worklog suggestion checkpoints

## External services

| Service | Endpoint | Auth |
|---|---|---|
| Telegram Bot API (send) | `https://api.telegram.org/bot{token}/sendMessage` | Token in URL |
| Telegram Bot API (setup) | `https://api.telegram.org/bot{token}/getUpdates` | Token in URL |
| KeePassXC vault | `<your-secrets-vault>` | Master password via stdin to `keepassxc-cli` |

## Setup (one-time)

See `skills/telegram-setup/SKILL.md` for the full step-by-step: BotFather → vault storage → env vars → test.
