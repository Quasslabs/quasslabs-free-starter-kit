---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits into the bigger picture.
disable-model-invocation: true
---

# SKILL: zoom-out

**Bot:** any · code-navigation · exploration
**Role:** Force a higher-level summary instead of line-by-line analysis. Produces a map of modules and callers using the project's domain glossary vocabulary, so the agent stops drilling into one file when it should be reading the system.
**Ug-ug mode:** lite
**Model:** haiku — single-prompt summary, no reasoning chain
**Tool compatibility:** Claude Code · Cursor · Codex

**Origin:** Imported from [mattpocock/skills](https://github.com/mattpocock/skills) (engineering/zoom-out), MIT licensed. Source preserved at `_source_SKILL.md`.

---

## When to invoke

- Agent (or user) is stuck inside one file/module and needs the system-level view
- Onboarding into an unfamiliar codebase
- Before refactor: understand the seam before touching the implementation
- Trigger phrases: "zoom out", "give me the map", "what calls this", "higher level"

## Handoffs

| Triggered by | Next step |
|---|---|
| Map produced → user wants to refactor | `skills/developer/improve-codebase-architecture/SKILL.md` |
| Map produced → user wants to test it | `skills/developer/tdd/SKILL.md` |
| Map produced → user wants ADR | `skills/developer/arch-decision/SKILL.md` |

## Lambda candidates

None — this is a single-prompt direction skill, no functions to extract.

## Input / Output

**Input:** repo root + (optionally) a specific symbol or file you're stuck on.
**Output:** a markdown map of relevant modules + callers using the project's domain glossary vocabulary.

---

# zoom-out (source body)

I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary.
