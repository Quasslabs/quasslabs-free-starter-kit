# SETUP: meta/skill-linter

**Skill:** `meta/skill-linter`
**Setup tier:** none
**Last verified:** 2026-05-31 on Windows / Python 3.14

skill-linter is a pure Python script (`lint_skill.py`). No install needed beyond Python.

## Dependencies

| Dep | Version | Install | Notes |
|---|---|---|---|
| Python | 3.8+ | present | stdlib only; no third-party packages |

## Credentials / vault

None.

## How to run

```bash
# Single file
python "skills/meta/skill-linter/lint_skill.py" "<path-to-SKILL.md>" --root "skills/wip"

# All skills
python "skills/meta/skill-linter/lint_skill.py" --all --root "skills/wip"

# Strict commercial (pack-inclusion gate)
python "skills/meta/skill-linter/lint_skill.py" "<path>" --root "skills/wip" --strict-commercial
```

## Verify it works

1. `python "skills/meta/skill-linter/lint_skill.py" "skills/ug-ug/SKILL.md" --root "skills/wip"` → exit 0
2. Output shows `[PASS]` or `[WARN]` (no `[ERR]`).
