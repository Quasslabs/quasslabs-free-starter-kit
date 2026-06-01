# REPORT: repo-doc-builder

**Skill:** `repo-doc-builder` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to write repo map + process docs | 2–4 hours | ~15 min | Timed |
| Repos with zero docs | Most | 0 after one run | Count |
| New dev onboarding time | 1–2 days ("read the code") | Hours ("read the docs") | Self-reported |

## Who gets the most value

Solo devs and small teams who never write docs because they're always shipping. repo-doc-builder does it in one command so new contributors (or your future self after 6 months) know where things are.

## How it fits in a flow

**Upstream:** new repo or stale docs → **repo-doc-builder** → 00-how-we-work + 01-repo-map + 02-skill-lifecycle committed → agents have accurate context

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/agent-setup-wizard` | wizard generates CLAUDE.md; repo-doc-builder generates the technical docs |

## Measured outcomes

- Docs generated from zero in ~15 min per repo.
- Applied to: taylor-ql-at repos, qa-developer-skills, taylor-program-docs.

## Test coverage

1. Invoke on any GitHub repo → at least one `00-*.md` doc committed within the session.
