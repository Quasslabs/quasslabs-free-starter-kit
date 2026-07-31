# Lessons — skill-linter

## 2026-06-11 — initial release

- Required header fields stayed at 6 (Bot, Role, Ug-ug mode, Model, Status, Parallelizable). Adding License/Origin/Pack/Commercial/Tier would have caught more leaks but breaks too many older skills — leave those to the hub linter's `--strict-commercial` mode.
- Section check matches `## When to invoke` and `## Handoffs` only. Looser than the hub linter on purpose: kit buyers care about callability, not file completeness.
- Exit code 1 on any issue. CI gates can wire this directly without parsing stdout.
