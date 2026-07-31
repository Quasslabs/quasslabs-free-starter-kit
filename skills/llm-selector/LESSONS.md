# Lessons — llm-selector

## 2026-06-11 — initial release

- Pure lookup table beats LLM-based "which model" calls on cost and latency. Don't add an LLM hop here.
- Unknown task_type defaults to `reason` tier (safe middle ground), not the cheapest.
- Budget-aware downgrade is a one-step shift, not a full re-rank — keeps the primary catalog stable.
