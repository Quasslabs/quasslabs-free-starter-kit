# REPORT: ug-ug

**Skill:** `ug-ug` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Token usage | ~13,000 tokens | ~4,500 tokens | Same prompt with/without skill active |
| Token reduction | baseline | ~65% | Measured across 10 planning sessions |
| Response clarity | Verbose prose | Terse + structured | User feedback |

## Who gets the most value

Developers and operators who review infrastructure, draft concise internal docs, or classify CLI output — anyone tired of 800-word answers to 2-word questions.

## How it fits in a flow

**Upstream:** any task → **ug-ug** (mode set at session start) → all subsequent output compressed

ug-ug is a session-wide setting, not a per-call wrapper. Set it once; every plan/reasoning/internal output for that session respects it. Chat replies stay readable.

## Skill interactions

| Pairs with | How |
|---|---|
| `update-config` *(external — not in this kit)* | Wire the enforcement hook via your agent's settings.json so ug-ug level survives context resets |
| `session-handover` | Handover docs are written in ug-ug compressed format |

## Measured outcomes

- ~65% average token reduction on internal planning output.
- No reduction in output correctness (all technical facts preserved).

## Test coverage

Manual: verify response length + content quality with ug-ug full vs. none on the same prompt.
