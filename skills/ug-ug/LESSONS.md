# Lessons — ug-ug

## 2026-06-11 — initial release

- Banned-opener list was originally enforced at every level; that broke chat replies at `lite`. Now banned openers only apply to non-chat output (plans, LESSONS, handovers).
- `full` is the right internal default. Higher levels (`extra-ug`/`maximum-ug`) are opt-in per session — users who set them once want them again.
- ROI defended in `evals/run.py`. Treat the claimed range (30-60%) as the floor, not the average — pathological prose-heavy inputs compress further.
