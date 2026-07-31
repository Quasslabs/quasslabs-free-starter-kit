# SKILL: session-handover

**Bot:** any · context-limit handover
**Role:** Generate a structured handover document when a session is running long or wrapping up. Captures completed tasks, current state, open items, key decisions, files modified, and the single most important next action. Emits a paste-ready opener for the next session.
**Ug-ug mode:** lite
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** yes
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- Approaching context limit; response quality degrading
- User says "we're running long", "save our progress", "wrap up"
- End of a multi-task sprint or significant batch
- Slash trigger: `/session-handover`

## Steps

1. Gather context: completed tasks, in-progress task, open items, files modified, key decisions.
2. Render a structured HANDOVER.md at the chosen output path.
3. Emit a 3–5 sentence "session opener" paragraph to chat for the user to paste at the start of the next session.
4. Note any uncommitted work in open items.

## Input

- `out_path` — path to write `HANDOVER.md`
- `ctx` — dict with `bot`, `project`, `completed[]`, `current_state`, `open_items[]`, `decisions[]`, `files_modified[]`, `next_action`, `session_opener`

## Output

- Writes `HANDOVER.md` at `out_path`
- Returns `{"path": "...", "written": true}`

## Handoffs

- `reflect` — run before this; reflect produces lessons, handover preserves state
- `notify` — optional alert that a session boundary occurred

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `HANDOVER.md` (write) | Render structured handover doc |

## Lambda candidates

`generate_session_opener` and the markdown render are stateless and Lambda-friendly; gather-context is conversation-bound and not Lambda-friendly.
