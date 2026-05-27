# LESSONS — tdd

_(Seeded 2026-05-14 from mattpocock/skills import. Append corrections + tuning notes here as the skill is used in production.)_

## Why we imported this

Our existing test-related skills (`staged-test-runner`, `exhaustive-test-generator`, `qa-auditor/story-test-builder`) cover the **harness** and the **post-hoc generation** of tests but don't enforce **TDD discipline during feature work**. This skill fills that gap.

## Key insights from the source

- **Vertical slices > horizontal slices.** Writing all tests first, then all implementation, produces tests that verify imagined behavior, not real behavior. Drive one test → one implementation → repeat.
- **Test public interfaces, not implementation.** Tests that survive refactors describe what the system does, not how. If renaming an internal function breaks tests, those tests are coupled to implementation.
- **Integration-style tests beat unit tests.** Exercise real code paths through public APIs.

## Integration with our existing skills

- **Before** `tdd`: `arch-decision` to lock the seam, `zoom-out` to understand context.
- **After** `tdd`: `staged-test-runner` to run the full suite gate.
- **Don't pair with**: `exhaustive-test-generator` — that's for post-hoc spec-based generation, opposite philosophy.

## Anti-patterns to watch in our context

- Test-first on glue code (DTO mappers, config loaders) wastes cycles. Default to "write the code, then a smoke test."
- Test-first on UI components is a bake-off (react-testing-library makes it work; some component libraries don't). Confirm the harness before committing.
