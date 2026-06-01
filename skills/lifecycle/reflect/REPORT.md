# REPORT: lifecycle/reflect

**Skill:** `lifecycle/reflect` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Lessons captured after a session | 0 (lost) | 1+ dated entries in LESSONS.md | File check |
| Time for retrospective | 15–30 min manual | 2–3 min | Timed |
| Same mistake repeated next session | Common | Rare | Self-reported |

## Who gets the most value

Anyone doing iterative development who keeps solving the same problems because the lessons don't stick session to session. reflect externalizes what you learned so the next session starts smarter.

## How it fits in a flow

**Upstream:** task completes or session ends → **reflect** → LESSONS.md updated → `session-handover` captures next state

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/session-handover` | reflect captures lessons; handover captures state — run reflect first |
| `memory/memory-ladder` | lessons feed into memory-ladder Layer 3 for cross-session recall |

## Measured outcomes

- Lessons externalized and dated: 1+ entries per session when used.
- Fewer repeated mistakes on returning sessions.

## Test coverage

1. Invoke after any completed task → `_context/LESSONS.md` has a new dated entry with the lesson.
