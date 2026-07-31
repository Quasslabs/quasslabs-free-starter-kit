# Lessons — task-router

## 2026-06-11 — initial release

- Keyword heuristics catch ~80% of red gates without LLM cost. Anything less obvious belongs in `ollama-task-router` (which uses a real model).
- Yellow notes are NOT warnings to ignore — they show up in the session report so the human reviews assumptions before sign-off.
- `estimated_cost` is always 0.0 in the free tier; downstream `llm-selector` computes the real number.
