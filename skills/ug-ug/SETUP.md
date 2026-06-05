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
To install the enforcement hook that re-injects the active ug-ug level each turn:

```
Invoke skill: skills/update-config/SKILL.md
```

The hook reads `_context/ug-ug-level` and prepends a one-line directive to each `UserPromptSubmit`.
See `update-config/SKILL.md` for settings.json hook registration.

## Scheduled task / daemon

None.

## How to run

Say "ug-ug" (defaults to `full`) or "ug-ug <level>" (`lite`/`medium`/`full`/`extra-ug`/`maximum-ug`).
Exit with "normal mode".

## Verify it works

1. Say "ug-ug full" → assistant switches to terse internal output, normal chat replies.
2. Ask a planning question → response is bullets/symbols only, no narrative prose.
3. Say "normal mode" → full prose returns.
