# The one idea that makes AI agents actually useful

## Coloring book, not a blank room

Most people use AI like this: drop a kid in an empty room with a box of crayons and say "make me a picture." Then they're surprised when there's crayon on the wall.

A skill system is the coloring book. You hand the agent:
- **Context** — what the project is, the stack, the conventions (a `CLAUDE.md`).
- **A defined task** — one job, with steps and known gotchas (a `SKILL.md`).
- **Handoffs** — what to do next, and which skill owns it.

Same model, structured input → dramatically better, more consistent output. That's the whole game.

## Treat the AI like a sharp junior dev

It knows more than you about some things and less about others. You still admin it: you watch what it proposes, you say "no, not that, go here instead," you own the final call. The skills encode the judgment so you don't re-explain it every session.

## Which model for which job

| Job | Reach for |
|---|---|
| Programmatic / code-heavy work, long agent loops | Claude (Claude Code) |
| Creative / research / drafting / "help me think" | ChatGPT (or Codex for code-with-creativity) |
| In-editor, see-everything, hands-on | Cursor |
| Cheap classification / routing / bulk extraction | a small local model (Ollama) — free |
| Architecture calls, high-stakes trade-offs | the smartest model you have |

Don't marry one tool. Route the task to the right one — that's what `task-router`, `llm-selector`, `gstack`, and `ollama-task-router` in this kit are for.

## Structure compounds

One skill is a note. Fifty composable skills that hand off to each other is a system that builds fast and consistently — because every recurring decision is captured once and reused. Start with `task-router` on your next multi-step job and grow from there.
