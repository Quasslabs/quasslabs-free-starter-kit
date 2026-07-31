# Functions — notify

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `format_red_gate(task, blocker, action)` | str, str, str | str | Template fill; deterministic |
| `format_report(title, body)` | str, str | str | Template fill |
| `format_checkpoint(task, question, options)` | str, str, list | str | Template fill |
| `send(level, message)` | str, str | dict | HTTP POST to Telegram |

## AI-assisted steps

None. All message formatting is template-driven.

## External services

| Service | Endpoint | Auth |
|---|---|---|
| Telegram Bot API | `https://api.telegram.org/bot<token>/sendMessage` | `TELEGRAM_BOT_TOKEN` env |
