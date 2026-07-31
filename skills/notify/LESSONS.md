# Lessons — notify

## 2026-06-11 — initial release

- One message per red gate. Combining multiple blockers into a single message defeats the DONE/SKIP reply contract.
- Never include secret values — reference key names (e.g. `STRIPE_SECRET_KEY`) only. Telegram logs are not a vault.
- On send failure, append to `logs/notify-failed.log` with timestamp + body. Silent drops cause agents to think they delivered a message they didn't.
- Telegram Markdown parse mode is finicky around underscores and brackets in code-like strings — fall back to plain text on parse errors rather than failing the call.
