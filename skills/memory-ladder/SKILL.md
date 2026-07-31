# SKILL: memory-ladder

**Bot:** any · cross-session memory
**Role:** File-based cross-session memory layer (Layer 4+). Loads, saves, and appends to per-slug JSON memory files so agents can resume context after a session ends.
**Ug-ug mode:** lite
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** no
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- User says "remember this", "long session", "cross-project context", "compress memory"
- Starting a new chat that needs prior-session state
- Before a context-limit handover
- Slash trigger: `/memory-ladder`

## Layers

| Layer | What lives there |
|---|---|
| 1 — identity anchor | project name, stack, current goal |
| 2 — micro-compaction | drop pleasantries, keep decisions |
| 3 — narrative summary | one paragraph per work block |
| 4 — structural state | 9-point: goal/stack/done/in-progress/blocked/decisions/constraints/next/files |
| 5 — durable facts | confirmed choices, hard constraints, fixed paths |
| 6 — promotion | recurring patterns become rules |
| 7 — handoff block | structured paste-block for next session |

## Steps

1. Resolve memory path: `~/.memory/<slug>.json`.
2. `load(slug)` returns existing payload or empty dict.
3. `save(slug, payload)` writes JSON atomically.
4. `append(slug, entry)` appends to the `entries` list inside the payload.
5. Caller composes layer content; this skill is the storage primitive.

## Input

| Field | Type | Required |
|---|---|---|
| `slug` | string | yes |
| `payload` | dict | save only |
| `entry` | any | append only |

## Output

- `load`: dict payload (empty dict if no file)
- `save`: path written
- `append`: updated entries length

## Handoffs

- `session-handover` — Layer 7 paste-block composition
- `task-router` — pre-flight evaluator before a long session

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `~/.memory/*.json` | Per-slug memory files |

## Lambda candidates

None — file-based local storage.

## Value

Removes session-amnesia rework. A new chat that loads prior structural state skips re-asking settled questions; tests verify save/load/append round-trip is lossless.
