# Setup — notify

## Env vars

| Name | Required | Notes |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | yes | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | yes | Your chat id from `getUpdates` |

## Vault entries (KeePassXC)

| Entry name | Field | Maps to env |
|---|---|---|
| `Telegram/bot-token` | password | `TELEGRAM_BOT_TOKEN` |
| `Telegram/chat-id` | password | `TELEGRAM_CHAT_ID` |

## Ollama models

None required.

## One-time Telegram setup

1. Message `@BotFather` -> `/newbot` -> copy token.
2. Message your new bot anything, then `curl "https://api.telegram.org/bot<TOKEN>/getUpdates"` to find your chat id.
3. Store both in the vault entries above.
