# quasslabs-free-starter-kit — Agent Context

12 free MIT-licensed skills for Claude Code, Cursor, and Codex. Foundation layer for any project.

## Mandatory skill routing

**Before non-trivial work, invoke the matching skill from this kit.**

| Task | Skill | Path (repo-local) |
|---|---|---|
| Token-efficient output mode | `ug-ug` | `skills/ug-ug/SKILL.md` |
| Task routing (local vs cloud, red gates) | `task-router` | `skills/task-router/SKILL.md` |
| Ollama task routing ($0 local path) | `ollama-task-router` | `skills/ollama-task-router/SKILL.md` |
| Model/LLM selection | `llm-selector` | `skills/llm-selector/SKILL.md` |
| Multi-role review panel (CEO/architect/QA/design/security) | `gstack` | `skills/gstack/SKILL.md` |
| Cross-session memory | `memory-ladder` | `skills/memory-ladder/SKILL.md` |
| End-of-session handover doc | `session-handover` | `skills/session-handover/SKILL.md` |
| Post-task retrospective + lessons | `reflect` | `skills/reflect/SKILL.md` |
| Alert / notification (agent to human) | `notify` | `skills/notify/SKILL.md` |
| Build a new skill | `skill-builder` | `skills/skill-builder/SKILL.md` |
| Validate a skill (lint) | `skill-linter` | `skills/skill-linter/SKILL.md` |
| Route a request to the right skill | `operator` | `skills/operator/SKILL.md` |

## How skills work

Skills are guidance markdown, not runnable code. When you invoke a skill, read its `SKILL.md`
and follow the steps. Each skill includes:
- **When to invoke** — trigger phrases
- **Steps** — the procedure
- **Handoffs** — what skill to call next

## Installation

See `INSTALL.md` for agent-facing setup instructions.
