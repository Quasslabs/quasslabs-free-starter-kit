# REPORT: lifecycle/agent-setup-wizard

**Skill:** `lifecycle/agent-setup-wizard` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to onboard a new project | 2+ hours | ~30 min | User timing |
| Manual config steps | 50+ | ~10 | Step count comparison |
| Agent "what's the stack?" errors | Common | Rare | Session observation |

## Who gets the most value

Anyone starting a new project with Claude Code or another agent. Without a CLAUDE.md the agent guesses — with one it knows your stack, conventions, and which skills to use.

## How it fits in a flow

**Upstream:** new project started → **agent-setup-wizard** → CLAUDE.md + AGENTS.md + .cursorrules created → `chat-primer` auto-triggers on first session

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/project-env-setup` | wizard runs first; env-setup generates the local Docker stack |
| `lifecycle/chat-primer` | primer reads the CLAUDE.md that wizard created |

## Measured outcomes

- Setup time from scratch to working agent context: ~30 min vs. 2+ hours.
- Agents make fewer wrong assumptions about tech stack.

## Test coverage

1. Invoke in a new empty directory → CLAUDE.md + AGENTS.md created within the session.
