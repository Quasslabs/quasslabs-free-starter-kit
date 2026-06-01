# SETUP: ug-ug

**Skill:** `ug-ug`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. `ug-ug` is a pure in-model output-style directive;
it has no binary dependencies, no credentials, and no network calls.

## Dependencies

stdlib only — no install.

## Credentials / vault

None.

## .claude / harness wiring (optional enforcement hook)

The skill works without this, but drifts over long sessions without it.
To prevent drift, wire a `UserPromptSubmit` hook in your agent's settings that reads
`_context/ug-ug-level` and prepends a one-line directive each turn.

**`update-config` is not included in this kit** — see your agent harness docs
(Claude Code: `~/.claude/settings.json` hooks section) to wire this manually if needed.

## How to run

Say "ug-ug" (defaults to `full`) or "ug-ug <level>" (`lite`/`medium`/`full`/`extra-ug`/`maximum-ug`).
Exit with "normal mode".

## Verify it works

1. Say "ug-ug full" → assistant switches to terse internal output, normal chat replies.
2. Ask a planning question → response is bullets/symbols only, no narrative prose.
3. Say "normal mode" → full prose returns.
