# LESSONS — humanizer

_(Seeded 2026-05-14 from blader/humanizer v2.5.1 import. Append corrections + tuning notes here as the skill is used in production.)_

## Import-time observations

- **Source format vs our triad.** blader/humanizer ships a single 559-line SKILL.md with YAML frontmatter + `allowed-tools` array. Our triad adds `FUNCTIONS.md` + `LESSONS.md` alongside; the source body is preserved verbatim under a `# Humanizer: ... (source body)` heading so future upstream syncs are a one-line diff.
- **Ug-ug mode = none.** Most skills in our hub use `lite` or `full`. Humanizer is an exception — its output IS the user-facing prose. Compressing the SKILL.md instructions risks Claude internalizing ug-ug style and applying it to the rewrite. Keep this skill un-compressed.
- **Voice-sample mode is the key differentiator.** Default humanization produces "clean but generic" prose. The voice-calibration path (user provides a writing sample, skill extracts patterns, rewrite matches) is what makes this worth importing over building from scratch.

## When to use which model

- **sonnet** — default. Haiku will follow the rules but flatten cadence; it's literal-minded and produces something that reads humanized in the same way every time. That sameness is itself an AI tell.
- **opus** — only for high-stakes voice matching (e.g. client signature pieces) where the sample is short and the rewrite is long.
- **haiku** — only for the regex pre-pass (counting em-dashes, flagging AI vocab) before deciding whether to invoke the full skill.

## Anti-patterns to watch

- Don't run humanizer on output that's already gone through humanizer. Cycle compounds — the second pass over-corrects and produces twee, performatively-imperfect prose with too many "kind of"s and "I genuinely"s.
- Don't invoke on code, JSON, or anything structured. The skill will try to rewrite identifiers and string literals.
- Don't pair with ug-ug-ultra in the same pipeline. They have opposite goals; pick one.

## Integration with our existing skills

- `marketing/blog-newsletter` should call humanizer as a final pass before publishing.
- `marketing/content-brief` should NOT call humanizer — briefs are internal scaffolding, not finished prose.
- `for-russ-doc-builder` should call humanizer on the narrative sections only, not on the code-block or diagram-caption sections.
- `client-handoff-zip` should call humanizer on the README.md and CLAUDE.md it generates.

## Cost notes

- Per-section: ~2k in / ~2k out @ sonnet = ~$0.012 per 500-word section.
- A 2,000-word blog post = ~$0.05 in sonnet calls if both rewrite + anti-AI passes fire.
- The regex pre-pass (`score_ai_ness`) costs $0 and routes ~40% of text past full processing in practice.

---

## Repo additions — 2026-05-18 triage (Pull-in attribution)

Source: `<notes>/...` → "Developer Tools triage".

- **`hardikpandya/stop-slop` (3.2k★)** — skill file specifically for removing "AI tells" from prose (slop phrases, hedge patterns, inflated transitions). **Adopt:** mine its tell-list to extend humanizer's `score_ai_ness` regex pre-pass — stop-slop's pattern set is a second source of AI-tell signatures beyond blader/humanizer's 29 patterns. Merge non-overlapping patterns into the pre-pass; keep blader/humanizer as the rewrite engine. Pattern-after (extend the detector), not a separate pipeline stage.
