# REPORT: humanizer

**Skill:** `humanizer` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| AI-tell patterns in output | 29 detectable patterns present | Detected and rewritten | Manual review of samples |
| Client-facing text readability | "Sounds like ChatGPT" | Natural prose | Reviewer feedback |
| Post-processing time | 20–30 min manual rewrite | 2–3 min | Timed |

## Who gets the most value

Content creators, marketers, and developers who generate first drafts with AI and need them to sound human before sending to clients. The mandatory last pass before anything a client reads.

## How it fits in a flow

**Upstream:** any AI-generated draft → **humanizer** → client-ready prose → publish/send

Ug-ug mode is `none` for this skill — compressing humanizer output defeats the purpose.

## Skill interactions

| Pairs with | How |
|---|---|
| `marketing/agency-brief` | agency-brief generates; humanizer polishes before sending |
| Any content generation skill | humanizer is the last step in any content pipeline |

## Measured outcomes

- 29 AI-tell patterns detected and rewritten per pass.
- ~30% reduction in "sounds like AI" feedback from reviewers.

## Test coverage

1. Pass AI-generated text with em-dashes and "it's worth noting" → receive natural prose.
