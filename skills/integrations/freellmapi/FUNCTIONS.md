# FUNCTIONS: freellmapi

## Pure functions (Lambda candidates)

| Function | Input | Output | Notes |
|---|---|---|---|
| `call_free_cloud(prompt, system)` | str, str | str | POST to localhost:3001/v1/chat/completions, model=auto |
| `add_provider(platform)` | str | None | POST /api/keys — no auth needed |
| `list_providers()` | — | list | GET /api/keys — returns active providers |

## External services

| Service | Endpoint | Auth |
|---|---|---|
| freellmapi local proxy | `http://localhost:3001` | None (local) |
| Provider APIs | Proxied by freellmapi | Provider keys stored in freellmapi sqlite |
