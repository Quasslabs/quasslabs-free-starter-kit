# SETUP: meta/skill-linter

**Skill:** `meta/skill-linter`
**Setup tier:** none
**Last verified:** 2026-05-31

Pure Python script (`lint_skill.py`). No install needed beyond Python 3.8+.

## Dependencies

| Dep | Install | Notes |
|---|---|---|
| Python | 3.8+ | stdlib only — no third-party packages |

## Credentials / vault

None.

## How to run

```bash
# Single file
python skills/meta/skill-linter/lint_skill.py skills/ug-ug/SKILL.md --root skills/

# All skills in your skills/ folder
python skills/meta/skill-linter/lint_skill.py --all --root skills/
```

## Verify it works

1. `python skills/meta/skill-linter/lint_skill.py skills/ug-ug/SKILL.md --root skills/` → exit 0
2. Output shows `[PASS]` or `[WARN]` lines per skill, no `[ERR]`.
