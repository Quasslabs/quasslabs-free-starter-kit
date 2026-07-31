# SKILL: notify

**Bot:** any · communication primitive
**Role:** Send alerts, reports, and checkpoint questions to a human via Telegram. Abstraction layer for all agent -> human communication. Three message types: red_gate (immediate blocker), report (digest or session summary), checkpoint (yellow gate needing a decision).
**Ug-ug mode:** full
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** yes
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- A blocker prevents the agent from continuing -> `red_gate`
- Session ends or morning digest runs -> `report`
- Decision required before continuing -> `checkpoint`
- Slash trigger: `/notify`

## Steps

1. Read `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` from env (vault-loaded).
2. Format message per type (red_gate / report / checkpoint).
3. POST to `https://api.telegram.org/bot<token>/sendMessage` with Markdown parse mode.
4. On failure: append to a local fallback log; never silently drop.
5. Never include secret VALUES in message bodies — reference key names only.

## Input

- `level` — one of `red_gate | report | checkpoint`
- `message` — string body (Markdown supported)

## Output

- `{"status": "ok" | "error", "level": "...", "delivered": bool, "error": null | str}`

## Handoffs

- `session-handover` — calls `notify.report()` when a session boundary occurs
- `reflect` — may call `notify.report()` with retro summary

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `https://api.telegram.org/*` | Send messages via Telegram Bot API |
| Filesystem | `logs/notify-failed.log` (write) | Append failed sends |

## Lambda candidates

All three send paths (`red_gate`, `report`, `checkpoint`) are stateless HTTP POSTs — strong Lambda candidates.
