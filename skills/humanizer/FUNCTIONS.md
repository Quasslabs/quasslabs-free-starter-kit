# FUNCTIONS — humanizer

## Pure functions (Lambda candidates)

| Function | Input | Output | Notes |
|---|---|---|---|
| `scan_em_dashes(text)` | string | list[(line_no, count)] | Flag lines with > 1 em-dash; pattern `—` |
| `scan_ai_vocab(text)` | string | list[(line_no, word)] | Regex against curated AI-vocab list (see source SKILL.md sections 4–7 + 12–16) |
| `scan_rule_of_three(text)` | string | list[(line_no, span)] | Detect "X, Y, and Z" triplets with shallow content |
| `scan_passive_voice(text)` | string | list[(line_no, span)] | Wrapper around an existing passive-voice library (e.g. `passivepy` or `textatistic`) |
| `scan_filler_phrases(text)` | string | list[(line_no, phrase)] | "It's worth noting that", "It is important to remember", etc. |
| `score_ai_ness(text)` | string | float 0–1 | Aggregate of all scans; gate for whether full rewrite is needed |
| `extract_voice_profile(sample)` | sample string | dict (sentence_len_dist, vocab_register, transition_style, etc.) | Used by voice-calibration mode |

## AI-assisted steps

| Step | Model | Reason | Token estimate |
|---|---|---|---|
| Pattern-by-pattern rewrite | sonnet | Tone-preserving rewrite; haiku flattens voice | ~2k in / ~2k out per 500-word section |
| Voice-sample analysis (optional) | sonnet | Judgment over rhythm, register, recurring tics | ~3k in / ~500 out one-shot |
| Final anti-AI pass (self-critique) | sonnet | "What still reads as AI?" → "Now fix it" | ~3k in / ~2k out |

## External services

| Service | Auth | Notes |
|---|---|---|
| None | — | Skill is fully local-and-LLM. No external calls. |

## Recommended pipeline

```
scan_ai_ness()  →  if > 0.4 →  invoke sonnet rewrite (with voice profile if available)
                              →  scan_ai_ness() again
                              →  if > 0.2 →  invoke anti-AI self-critique pass
                              →  emit
                ↘  if <= 0.4 →  emit as-is
```

This keeps cost low on already-clean text and only fires the heavier passes when needed.
