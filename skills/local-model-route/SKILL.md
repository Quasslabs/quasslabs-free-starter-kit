---
name: local-model-route
description: >
  Routes any task to the correct local Ollama model based on task type, context
  size, and privacy requirements. Prevents GPU overload on 12GB VRAM systems.
ug-ug: lite
model: sonnet
gstack_stage: Think
---

# SKILL: local-model-route

**Bot:** any
**Role:** Given a task description and constraints, select the correct local Ollama model and emit a ready-to-use routing decision with `ollama run` or API call pattern.
**Ug-ug mode:** lite
**Status:** beta  <!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->
**Parallelizable:** yes — no shared mutable state detected (auto-inferred; verify)
**Model:** sonnet
**Tool compatibility:** Claude Code · OpenCode · Aider · n8n HTTP node

---

## When to invoke

Trigger phrases: "which model should I use?", "route this task", "what ollama model for X", "local model for [task]", "offload to ollama"

Invoke before any local Ollama session when the right model isn't obvious.

---

## Routing table

| Task type | Model | Size | Notes |
|-----------|-------|------|-------|
| Tab autocomplete | `qwen2.5-coder:3b` | 1.9GB | Always-on, fastest |
| Boilerplate / light code transforms | `qwen2.5-coder:3b` | 1.9GB | Low latency |
| Code edit, refactor, focused build | `qwen2.5-coder:7b` | 4.7GB | Main coding sweet spot |
| PRD draft, PM summary, scoped estimate | `qwen3:8b` | 5.2GB | Best general local model |
| Estimate sanity check, spec critique | `deepseek-r1:8b` | 4.9GB | Slower; use for review only |
| 14B edge sessions (short, focused) | `qwen2.5-coder:14b` | 9.0GB | Edge of comfort; close other models first |
| Embeddings (Mem0, Qdrant, repo search) | `nomic-embed-text` | 274MB | Always-on alongside gen model |
| Higher-quality embeddings | `qwen3-embedding:8b` | 4.7GB | Run separately from large gen jobs |

**Hard limits on 12GB VRAM:**
- Never run 14B + any other gen model simultaneously
- Default context: 4k (Ollama default under 24GB VRAM). Raise to 16k only when OpenCode tool use or PRD work needs it: `OLLAMA_CONTEXT_LENGTH=16384 ollama serve`
- 30B+ models: not viable locally

---

## Step-by-step execution

### Step 1 — Classify the task

```
task_type:       autocomplete | code-edit | prd-summary | estimate-review | embeddings
context_needed:  small (<4k) | medium (4k–16k) | large (>16k)
privacy:         local-only | cloud-ok
concurrent_jobs: list any other models currently loaded
```

### Step 2 — Apply routing logic

```
IF privacy == local-only → always route local regardless of task
IF context_needed == large AND task != embeddings → warn: may need cloud exception path
IF concurrent_jobs includes 14b model → do not add another gen model
ELSE → pick from routing table above
```

### Step 3 — Emit decision

```
MODEL:    qwen3:8b
CONTEXT:  16384  (raise only if needed)
PATTERN:  ollama run qwen3:8b
          OR: curl http://localhost:11434/api/generate -d '{"model":"qwen3:8b","keep_alive":"30m"}'
REASON:   PRD draft — general reasoning, no long context needed
```

---

## Cloud exception path

Only use when:
- Context clearly exceeds 16k–32k effective local capacity
- Multi-repo architectural reasoning required
- Deliverable has zero margin for error

Never send: raw secrets, broad repo snapshots, PII, client-confidential code.
Send: Repomix-compressed slices, redacted excerpts, issue-specific context only.

---

## Key rules

- **Autocomplete model stays loaded all day** — 3B never competes with main model
- **nomic-embed-text stays loaded** alongside any gen model (only 274MB)
- **deepseek-r1:8b is for review passes only** — not interactive sessions
- **Never recommend cloud for proprietary client code** (PrevenDebt, WebMeet, etc.)

---

## Handoffs

| Next step | Where |
|-----------|-------|
| Terminal agent loop | `skills/opencode-aider/SKILL.md` |
| Repo context packaging | `skills/repomix-pack/SKILL.md` |
| Memory system bootstrap | `skills/mem0-qdrant/SKILL.md` |

## Permissions

<!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<workspace>/...` | Referenced in skill body |
| Network | `https://localhost/*` | Referenced in skill body |
