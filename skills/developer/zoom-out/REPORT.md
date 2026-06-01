# REPORT: developer/zoom-out

**Skill:** `developer/zoom-out` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time stuck inside a single file | Until you give up | 1-prompt escape | Self-reported |
| Architecture clarity | Local (in-file) | Module-level view | Reviewer feedback |

## Who gets the most value

Any developer who's spent 45 minutes fixing one file only to realize the bug was in a completely different layer. zoom-out surfaces the module map in a single prompt so you know where you actually are.

## How it fits in a flow

**Upstream:** stuck inside a file / wrong abstraction level → **zoom-out** → module-map → continue at the right layer

Note: `disable-model-invocation: true` — human-triggered only; not auto-chained by other skills.

## Skill interactions

| Pairs with | How |
|---|---|
| `developer/improve-codebase-architecture` | zoom-out reveals where; improve-arch decides what to change |

## Measured outcomes

Qualitative: developers report resolving stuck states in < 5 min after invoking zoom-out.

## Test coverage

Manual: invoke on any codebase → receive module-map using Module/Interface/Depth/Seam/Adapter vocabulary.
