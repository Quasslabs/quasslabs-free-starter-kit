---
name: improve-codebase-architecture
description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable.
---

# SKILL: improve-codebase-architecture

**Bot:** developer · operator · any
**Role:** Surface architectural friction in a codebase and propose **deepening opportunities** — refactors that turn shallow modules into deep ones (high leverage at a small interface). Uses a strict glossary (Module / Interface / Implementation / Depth / Seam / Adapter / Leverage / Locality) — consistent language is the point. Informed by `CONTEXT.md` + `docs/adr/`.
**Ug-ug mode:** lite — output structured findings, not prose
**Model:** sonnet — judgment-heavy: identifying genuine depth opportunities vs. premature abstraction
**Tool compatibility:** Claude Code · Cursor · Codex
**Status:** beta  <!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->
**Parallelizable:** yes — no shared mutable state detected (auto-inferred; verify)

**Origin:** Imported from [mattpocock/skills](https://github.com/mattpocock/skills) (engineering/improve-codebase-architecture), MIT licensed. Source files preserved at `_source_*.md`. Companion docs (`DEEPENING.md`, `INTERFACE-DESIGN.md`, `LANGUAGE.md`) copied into this folder so the SKILL.md's relative links resolve.

---

## When to invoke

- User asks: "improve architecture", "find refactoring opportunities", "consolidate this", "make this more testable"
- Onboarding: producing the first architectural map for a codebase
- Pre-feature: identifying seams a new feature needs before writing it
- Periodic: scheduled architecture review (quarterly per project)

**Don't invoke for:**
- Single-file edits — too zoomed in
- Codebases without a CONTEXT.md or ADRs — the skill leans on them; run `arch-decision` first
- Greenfield projects with no code yet

---

## Handoffs

| Triggered by | Next step |
|---|---|
| Deepening proposal accepted | `skills/developer/arch-review/SKILL.md` to lock decisions, then implementation |
| Missing ADRs or CONTEXT.md | `skills/developer/arch-decision/SKILL.md` first |
| Need higher-level map before deep-diving | `skills/developer/zoom-out/SKILL.md` |
| Refactor needs test coverage first | `skills/developer/tdd/SKILL.md` to write characterization tests |

## Lambda candidates

| Function | Lambda-safe |
|---|---|
| Module-count + line-count metrics scan | ✅ — pure file walk + AST parse |
| Deletion-test simulation (find callers, estimate complexity reappearance) | ⚠️ — tree-sitter based, possible on Lambda with the right layer |
| Deepening proposal generation | ❌ — judgment-heavy |

## Input / Output

**Input:** repo root with `CONTEXT.md` (domain glossary) + `docs/adr/` (decisions). Optionally a specific module or area to focus on.
**Output:** list of deepening proposals, each with: shallow-module identified, deletion-test reasoning, suggested seam, adapter count today vs. needed, proposed interface, callers affected, ADR reference.

---

# Improve Codebase Architecture (source body)

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary." Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Module** — anything with an interface and an implementation (function, class, package, slice).
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place. (Use this, not "boundary.")
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs, knowledge concentrated in one place.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate.

## Process

### 1. Explore

Read the project's domain glossary and any ADRs in the area you're touching first.

Then use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates

Present a numbered list of deepening opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and also in how tests would improve

**Use CONTEXT.md vocabulary for the domain, and [LANGUAGE.md](LANGUAGE.md) vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly (e.g. _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

Do NOT propose interfaces yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs` (see [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md)). Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones. See [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md).
- **Want to explore alternative interfaces for the deepened module?** See [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md).

## Permissions

<!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<workspace>/...` | Referenced in skill body |
