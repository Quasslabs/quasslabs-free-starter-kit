# Lessons Learned — ug-ug

| Lesson | Why it matters | Source |
|---|---|---|
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for ug-ug. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## Repo additions — 2026-05-16/17 triage (Pull-in attribution)

Source: `<notes>/...` → "TQuass 2026-05-06" + "2026-05-17 TaylorQ batch".

- **`rtk-ai/rtk` (48.6k★ Apache)** — CLI proxy that reduces LLM token consumption 60–90% on common dev commands. Single Rust binary, zero deps. Routes short/repetitive commands through a compressed path before hitting the LLM. **Adopt:** pair with `ug-ug` skill as a complementary layer — rtk compresses at the CLI call level; ug-ug compresses at the prompt/reasoning level. Together they represent max token efficiency. Install: single Rust binary, download from rtk-ai/rtk releases. Test before adopting — verify it doesn't strip context that ug-ug formatting depends on. Route: ug-ug applies ultra compression → rtk reduces token footprint of the resulting commands → cost floor.
- **`JuliusBrussee/ug-ug` (51k★)** — Claude Code skill that cuts ~65% of tokens via "ug-ug compression". This is the same concept as our `ug-ug` skill — independent implementation. **Pattern to adopt:** compare its compression heuristics against ours; mine for compression rules we don't yet apply (it ranks high enough to be a credible reference impl). Do NOT vendor — our ug-ug is original; use only as a benchmark/alignment reference. License unverified → treat as pattern-after.
