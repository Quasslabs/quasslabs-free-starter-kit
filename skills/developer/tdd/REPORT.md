# REPORT: developer/tdd

**Skill:** `developer/tdd` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Feature shipped without tests | Common | Rare | PR reviews |
| Scope creep per feature | High | Low (vertical-slice constraint) | Feature size at merge |
| Regressions from untested code | Frequent | Reduced | Bug tracking |

## Who gets the most value

Developers who know TDD is good practice but skip it under deadline pressure. tdd structures the discipline as a sequence, not a philosophy — write the failing test, implement just enough to pass, then refactor.

## How it fits in a flow

**Upstream:** feature description → **tdd** → failing test → implementation → refactor → `developer/staged-test-runner` validates

## Skill interactions

| Pairs with | How |
|---|---|
| `developer/improve-codebase-architecture` | architecture is locked before TDD begins |
| `developer/zoom-out` | zoom-out maps the module; tdd tests one slice at a time |

## Measured outcomes

Not yet measured with fixtures. Reported qualitative: reduced scope creep, fewer regressions.

## Test coverage

Manual: invoke with a feature → receive failing test stub → implement → stub passes.
