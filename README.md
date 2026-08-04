# Agent Skills — Free Starter Kit

A curated, free set of **agent skills** for Claude Code, Cursor, and Codex — the foundation layer from a 500+ skill private hub, given away so you can see how good a structured skill system feels.

Built by [QuassLabs](https://quasslabs.com) (Taylor Quass). If these help, the deeper specialized packs are linked at the bottom.

> **Setting up?** Hand this repo to your AI agent and have it read [`INSTALL.md`](INSTALL.md) — it walks the agent through integrating these skills into your existing project without breaking anything. Or paste the block in INSTALL.md into a fresh chat.

---

## What's a "skill"?

A skill is a small markdown file (`SKILL.md`) that tells an AI agent *how* to do one job well — the steps, the gotchas, the handoffs to other skills. Drop them in your agent's skills folder and it stops guessing.

Each skill in this kit ships with:
- `SKILL.md` — what the skill does and how to invoke it
- `FUNCTIONS.md` — pure functions (deterministic/Lambda-ready), AI-assisted steps, external services
- `SETUP.md` — deps, credentials, how to run, how to verify it works
- `REPORT.md` — measured value, flow context, skill interactions
- `LESSONS.md` — production lessons and corrections
- `INSTALL.md` + `manifest.json` — drop-in install steps and declared dependencies

> The core idea: **don't hand the AI a blank room and a box of crayons — hand it a coloring book.** A structured environment (clear context, conventions, and a defined task) gets dramatically better output than "go build me a thing." See [`PHILOSOPHY.md`](PHILOSOPHY.md).

---

## What's in here (12 skills)

### Make the AI behave
| Skill | What it does |
|---|---|
| `ug-ug` | Token-efficient output mode — terse where it should be, full prose where it matters. 5 levels (`lite` to `maximum-ug`). |
| `task-router` | Pre-flight step: routes each sub-task to the right model + flags blockers before you start. |
| `ollama-task-router` | Decide what runs locally (free, via Ollama) vs in the cloud. |
| `llm-selector` | Pick the optimal LLM for a task + a fallback chain + cost estimate. |
| `gstack` | A CEO/architect/QA/designer/security role-panel workflow — Think → Plan → Build → Review → Ship. Role/pipeline taxonomy adapted with credit from [Garry Tan's gstack](https://github.com/garrytan/gstack) (MIT). |

### Memory + continuity (for solo devs juggling many chats)
| Skill | What it does |
|---|---|
| `memory-ladder` | Cross-session memory (layered, file-based) so the agent stops forgetting between chats. |
| `session-handover` | Capture a session's state into a clean handover when you hit a context limit. |
| `reflect` | End-of-session retrospective → writes lessons back into your skills. |
| `notify` | Simple agent → human alerts (e.g. Telegram) for long-running jobs. |

### Build + orchestrate
| Skill | What it does |
|---|---|
| `skill-builder` | Draft new skills in the house format, with a prior-art check baked in. |
| `skill-linter` | Validate a skill's structure before you rely on it. |
| `operator` | Orchestrator entry point — routes a request to the right skill. |

---

## How to use them

**Claude Code:** drop a skill folder into `~/.claude/skills/` (or your project's `.claude/skills/`) and invoke it by name, or just point Claude at the `SKILL.md`.

**Cursor / Codex:** every skill except `gstack` is designed to work the same way here — open the `SKILL.md` and reference it as instructions for the task. `gstack`'s role-panel workflow currently assumes Claude Code's slash-command + hook infrastructure, so it's Claude Code-only for now.

Best first move: run `task-router` before a multi-step build, or `memory-ladder` if you're juggling several long-running chats on the same project.

---

## More skills that would help you — but we can't redistribute

A lot of genuinely great work is under licenses (or no license) that mean we can't bundle it. See [`OTHER-REPOS.md`](OTHER-REPOS.md) for a hand-picked list pointing straight at the source — including the projects some of these skills build on.

---

## Credits

These skills stand on other people's shoulders where noted. Upstream origins are credited in [`CREDITS.md`](CREDITS.md) — most notably `gstack`, which adapts its role/pipeline taxonomy from [Garry Tan's gstack](https://github.com/garrytan/gstack) (MIT).

---

## Paid packages

This free kit is the foundation. [Freelancer Finance](https://quassian.gumroad.com/l/freelancer-finance) and [Web Design Kit](https://quassian.gumroad.com/l/web-design-kit) are live now; more specialized packs + a "set up your agent toolkit for you" engagement are listed in [`PAID-PACKAGES.md`](PAID-PACKAGES.md).

## License

**MIT** — use it freely, including commercially. Licensed permissively to maximize adoption. See [`LICENSE.md`](LICENSE.md). The `gstack` skill retains upstream attribution (see CREDITS). If it helps, the specialized packs + done-for-you setup are how we keep the lights on.
