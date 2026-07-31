# Install: gstack

> Apply gstack AI engineering roles (CEO, architect, QA, designer, security) in a Think->Plan->Build->Review->Ship workflow. Invoke per-role or full pipeline.

## 1. Copy skill folder

```bash
cp -r skills/gstack/ your-project/.skills/gstack/
# or
cp -r skills/gstack/ "$HUB_ROOT/gstack/"
```

## 2. CLAUDE.md entry

Add to your project's `CLAUDE.md`:

```
Skill: /office-hours
```

This skill activates with `/office-hours` — type it in any Claude Code session.

## 3. Prerequisites

stdlib only — no install.

## 4. Environment variables

None.

## 5. Verify

Invoke with a task description → receives a routing card with role assignment + model pick.
