---
name: session-handover
description: >
  Auto-MindPalace at context limit. Detects when a session is running long, writes a structured handover block capturing current task state, open items, key decisions made, files modified, and the single most important next action. Produces a handover that can be pasted at the start of a new session to resume without loss of context. Use when approaching context limit, wrapping up a long session, or at the end of a multi-task sprint.
---

# SKILL: session-handover

**Bot:** any  
**Role:** Auto-MindPalace at context limit. Detects when a session is running long, writes a structured handover block capturing: current task state, open items, key decisions made, files modified, and the single most important next action. Produces a handover that can be pasted at the start of a new session to resume without loss of context. No LLM needed — reads current conversation/task state.  
**Ug-ug mode:** lite  
**Model:** haiku — pure file I/O and markdown templating; no reasoning or generation required
**Tool compatibility:** Codex · Claude Code · Cursor · Cowork
**Status:** beta  <!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->
**Parallelizable:** yes — no shared mutable state detected (auto-inferred; verify)

---

## Model

**Verdict:** `phi4-mini` — structured handover write is deterministic markdown templating; no generation needed.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Deterministic markdown template fill; no generation |
| Local (installed) | phi4-mini | Template rendering within local capability |
| Local (ideal) | phi4-mini | Already installed; ideal for structured writes |

---

## When to invoke

- When approaching context limit (Claude warns or response quality degrades)
- "We're running long — write a handover"
- "Summarize where we are so I can start a new session"
- "Save our progress"
- At natural stopping points in multi-session work
- After completing a major batch of tasks (e.g., end of a skill-build sprint)
- Automatically: after the `reflect` skill's Phase 4 if context > ~60k tokens
- **Note — abrupt session end:** the `stop-hook` skill (`skills/memory/stop-hook/SKILL.md`) fires automatically on every Claude Code session close (including abrupt/crash). It stamps a flush timestamp to MEMORY.md and calls compress_for_ollama.py. For graceful ends with full handover content, invoke this skill manually BEFORE closing the session so the handover block is available to paste into the next session.

---

## What a handover captures

```
SESSION HANDOVER — [date/time]
Bot: [bot name]
Project: [project path]

━━━ COMPLETED THIS SESSION ━━━
[bulleted list of tasks finished — one line each]

━━━ CURRENT STATE ━━━
[what was in progress when session ended]
[exact file being edited, function/section being worked on]

━━━ OPEN ITEMS (pick these up next) ━━━
Priority 1: [most important thing]
Priority 2: [next]
...

━━━ KEY DECISIONS MADE ━━━
[decisions that future self needs to know — with reasoning]

━━━ FILES MODIFIED ━━━
[list of files touched this session with one-line summary of change]

━━━ NEXT ACTION ━━━
[single, specific, executable first step for the new session]
[e.g.: "Run skill-linter --all, then update CLAUDE.md with the 3 new skills from wip/"]

━━━ CONTEXT TO PASTE AT SESSION START ━━━
[paste-ready paragraph for the new session opener]
```

---

## Phase 0 — Relay scan (auto, ~10s)

Before gathering handover context, scan for cross-session items to dispatch.

**Run automatically — no user prompt needed.**

1. Collect files modified this session (from tool history / git status)
2. Map each file path → owning bot domain using `session-relay` bot registry
3. Identify relay-worthy items:
   - Changed shared files (`_lib_*.py`, `REGISTRY.md`, `CAPABILITY-MAP.md`) → note to affected bots
   - New skill triads created → note to bots in that domain
   - Lessons learned about a tool another bot uses → yellow note to that bot
   - Explicit deferred items for a specific bot → red todo to that bot
4. For each candidate: call `relay(to_bot, subject, content, priority)`
5. If ≥1 relayed: print brief RELAY block to chat (see session-relay SKILL.md)
6. If 0 candidates: silent

**Skill:** `skills/session-relay/SKILL.md`

---

## Phase 1 — Gather context

Pull from available sources:

```
Source                      What to extract
──────────────────────────────────────────────────────
TodoList / TaskList tool    completed ✅, in_progress 🔄, pending ⏳
Conversation history        last few user messages + agent responses
Git status (if available)   modified files, uncommitted changes
LESSONS.md (if exists)      any lessons written this session
HANDOVER.md (if exists)     read existing, then update
```

```bash
# Git state snapshot (run if available)
git status --short
git diff --stat HEAD
```

---

## Phase 2 — Write the handover

Write to two places:

### 1. `HANDOVER.md` in the project root

```python
# write_handover.py

from pathlib import Path
from datetime import datetime, timezone

def write_handover(project_root: str, handover: dict):
    """Write structured handover to HANDOVER.md."""
    path = Path(project_root) / "HANDOVER.md"
    now  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Session Handover — {now}",
        f"**Bot:** {handover.get('bot', 'unknown')}",
        f"**Project:** {project_root}",
        "",
        "## Completed This Session",
        *[f"- {item}" for item in handover.get("completed", ["(none recorded)"])],
        "",
        "## Current State",
        handover.get("current_state", "(not recorded)"),
        "",
        "## Open Items",
        *[f"{i+1}. {item}" for i, item in enumerate(handover.get("open_items", []))],
        "",
        "## Key Decisions",
        *[f"- **{d['decision']}** — {d['reason']}" for d in handover.get("decisions", [])],
        "",
        "## Files Modified",
        *[f"- `{f['path']}` — {f['change']}" for f in handover.get("files_modified", [])],
        "",
        "## Next Action",
        f"> {handover.get('next_action', '(define before closing session)')}",
        "",
        "---",
        "## Session Opener (paste at start of next session)",
        "",
        f"```",
        handover.get("session_opener", "(generate from above)"),
        "```",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Handover written to: {path}")
```

### 2. A paste-ready block printed to chat

The agent prints the `━━━ CONTEXT TO PASTE AT SESSION START ━━━` block directly in the conversation so the user can copy it immediately.

---

## Phase 3 — Generate the session opener

The session opener is a 3–5 sentence paragraph the user pastes at the top of the next session to prime the new context window. It should:

- State what bot/project this is
- Summarize what was accomplished
- State the single most important open item
- Tell the agent what the first action should be

**Template:**
```
Continuing [bot name] session for [project]. Last session completed:
[2-3 key items]. Currently working on [task]. The most important open
item is [priority 1]. Start by [next action].
```

**Example:**
```
Continuing Skillmaster session for the skills hub. Last session built:
estimate-billing-report, skill-linter, claude-md-sync, coverage-checker,
session-handover. Currently in yellow skill builds — 4 of 10 done.
The most important open item is adding all new skills to CLAUDE.md inventory
and then building fathom-fetcher/lambda. Start by running claude-md-sync
to get the current inventory drift count.
```

---

## Phase 4 — Close out

```
[ ] Phase 0 relay scan run — cross-session items dispatched to INBOX.md files
[ ] HANDOVER.md written to project root
[ ] Session opener pasted in chat for user to copy
[ ] Any uncommitted work noted in open items
[ ] LESSONS.md updated if reflect skill was run
[ ] TodoList tasks marked completed/pending as appropriate
```

---

## Trigger heuristics (for automatic invocation)

Invoke proactively when ANY of these are true:
- User says "this is getting long" / "we should wrap up" / "let's pick this up later"
- Task list has >5 completed items and >3 pending items (substantial session)
- Agent has been working for >40 tool calls
- User explicitly asks for a summary or save point
- Context window warnings appear

---

## Input spec

```
trigger:       "context limit" | "user request" | "post-reflect" | "end of sprint"
task_list:     current TaskList state (completed + pending)
files_touched: list of files modified this session (from tool history)
decisions:     key choices made (optional - Claude synthesizes from context if not supplied)
```

---

## Output spec

```
Writes to:  HANDOVER.md (project root or skills/HANDOVER.md)
Also emits: chat paste block (--- SESSION OPENER --- format)

Structure:
  ## Handover - [date]
  ### Completed this session
  ### Open items
  ### Key decisions
  ##
## Memory

**Recommended:** memory-ladder Layer 4 — handover state must persist across sessions

## Handoffs

- **→ memory-ladder** to restore session state at the start of the next context window
- **→ operator** in the new session to re-route based on the handover's "next action"
- **→ notify** to alert a human that a session boundary has occurred and handover is ready

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `gather_context` | Phase 1 — read task list, conversation history, git status, LESSONS.md | no | ❌ |
| `write_handover_md` | Phase 2 — render structured HANDOVER.md and write to project root | no | ❌ |
| `generate_session_opener` | Phase 3 — synthesize 3–5 sentence paste-ready context block | yes | ✅ |
| `emit_chat_paste_block` | Phase 2 — print SESSION OPENER block to chat for user to copy | yes | ✅ |
| `check_trigger_heuristics` | Inline — evaluate context size, tool call count, task counts to auto-invoke | yes | ✅ |

None. This skill is conversation-context-dependent and local-filesystem-bound — not a Lambda candidate. `gather_context` requires reading live conversation state and local git status; `write_handover_md` writes to a project-root path on the local machine. `generate_session_opener` and `emit_chat_paste_block` are stateless text operations that could be extracted to Lambda but provide no value outside the session context where they run.

## Permissions

<!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->

| Type | Pattern | Why |
|---|---|---|
| Bash | `git *` | Referenced in skill body |
| Filesystem | `<workspace>/...` | Referenced in skill body |
