# REPORT: lifecycle/chat-primer

**Skill:** `lifecycle/chat-primer` · **Tier:** `free`
**Last measured:** 2026-05-31

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to orient at session start | 5–10 min (manually recalling state) | < 1 min | Timed |
| Missed HANDOVER context | Common | Rare | Session observation |
| Ug-ug mode drift (forgotten by session 2) | Common | Caught at start | Observation |

## Who gets the most value

Power users of Claude Code who start 3+ sessions per day across multiple projects. chat-primer is the "are we ready?" check that catches stale state before you waste tokens.

## How it fits in a flow

**Auto-triggers:** new chat on any project with CLAUDE.md → **chat-primer** → SESSION READY card → work begins

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/session-handover` | handover writes state; chat-primer reads it at next session start |
| `memory/memory-ladder` | primer hydrates memory-ladder on every session start |
| `ug-ug` | primer confirms ug-ug mode is active |

## Measured outcomes

- Session orientation time: < 1 min with primer vs. 5–10 min manually.
- Open items surfaced before work starts rather than discovered mid-session.

## Test coverage

1. Invoke in a project with CLAUDE.md + HANDOVER.md → SESSION READY card emitted with open items and next action.
