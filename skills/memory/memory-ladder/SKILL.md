---
name: memory-ladder
description: Cross-session memory layer to prevent context overflow. Triggers - "remember this", "long session", "cross-project context", "compress memory". 7-layer architecture.
---

# SKILL: memory-ladder

**Bot:** any
**Role:** Cross-session memory layer — 7-layer architecture for context preservation across chats; primary Layer 4+ memory system
**Ug-ug mode:** lite
**Model:** phi4-mini — deterministic structured-memory write/compaction
**Tool compatibility:** Claude Code · Cursor · Codex
**Status:** beta
**Parallelizable:** no — single project memory file per slug; concurrent writers can corrupt MEMORY.md / HANDOVER.md

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `~/.claude/projects/<slug>/memory/MEMORY.md` | Per-project memory index |
| Filesystem | `<project_root>\HANDOVER.md` | Per-project session handover |
| Filesystem | `<project_root>\_context\memory-config.yaml` | Memory tier config |
| Network | `http://localhost:11434/api/generate` | Local Ollama (phi4-mini) for compaction |

## Model

**Verdict:** `phi4-mini` — structured memory write (compaction, extraction, handoff formatting) is deterministic with fixed templates; no generation needed.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Deterministic extraction and formatting across 7 layers |
| Local (installed) | phi4-mini | Layer 1-5 compaction is template-driven |
| Local (ideal) | phi4-mini | Structured write pattern fits phi4-mini |

# memory-ladder -- AI Agent Memory Management

MindPalace is a 7-layer memory pipeline for maintaining coherent context across long agent
sessions. Apply these layers in order when context is growing unwieldy or when starting a
new session that needs to inherit state from a previous one.

Source: https://github.com/whiterabb17/mindpalace

---

## Companion layer — claude-subconscious

Always activate alongside memory-ladder. It runs passively in the background; memory-ladder handles intentional writes.

**Session start:** load both `MEMORY.md` and `subconscious.md` (if exists) for the project slug. Inject subconscious observations as low-weight context.

**Session end:** before writing the Layer 6/7 handoff, call `drain_subconscious()` — high-signal observations from `subconscious.md` promote into formal `MEMORY.md` entries. Medium-signal stays in `subconscious.md` for next session.

Skill: `skills/agent-llm/claude-subconscious/SKILL.md`

---

## When to invoke

- "Context is getting long"
- "Compress the conversation"
- "I'm starting a new session -- load context"
- "Summarize what we know so far"
- "The context window is filling up"
- "Carry this forward to the next chat"
- Before handing off work to a sub-agent

---

## What this skill produces

- A compressed, structured memory snapshot ready to paste into a new session
- Preserved technical facts with reduced token footprint
- A clear handoff document when switching sessions or agents

---

## The 7-layer pipeline

Apply layers in sequence. Stop at the layer that solves the problem -- do not run all
layers if the earlier ones are sufficient.

### Layer 1 -- Identity anchor + bulk offload

Before compressing anything, write an identity anchor:
```
Project: [name]
Stack: [tech]
Current goal: [one sentence]
Session started: [date]
Key files: [list]
```

Then identify any large blobs in context (long code blocks, full file contents, raw logs)
and flag them for offloading. Reference them by filename rather than content:
- Bad: [300 lines of Python pasted inline]
- Good: "See: build_static_screens.py -- last modified this session"

### Layer 2 -- Adaptive micro-compaction

Remove low-relevance messages from the working context summary:
- Greetings, pleasantries, "got it" acknowledgments -- drop
- Failed attempts that were superseded -- drop (keep only the final solution)
- Debugging output that led to a resolved issue -- compress to: "Fixed: [symptom] -> [fix]"
- Retain: decisions made, constraints confirmed, commands that worked

### Layer 3 -- Narrative summarization

Convert older conversation history into a technical summary paragraph:

```
We established the screen inventory (22 screens, M0-M3), wrote build_static_screens.py
with the standard helper functions, and ran Playwright capture. The CSS variable names
were corrected from --bg-primary to --bg after comparing against real project output.
Auth cookie transport was fixed in the backend middleware to accept ng_token alongside
bearer token. All unit tests pass; E2E suite passes for the runnable subset.
```

One paragraph per major work block. Drop chronology, keep facts.

### Layer 4 -- Structural compaction (9-point model)

Preserve the project state in 9 fixed categories:

```
1. GOAL: [current objective in one sentence]
2. STACK: [technology decisions, locked]
3. DONE: [completed items, bulleted]
4. IN PROGRESS: [active work item]
5. BLOCKED: [what is blocked and why]
6. DECISIONS: [locked choices that must not be revisited]
7. CONSTRAINTS: [hard rules that apply to all work]
8. NEXT: [immediate next action]
9. FILES: [key file paths and their current state]
```

This is the minimum viable context for a fresh session to resume without re-asking questions.

### Layer 5 -- Fact extraction

Pull durable facts that should survive into future sessions:

Durable facts (always keep):
- Confirmed technology choices ("Backend is TypeScript/Express, not Python -- decided Apr 2026")
- Hard constraints ("Never git init from Linux sandbox on Windows paths")
- Fixed credentials/paths ("gh-token at <project>/...")
- Known failure modes ("Ollama health 200 does not mean model is installed")

Volatile facts (drop after session):
- In-progress task state
- Intermediate debugging observations
- File contents that can be re-read

### Layer 6 -- Background consolidation

Identify patterns across sessions that should be promoted to permanent memory:

- A fix that worked three times = a rule, not an observation
- A failure mode encountered twice = add to the relevant SKILL.md failure table
- A decision that was revisited = it needs a stronger rationale in CONTEXT.md

Produce a short list of memory promotions:
```
PROMOTE TO MEMORY:
- [feedback] PowerShell: never use && -- use separate lines (burned twice)
- [feedback] Ug-ug mode: stay in mode until explicitly asked to exit
- [project] NestGenie backend: auth middleware fixed to accept ng_token cookie
```

### Layer 7 -- Multi-agent handoff

When handing context to a sub-agent or a new session, produce a structured handoff block:

```
=== SESSION HANDOFF ===
From: [current session/agent]
To: [target session/agent]
Date: [date]

INHERIT:
[Paste the Layer 4 structural state here]

DO NOT REDO:
[List of completed work items -- sub-agent should not repeat these]

OPEN THREAD:
[Exactly where the current session left off]

START HERE:
[The single next action for the inheriting session]
=== END HANDOFF ===
```

---

## Key rules / constraints

- **Run layers in order.** Do not jump to Layer 6 without doing Layers 1-5 first.
- **Preserve decisions and constraints above all else.** Decisions that get lost cause
  rework. When in doubt about what to keep, keep the decision.
- **Never summarize away a file path or command.** These must be exact or they are useless.
- **Layer 4 is the minimum for any handoff.** Even for a quick session switch, the 9-point
  structural state must be preserved.
- **Volatile state does not travel.** Do not carry in-progress scratch work into the handoff.
  Only carry completed facts and the single open thread.

---

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Summarizing too aggressively | New session re-asks settled questions | Keep decisions and constraints verbatim; only compress narrative |
| Carrying volatile state | New session confused by half-done work | Layer 5: classify as durable vs volatile before handoff |
| Skipping identity anchor | New session starts without project context | Layer 1 first, always |
| Dropping file paths in summary | Agent looks for file that was referenced but path is gone | Layer 4 item 9: all key files with paths, explicitly |
| Over-compressing to the point of ambiguity | Summary is terse but vague -- agent makes wrong assumptions | Keep technical specifics; compress prose, not facts |

## Handoffs

- **→ session-handover** when context limit is reached and state must be persisted
- **→ agent-memory** for short-term in-session memory patterns
- **→ operator** if memory retrieval returns stale or contradictory state
- **→ claude-subconscious** (`skills/agent-llm/claude-subconscious/SKILL.md`) — passive companion; activate at session start, drain at session end alongside Layer 6 promotion
- **→ stop-hook** (`skills/memory/stop-hook/SKILL.md`) — auto-flushes memory on session end; stamps MEMORY.md timestamp + calls compress_for_ollama.py; fires automatically via Claude Code `Stop` hook
- **→ obsidian-vault** (`skills/memory/obsidian-vault/SKILL.md`) — browse/edit raw memory files in Obsidian graph view; add_frontmatter.py backfills YAML tags + related links across all 47 topic files

---

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `bulk_offload` | Layer 1 — identify large blobs, replace with file references | yes | ⚠️ (file-based; requires access to local project paths — not Lambda) |
| `micro_compact` | Layer 2 — remove low-relevance messages from context summary | yes | ⚠️ (file-based, local-only by design) |
| `narrative_summarize` | Layer 3 — convert older history to technical summary paragraph | yes | ⚠️ (file-based, local-only by design) |
| `structural_compact` | Layer 4 — produce 9-point project state snapshot | yes | ⚠️ (file-based, local-only by design) |
| `extract_durable_facts` | Layer 5 — classify facts as durable vs volatile | yes | ⚠️ (file-based, local-only by design) |
| `promote_to_memory` | Layer 6 — identify patterns to promote to SKILL.md or CONTEXT.md | yes | ⚠️ (file-based, local-only by design) |
| `write_handoff_block` | Layer 7 — produce structured SESSION HANDOFF document | yes | ⚠️ (file-based, local-only by design) |

Note: memory-ladder is file-based and local-only by design. All steps write to local project files. Not Lambda-compatible without S3 I/O rewrite.

---

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `trigger` | string | yes | `compress` / `new-session` / `handoff` / `promote` |
| `layers` | int[] | no | Which layers to run (1–7); defaults to running all in order |
| `project` | string | yes | Project name or slug |
| `goal` | string | yes | Current objective in one sentence |
| `stack` | string | no | Technology decisions already locked |
| `conversation_history` | string | no | Raw conversation text to compress (Layers 1–3) |
| `target_agent` | string | no | For Layer 7 handoff: name/path of receiving agent |

**Output:**
```json
{
  "status": "ok | error",
  "result": {
    "layers_run": [1, 2, 3, 4],
    "structural_state": {
      "goal": "...",
      "stack": "...",
      "done": ["..."],
      "in_progress": "...",
      "blocked": "...",
      "decisions": ["..."],
      "constraints": ["..."],
      "next": "...",
      "files": ["..."]
    },
    "memory_promotions": ["PowerShell: never use && -- use separate lines"],
    "handoff_block": "=== SESSION HANDOFF === ..."
  }
}
```
