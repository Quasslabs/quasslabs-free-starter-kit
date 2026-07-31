# Lessons — operator

## 2026-06-11 — initial release

- Keyword routing over a small allowlist beats LLM routing for the entry-point skill. Latency is zero and the failure mode (`skill: null`) is explicit and easy to handle upstream.
- Order of allowlist matters: more specific keywords (lint, validate) come before more general ones (skill, build). Iterate in declared order; first match wins.
- "no match" is a legitimate output. Never guess. The caller decides whether to fall back to a downstream LLM router or to prompt the user.
