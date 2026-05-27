# LESSONS — improve-codebase-architecture

_(Seeded 2026-05-14 from mattpocock/skills import.)_

## Why we imported this

We have `developer/arch-review` (a gate that locks decisions before coding) and `arch-decision` (writes an ADR). We did NOT have a skill that **proactively surfaces refactoring opportunities** from an existing codebase. This skill fills that.

## Key concepts to internalize

- **Module = anything with an interface + implementation.** Not just files. Functions, classes, packages.
- **Depth = leverage at the interface.** A small interface that exposes lots of behavior = deep. A wide interface that exposes thin behavior = shallow.
- **Seam = where interfaces live.** Use this term, not "boundary."
- **Deletion test = the killer heuristic.** If you deleted the module, does complexity vanish (pass-through, kill it) or reappear in N callers (it was earning its keep)?
- **One adapter = hypothetical seam. Two adapters = real seam.** Don't extract until you have two concrete needs.

## Integration with our existing skills

- **Before**: `arch-decision` to lock ADRs the skill should not re-litigate.
- **Pairs with**: `tdd` (write characterization tests for the modules you're about to deepen).
- **After**: `developer/arch-review` to gate the proposed change before implementing.
- **Don't pair with**: this skill on greenfield code — there's nothing to deepen yet.

## Glossary discipline matters

The skill is opinionated about vocabulary. Use **Module / Interface / Implementation / Depth / Seam / Adapter / Leverage / Locality** consistently. Drifting into "component / service / API / boundary" defeats the purpose — the consistent language IS the value.

## Anti-pattern: premature abstraction

The skill explicitly warns against extracting an interface when you only have one adapter. Two concrete needs justify a seam. One concrete need + an imagined future need does not.
