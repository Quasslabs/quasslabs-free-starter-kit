# SKILL: reflect

**Bot:** any · end-of-session
**Role:** Terminal retrospective. Run at the end of a project, milestone, or significant flow to capture what worked, what caused friction, and what was a near-miss. Appends a dated retro to `_context/LESSONS.md`.
**Ug-ug mode:** none
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** conditional — yes across distinct projects; no for two concurrent retros appending the same LESSONS.md
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- End of project, milestone, sprint, or significant flow
- After a production incident is resolved
- User says "run a retro", "reflect on this", "capture lessons"
- Slash trigger: `/reflect`

## Steps

1. Gather context: completed tasks, blockers, incidents, files modified.
2. Produce four short sections — **What worked**, **Friction**, **Near-misses**, **Actions** (1–2 sentences each).
3. Append to `_context/LESSONS.md` under a dated `## Retro — <project> — <date>` heading.
4. Surface any item that has repeated 2+ times across sessions as a memory-promotion candidate.
5. Emit a "skill gap detected" flag for friction the existing skill set didn't prevent.

## Input

- `notes_path` — directory containing `_context/` (created if missing)
- optional `project` / `entry` to override defaults

## Output

- Appends a dated retro block to `<notes_path>/_context/LESSONS.md`
- Returns `{"path": "...", "appended": true, "date": "YYYY-MM-DD"}`

## Handoffs

- `session-handover` — run before closing the session; reflect produces lessons, handover preserves state
- `notify` — optional report of the retro summary

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `_context/LESSONS.md` (write) | Append dated retro |

## Lambda candidates

The write step is Lambda-ready once the retro content is generated; gather-context is conversation-bound and not Lambda-friendly.
