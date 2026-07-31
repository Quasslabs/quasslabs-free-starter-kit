# SKILL: operator

**Bot:** operator · orchestrator
**Role:** Orchestrator entry point. Routes a task description to the right skill slug from a small allowlist.
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
- User says "route this", "what skill do I need", "orchestrate"
- Slash trigger: `/operator`
- First step of any multi-skill workflow

## Steps

1. Read the task description.
2. Match keywords against the routing allowlist.
3. Return a dict `{skill, reason}`.
4. Hand off to the named skill, or report "no match" so the caller can fall back to manual selection.

## Input

- `task` — free-text task description

## Output

- `{skill, reason}` dict, or `{skill: null, reason: ...}` when no match

## Handoffs

- `skill-builder` — when the task has no matching skill, draft a new one
- `skill-linter` — when the task involves validating an existing SKILL.md
- `ug-ug` — when the task is "compress this output"

## Permissions

None.

## Lambda candidates

`route(task)` — pure function over a small allowlist; ideal Lambda candidate for an API-Gateway-fronted router.
