# Gumroad Listing — QuassLabs Free Starter Kit

## Listing setup

| Field | Value |
|---|---|
| Product type | Digital download |
| Price | $0 (free — set price to 0, do NOT require email unless you want lead capture) |
| File to upload | `dist/quasslabs-free-starter-kit-v1.0.0.zip` OR link to GitHub release |
| Cover image | See notes below |
| Tags | claude, ai agents, claude code, developer tools, productivity, llm, skills |
| Category | Design & Tech > Programming |

---

## Title

QuassLabs Free Starter Kit — 19 Claude Code Agent Skills

---

## Short description (shown in card preview)

Stop prompting from scratch. 19 free skills that give Claude Code memory, routing, project setup, and structured output — built from a 400+ skill private hub.

---

## Full description (paste into Gumroad's rich text editor)

---

**The problem with AI-assisted development:** every new chat, the agent forgets everything. Your project conventions, your preferences, what you fixed last week — gone. You spend the first 10 minutes re-orienting it before you can do any real work.

**This kit fixes that.**

19 MIT-licensed skills for Claude Code — small markdown files that tell the agent exactly how to do one job well, including how to remember things between sessions.

### What's inside

**Start here — take weight off day one**
- `agent-setup-wizard` — generate a `CLAUDE.md` that teaches Claude your stack. The "no documentation" fix.
- `project-env-setup` — bootstrap dev scaffolding for a new project
- `chat-primer` — a session-start ritual that wires memory and surfaces the right skills
- `repo-doc-builder` — point it at a repo → it writes the map + process docs

**Make the AI behave**
- `ug-ug` — token-efficient output: terse where it should be, prose where it matters
- `task-router` — route each sub-task to the right model before you start
- `gstack` — model-selection roles (cheap model vs smart one, when)
- `llm-selector` — pick the optimal LLM + cost estimate + fallback chain
- `ollama-task-router` — decide what runs locally (free) vs cloud

**Memory + continuity**
- `memory-ladder` — 7-layer cross-session memory pipeline
- `session-handover` — clean state capture when you hit a context limit
- `reflect` — end-of-session retrospective that writes lessons back into your skills
- `notify` — agent-to-human alerts for long-running jobs

**Build your own**
- `skill-builder` — draft new skills in the standard format
- `skill-linter` — validate a skill's structure before you rely on it

**Dev/QA taste**
- `tdd` — red-green-refactor with vertical-slice discipline
- `improve-codebase-architecture` — surface architectural friction + deletion-test heuristic
- `zoom-out` — escape-hatch when you're stuck inside one file
- `humanizer` — strip the AI tells out of generated writing

### How to use it

Drop the skill folders into `~/.claude/skills/` and invoke by name — or paste a `SKILL.md` as instructions for any task. Works with Claude Code, Cursor, Codex, or any agent that reads markdown.

Best first move: run `agent-setup-wizard` on a repo you maintain. You'll get a project-specific `CLAUDE.md` that makes every future chat smarter.

Full install instructions are in the included `INSTALL.md` — hand it to your agent and it will wire itself in.

### GitHub repo

[github.com/Quasslabs/quasslabs-free-starter-kit](https://github.com/Quasslabs/quasslabs-free-starter-kit)

### License

MIT — use commercially, modify freely.

---

*The paid packs (QA automation suite, designer toolkit, done-for-you setup) are in the works. This free kit is the foundation.*

---

## Cover image notes

Suggested: dark background, mono font, something like:

```
QuassLabs
Free Starter Kit

19 Claude Code Skills
Memory · Routing · Project Setup

MIT Licensed · Free Forever
```

Dimensions: 1280 x 720 (Gumroad recommended). Simple > busy.

---

## Post-publish checklist

- [ ] Copy Gumroad product URL
- [ ] Update `PAID-PACKAGES.md` in the repo with the Gumroad link
- [ ] Add to quasslabs.com — see WEBSITE-COPY.md (to be created)
- [ ] Share GitHub repo link with Sean Jefferies (Scripture Central)
- [ ] Update the intro email with real Gumroad URL
