# INSTALL — read this first (agent-facing)

**You are an AI coding agent (Claude Code, Cursor, Codex, etc.) and someone just handed you this repo.** Your job: integrate these skills into their existing project **without breaking anything**. Follow this exactly.

---

## 0. Ground rules

- **These skills are guidance markdown, not runnable code.** Each `skills/<name>/SKILL.md` describes how to do one job well.
- **Ignore absolute paths inside the skills** like `<workspace>/...` or `<lan-host>` — those are the author's local environment. Adapt every path/host to THIS user's setup. Never try to read the author's machine paths.
- **Do not overwrite the user's existing files or skills.** Propose a plan, get a yes, then act.
- **Don't invent secrets or infra.** Where a skill mentions a vault, AWS, Telegram, etc., use whatever the user already has, or note it as optional.

## 1. Detect the host + where skills live

| Host | Skills location |
|---|---|
| Claude Code | `~/.claude/skills/` (global) or `<project>/.claude/skills/` (project-local, preferred) |
| Cursor / Codex / other | No standard folder — reference the `SKILL.md` files directly, or copy the ones you'll use into the project's docs |

Ask the user which they use if it's unclear. Prefer **project-local** install so it's versioned with their repo.

## 2. Inventory + propose (read-only first)

1. List `skills/` in this repo (20 skills — see `README.md` for the map).
2. Look at the user's project: does it already have a `CLAUDE.md`? a `.claude/skills/` folder? any same-named skills?
3. Propose a short integration plan and **wait for confirmation**:
   - which skills to install (default: all 20; or just the foundation),
   - target location,
   - any name collisions (never clobber — skip or rename, ask the user).

## 3. Install

- Copy the chosen `skills/<name>/` folders into the target skills location (project-local `.claude/skills/` recommended).
- If the user has **no `CLAUDE.md`**: offer to run `skills/lifecycle/agent-setup-wizard/SKILL.md` — it generates a project `CLAUDE.md` + context files tuned to their stack. This is the highest-value first step.
- If the user **already has a `CLAUDE.md`**: do NOT rewrite it. Append a short section listing the newly available skills + when to use them (pull the one-liners from `README.md`). Keep their existing rules intact.

## 4. Wire the session-start ritual (optional but recommended)

Point the user at `skills/lifecycle/chat-primer/SKILL.md`: have it run at the start of new chats so the agent loads project context + surfaces the right skill for the task. If they use Claude Code, suggest adding a one-line "at session start, read chat-primer" note to their `CLAUDE.md`.

## 5. Confirm it works

- Pick one skill matched to a real task the user has right now (e.g. `repo-doc-builder` on a repo with no docs, or `task-router` before their next multi-step job) and demonstrate it end-to-end.
- Summarize what you installed, where, and what you changed in their `CLAUDE.md` (if anything).

---

## Copy-paste block for the user

Tell the user they can start a fresh chat with their agent and paste this:

```
I've added the quasslabs-free-starter-kit repo to my project. Read INSTALL.md in
it and integrate the skills into my existing setup. Don't overwrite anything I
already have — show me a plan first. My stack is: <fill in: language/framework,
where my code lives, and whether I use Claude Code / Cursor / Codex>.
```

That's it. Start at section 1.
