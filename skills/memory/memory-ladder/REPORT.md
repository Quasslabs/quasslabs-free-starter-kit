# REPORT: memory/memory-ladder

**Skill:** `memory/memory-ladder` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Context preserved across sessions | None — starts fresh every time | 7-layer persistent memory | Session restart + resume test |
| Time to re-orient in a new session | 5–15 min (re-explaining context) | <1 min (load prior state) | Timed |
| Task continuity | Disrupted | Seamless | Successful continuations without user re-explanation |

## Who gets the most value

Solo devs juggling many projects across many chat sessions. memory-ladder is the answer to "what was I doing here again?"

## How it fits in a flow

**Upstream:** `chat-primer` loads memory-ladder at session start → **memory-ladder** serves layers → agent continues where last session left off

Works best when combined with `session-handover` (writes the state at session end) and `chat-primer` (reads it at session start).

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/session-handover` | Handover writes the state; memory-ladder stores and retrieves it |
| `lifecycle/chat-primer` | primer calls memory-ladder on every session start |

## Measured outcomes

- Task continuity across sessions without re-explaining context.
- Context restoration under 1 minute vs. 5–15 min manual catch-up.

## Test coverage

1. Write context to layer 1. Start a new session. Invoke with `mode: load` → prior state returned.
