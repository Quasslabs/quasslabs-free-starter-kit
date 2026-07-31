# Functions — ollama-task-router

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `route(task)` | str | dict | Returns `{target, model, reason}` |
| `build_prompt(task)` | str | str | Construct the JSON-mode classifier prompt |

## AI-assisted steps

| Step | Model | Notes |
|---|---|---|
| Classification call | phi4-mini (local) | via `_lib_llm.call_llm_json` |

## External services

| Service | Endpoint | Notes |
|---|---|---|
| Ollama | `http://localhost:11434/api/generate` | Local-only; OLLAMA_HOST env overrides |
