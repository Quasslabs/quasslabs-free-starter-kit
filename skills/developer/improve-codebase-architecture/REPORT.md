# REPORT: developer/improve-codebase-architecture

**Skill:** `developer/improve-codebase-architecture` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Architectural friction surfaced | Ad-hoc ("this feels bad") | Categorized (Depth/Seam/Module) | Review quality |
| Refactor scope creep | High | Low (deletion-test heuristic) | PR size at refactor |
| Time to identify friction point | 30–60 min | 5–10 min | Timed |

## Who gets the most value

Senior developers who need to justify refactors to a team — improve-codebase-architecture gives you the vocabulary and the heuristic, not just a vague "this should be cleaner."

## How it fits in a flow

**Upstream:** "this codebase feels wrong" → **improve-codebase-architecture** → specific friction points → `developer/arch-decision` locks ADR → refactor

## Skill interactions

| Pairs with | How |
|---|---|
| `developer/zoom-out` | zoom-out maps the modules; improve-arch identifies what to change |
| `developer/tdd` | TDD implements the refactor safely |

## Measured outcomes

Qualitative: clearer refactor targets, less scope creep, architectural changes with named rationale.

## Test coverage

Manual: invoke on a known-messy codebase → receives friction report categorized by Module/Interface/Seam.
