# quasslabs-free-starter-kit — Agent Context

21 free MIT-licensed Claude Code skills. Foundation layer for any project.

## Mandatory skill routing

**Before non-trivial work, invoke the matching skill from this kit.**

| Task | Skill | Path (repo-local) |
|---|---|---|
| New project setup (CLAUDE.md + context files) | `agent-setup-wizard` | `skills/lifecycle/agent-setup-wizard/SKILL.md` |
| Session start ritual (context + memory + ug-ug) | `chat-primer` | `skills/lifecycle/chat-primer/SKILL.md` |
| End-of-session handover doc | `session-handover` | `skills/lifecycle/session-handover/SKILL.md` |
| Post-task retrospective + lessons | `reflect` | `skills/lifecycle/reflect/SKILL.md` |
| New project bootstrap (env, Docker, config) | `project-env-setup` | `skills/lifecycle/project-env-setup/SKILL.md` |
| Cross-session memory | `memory-ladder` | `skills/memory/memory-ladder/SKILL.md` |
| Model/LLM selection | `llm-selector` | `skills/llm-selector/SKILL.md` |
| Task routing (local vs cloud) | `task-router` | `skills/task-router/SKILL.md` |
| Ollama task routing ($0 local path) | `ollama-task-router` | `skills/ollama-task-router/SKILL.md` |
| Pick the right local model for a task | `local-model-route` | `skills/local-model-route/SKILL.md` |
| Multi-perspective review panel | `gstack` | `skills/gstack/SKILL.md` |
| Build a new skill | `skill-builder` | `skills/meta/skill-builder/SKILL.md` |
| Validate a skill (lint) | `skill-linter` | `skills/meta/skill-linter/SKILL.md` |
| Alert / notification | `notify` | `skills/notify/SKILL.md` |
| Architecture improvement | `improve-codebase-architecture` | `skills/developer/improve-codebase-architecture/SKILL.md` |
| TDD workflow | `tdd` | `skills/developer/tdd/SKILL.md` |
| Codebase orientation (zoom out) | `zoom-out` | `skills/developer/zoom-out/SKILL.md` |
| Writing quality gate | `humanizer` | `skills/humanizer/SKILL.md` |
| Repo documentation | `repo-doc-builder` | `skills/repo-doc-builder/SKILL.md` |
| Free-cloud LLM proxy (failover) | `freellmapi` | `skills/integrations/freellmapi/SKILL.md` |

## Core skill kit

`CORE-SKILL-KIT.json` (repo root) is the manifest `agent-setup-wizard` reads in Phase 2.
Each core skill carries an `available` flag: skills shipped in this kit are **Included**
(pre-selected), and the remaining core skills are listed as **"Available in the full hub"**
upgrade pointers — so the wizard shows the full breadth without promising skills this free
tier doesn't ship.

## How skills work

Skills are guidance markdown, not runnable code. When you invoke a skill, read its `SKILL.md`
and follow the steps. Each skill includes:
- **When to invoke** — trigger phrases
- **Steps** — the procedure
- **Handoffs** — what skill to call next

## Installation

See `INSTALL.md` for agent-facing setup instructions.
