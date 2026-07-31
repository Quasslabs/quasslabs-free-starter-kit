# Lessons — ollama-task-router

## 2026-06-11 — initial release

- JSON-mode (`format=json` in the Ollama API) is mandatory; freeform generations drift off the locked schema.
- phi4-mini is the right size for this — classification at ~200 tokens output. Don't escalate to a 7B model for routing.
- Caller should treat the response as advisory; the dispatch layer still owns retry / fallback.
