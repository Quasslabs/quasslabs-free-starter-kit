# LESSONS: freellmapi

## Key lessons

- **404 "Cannot POST" = stale process, NOT a bad key.** Kill duplicate :3001 processes first, then retry. A bad key returns 401.
- **Use `model='auto'`** — do not specify `gemini-2.0-flash` or other provider-specific names directly; the proxy resolves automatically.
- **Add providers via API, not .env** — `POST /api/keys {platform: 'google'}` is the correct path. No auth required on this endpoint.
- **ENCRYPTION_KEY change does not affect existing keys** — the unified key is plaintext in sqlite and is unaffected.
- **`.env` requires `DASHBOARD_ORIGINS`** for the :5599 dashboard to load — omitting it silently blocks the UI.
