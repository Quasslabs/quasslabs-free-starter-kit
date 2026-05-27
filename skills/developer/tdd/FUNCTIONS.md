# FUNCTIONS — tdd

## Pure functions (Lambda candidates)

| Function | Input | Output | Notes |
|---|---|---|---|
| `parse_test_failures(stdout)` | test-runner stdout | list[{suite, name, message, file, line}] | Already covered by `staged-test-runner`; reuse |
| `detect_horizontal_slicing(diff)` | git diff | bool + reasons | Heuristic: many test files added without matching impl files = warn |

## AI-assisted steps

| Step | Model | Reason | Tokens |
|---|---|---|---|
| Decide what test to write next | sonnet | Vertical-slice judgment | ~1k in / ~500 out |
| Red→Green→Refactor narration | sonnet | Reasoning across cycles | ~2k in / ~1k out per cycle |
| Mocking decision (real vs fake) | sonnet | See `mocking.md` heuristics | ~500 in / ~200 out |

## External services

None — this is a workflow skill, not an integration skill.

## Companion files

- `tests.md` — example test shapes by category
- `mocking.md` — when to mock, when to use the real thing
- `refactoring.md` — refactoring during the Refactor step
- `deep-modules.md` — TDD's interaction with deep-module design
- `interface-design.md` — interface-first thinking
