# Agent Skills — Free Starter Kit

A curated, free set of **agent skills** for Claude Code, Cursor, and Codex — the foundation layer from a 400+ skill private hub, given away so you can see how good a structured skill system feels.

Built by [QuassLabs](https://quasslabs.com) (Taylor Quass). If these help, the deeper specialized packs are linked at the bottom.

> **Setting up?** Hand this repo to your AI agent and have it read [`INSTALL.md`](INSTALL.md) — it walks the agent through integrating these skills into your existing project without breaking anything. Or paste the block in INSTALL.md into a fresh chat.

---

## What's a "skill"?

A skill is a small markdown file (`SKILL.md`) that tells an AI agent *how* to do one job well — the steps, the gotchas, the handoffs to other skills. Drop them in your agent's skills folder and it stops guessing.

> The core idea: **don't hand the AI a blank room and a box of crayons — hand it a coloring book.** A structured environment (clear context, conventions, and a defined task) gets dramatically better output than "go build me a thing." See [`PHILOSOPHY.md`](PHILOSOPHY.md).

---

## What's in here (19 skills)

### Start here — take weight off day one
| Skill | What it does |
|---|---|
| `lifecycle/agent-setup-wizard` | Onboard a new project: generates a `CLAUDE.md` + context files so the agent knows your stack. The "no documentation" fix. |
| `lifecycle/project-env-setup` | Bootstraps local dev scaffolding for a new project. |
| `lifecycle/chat-primer` | A "session ready" ritual every new chat runs — wires memory + surfaces the right skills for your task. |
| `repo-doc-builder` | Point it at a repo → it writes the repo map + process docs for you. |

### Make the AI behave
| Skill | What it does |
|---|---|
| `ug-ug` | Token-efficient output mode — terse where it should be, prose where it matters. |
| `task-router` | Pre-flight step: routes each sub-task to the right model + flags blockers before you start. |
| `gstack` | Model-selection roles (when to use a cheap model vs a smart one). |
| `llm-selector` | Pick the optimal LLM for a task + a fallback chain + cost estimate. |
| `ollama-task-router` | Decide what runs locally (free) vs in the cloud. |

### Memory + continuity (for solo devs juggling many chats)
| Skill | What it does |
|---|---|
| `memory/memory-ladder` | Cross-session memory (7-layer pipeline) so the agent stops forgetting between chats. |
| `lifecycle/session-handover` | Capture a session's state into a clean handover when you hit a context limit. |
| `lifecycle/reflect` | End-of-session retrospective → writes lessons back into your skills. |
| `notify` | Simple agent → human alerts (e.g. Telegram) for long-running jobs. |

### Build your own (when you're ready)
| Skill | What it does |
|---|---|
| `meta/skill-builder` | Draft new skills in the house format. |
| `meta/skill-linter` | Validate a skill's structure before you rely on it. |

### A taste of the dev/QA packs (MIT-licensed)
| Skill | What it does |
|---|---|
| `developer/tdd` | Red-green-refactor with vertical-slice discipline. |
| `developer/improve-codebase-architecture` | Surface architectural friction + a deletion-test heuristic. |
| `developer/zoom-out` | Escape-hatch when you're stuck inside one file — produces a module map. |
| `humanizer` | Strip the AI tells out of generated writing. |

---

## How to use them

**Claude Code:** drop a skill folder into `~/.claude/skills/` (or your project's `.claude/skills/`) and invoke it by name, or just point Claude at the `SKILL.md`.

**Cursor / Codex / other agents:** open the `SKILL.md` and paste or reference it as instructions for the task. The skills are plain markdown — readable by any agent or human.

Best first move: run `lifecycle/agent-setup-wizard` on a repo you maintain. You'll get a `CLAUDE.md` that makes every future chat smarter.

---

## More skills that would help you — but we can't redistribute

A lot of genuinely great work is under licenses (or no license) that mean we can't bundle it. See [`OTHER-REPOS.md`](OTHER-REPOS.md) for a hand-picked list pointing straight at the source — including the projects several of these skills build on.

---

## Credits

These skills stand on other people's shoulders. Upstream origins are credited in [`CREDITS.md`](CREDITS.md) (e.g. `ug-ug` builds on JuliusBrussee/caveman + rtk-ai/rtk; the `tdd`/`zoom-out`/`improve-codebase-architecture` family on mattpocock/skills; `humanizer` on hardikpandya/stop-slop).

---

## Paid packages (coming soon)

This free kit is the foundation. The specialized, productized packs + done-for-you setup are listed in [`PAID-PACKAGES.md`](PAID-PACKAGES.md) — QA automation suite, designer toolkit, and a "set up your agent toolkit for you" engagement. Coming to Gumroad.

## License

**MIT** — use it freely, including commercially. Licensed permissively to maximize adoption. See [`LICENSE.md`](LICENSE.md). MIT-origin skills retain their upstream copyright notices (see CREDITS). If it helps, the specialized packs + done-for-you setup are how we keep the lights on.
