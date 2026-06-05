---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
---

# SKILL: tdd

**Bot:** developer · qa-auditor · any
**Role:** Drive feature work and bug fixes via red-green-refactor TDD. Enforces vertical-slice discipline (one test → one implementation, repeat) over horizontal slicing. Tests verify behavior through public interfaces, not implementation details, so they survive refactors.
**Ug-ug mode:** lite — output structured plans + reasoning, not deep prose
**Model:** sonnet — TDD requires judgment about what to test and when to stop; haiku misses the "vertical slice" discipline and produces test-first horizontal slices
**Tool compatibility:** Claude Code · Cursor · Codex
**Status:** beta  <!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->
**Parallelizable:** yes — no shared mutable state detected (auto-inferred; verify)

**Origin:** Imported from [mattpocock/skills](https://github.com/mattpocock/skills) (engineering/tdd), MIT licensed. Source files preserved at `_source_*.md`. Companion docs (`tests.md`, `mocking.md`, `refactoring.md`, `deep-modules.md`, `interface-design.md`) copied into this folder so the SKILL.md's relative links resolve.

---

## When to invoke

- User asks: "let's TDD this", "red-green-refactor", "test-first"
- New feature with clear behavior — TDD fits well
- Bug fix — write a failing test reproducing the bug first, then fix
- Refactoring with poor existing test coverage — write characterization tests first

**Don't invoke for:**
- Exploratory spikes (TDD costs more than it saves when you don't know what you're building)
- Pure prototypes thrown away after demo
- Glue code with no logic to verify

---

## Handoffs

| Triggered by | Next step |
|---|---|
| TDD cycle complete, suite green | `skills/developer/staged-test-runner/SKILL.md` → run full suite gate |
| Feature unclear, can't write first test | `skills/developer/arch-review/SKILL.md` first |
| Coverage gaps after cycle | `skills/qa-auditor/story-test-builder/SKILL.md` |

## Lambda candidates

| Step | Lambda-safe |
|---|---|
| Test runner harness invocation | ✅ — already covered by `staged-test-runner` |
| Red-green-refactor judgement | ❌ — judgment-heavy, keep with Claude |

## Input / Output

**Input:** a feature description or bug repro · current test suite state · target language/framework.
**Output:** sequence of (failing test → passing implementation → optional refactor) cycles. Final state: green suite with new behavior verified through public interfaces.

---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

When exploring the codebase, use the project's domain glossary so that test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching.

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

## Permissions

<!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<workspace>/...` | Referenced in skill body |
