# SKILL: ollama-task-router

**Bot:** any
**Role:** Annotate a plan or skill step list with LOCAL vs CLOUD routing decisions and estimate token savings vs an all-cloud baseline
**Ug-ug mode:** full
**Model:** haiku — routing decisions are deterministic keyword matching; no deep reasoning required
**Tool compatibility:** Claude Code · Codex
**Status:** beta
**Parallelizable:** no - dispatches to a single local Ollama instance (one GPU); concurrent runs contend for the same model load

---

## Model

**Verdict:** `phi4-mini` — routing classification is deterministic keyword matching against a fixed decision table.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Keyword classification from fixed routing table |
| Local (installed) | phi4-mini | Fast classification; fits keyword-matching task |
| Local (ideal) | phi4-mini | Already installed; ideal for routing annotation |

---

## When to invoke

- "Annotate this plan with local vs cloud steps"
- "Which steps can run locally?"
- "Route this plan through Ollama where possible"
- "Estimate token savings for this skill"
- At plan creation time before running any multi-step skill
- Called automatically by `task-router` as a sub-step (Step 0 of any orchestrated plan)
- Standalone: paste a plan in chat, get annotations back

---

## Installed Ollama models

### Windows RTX 3060 (localhost:11434)

| Model | Best for |
|---|---|
| `phi4-mini` | Classification, routing, yes/no judgments, short structured output, field extraction from JSON/text. Use for tasks with ≤500 token context. |
| `qwen2.5-coder:7b` | Code generation, refactoring, test writing, code review, debugging (7B tier) |
| `qwen2.5:7b` | General reasoning, QA, text analysis, summarization >500 tokens |
| `qwen3:8b` | General reasoning + planning; thinking mode (`/think` prefix); stronger than qwen2.5:7b on ambiguous/multi-step tasks |
| `gemma3` | Deterministic reasoning, fast general use (check `ollama list` first) |
| `gemma4:e2b` | Multimodal (image + text); use when input contains image bytes or file paths to images |

### Mac mini M4 (<lan-host>:11434) — route via `_lib_llm.py`

| Model | Best for |
|---|---|
| `qwen2.5:32b` | Long-context orchestration, complex planning, multi-step reasoning (14B+ tier) |
| `qwen2.5-coder:14b` | Code generation/review at 14B quality tier; larger context window than :7b |
| `qwen3.6-35b-a3b` *(install-pending)* | Reasoning upgrade over qwen2.5:32b — 35B MoE, 3B active params, 262k context, distilled from Claude 4.6 Opus; `ollama pull qwen3.6-35b-a3b` when available |
| `nomic-embed-text` | Text embeddings (768-dim) — semantic search / RAG vector index. Route via `embed()` |
| `mxbai-embed-large` | Higher-quality embeddings (1024-dim) — use when retrieval precision matters over speed. Route via `embed()` |

**Standard import:** use `call_llm(prompt, task_type=)` from `<routines>/_lib_llm.py` — handles host selection, fallback to local qwen2.5:7b if Mac mini is unreachable.

**Embeddings:** use `embed(texts, model="nomic-embed-text")` from the same module — POSTs `/api/embeddings`, returns list-of-vectors, same Mac-mini-first + local-fallback host logic. Switch `model="mxbai-embed-large"` for precision-critical retrieval.

---

## Routing decision table

| Step type | Route to | Why |
|---|---|---|
| Classify / route / is-this-X | LOCAL: phi4-mini | Fast, deterministic, cheap |
| Generate / refactor / review code (7B) | LOCAL: qwen2.5-coder:7b | Code-trained local model |
| Generate / refactor / review code (14B) | LOCAL → Mac mini: qwen2.5-coder:14b | Higher quality; use when 7B output is insufficient |
| Extract fields from JSON or text | LOCAL: phi4-mini | Structured extraction within local capability |
| Summarize ≤500 tokens | LOCAL: phi4-mini | Within local model capability |
| Summarize >500 tokens / general QA | LOCAL: qwen2.5:7b | Stronger general model than phi4-mini |
| Reasoning / planning (ambiguous tasks) | LOCAL: qwen3:8b | Stronger reasoning than qwen2.5:7b; use `/think` for chain-of-thought |
| Multimodal (image + text input) | LOCAL: gemma4:e2b | Only installed multimodal model |
| Long-context orchestration (14B+) | LOCAL → Mac mini: qwen2.5:32b | Complex plans, multi-document context; use `call_llm(prompt, "orchestrate")` |
| Draft narrative / research / creative | CLOUD: sonnet | Local models drift at open-ended creative tasks |
| Any step with >8k token context | CLOUD: sonnet | Local models hit quality cliff above this threshold |
| Multi-step reasoning chain (complex) | CLOUD: sonnet | Use Mac mini qwen3:8b first; escalate to cloud if quality insufficient |
| Security or compliance judgment | CLOUD: opus | High-stakes, needs best available model |

---

## Steps

### Step 1 — Parse plan
Accept input as either:
- `plan_text` (string) — markdown bullet list or numbered step list pasted directly
- `skill_md_path` (string) — path to a SKILL.md; read the `## Steps` section

Split into individual step strings. Strip markdown formatting (bullet chars, numbers, bold markers).

### Step 2 — Classify each step
For each step string, apply keyword matching (case-insensitive):

| Keyword signals | Classification |
|---|---|
| `classif`, `route`, `is this`, `detect`, `flag`, `yes/no`, `boolean` | classify/route |
| `generat`, `refactor`, `review code`, `write test`, `debug`, `implement`, `scaffold` | code |
| `extract`, `parse`, `field`, `json`, `structured` | extract |
| `summariz`, `condense`, `tldr` | summarize |
| `draft`, `research`, `creativ`, `narrat`, `write.*proposal`, `write.*brief` | draft/research |
| `reason`, `decide`, `trade-off`, `architect`, `design` | reasoning |
| `security`, `compliance`, `audit`, `vulnerability`, `threat` | security |

If a step matches multiple categories, use the highest-priority match (security > reasoning > draft > code > classify > extract > summarize).

Estimate context size: if the step description references loading a full file, transcript, or document, flag it as `>2k context`.

### Step 3 — Apply routing table
Map each classification to LOCAL or CLOUD + model name using the routing decision table above. If the model is `gemma3`, add a note: `(requires ollama list check)`.

### Step 4 — Estimate token savings
For each LOCAL step, estimate tokens saved vs using sonnet:
- Short classification step: ~200 tokens
- Code generation step: ~800 tokens
- Extraction step: ~300 tokens
- Summarization step: ~400 tokens

Multiply local token count × cloud price rate (haiku: $0.00025/1k input, $0.00125/1k output as baseline).
Report as: `~{N} tokens (~${cost} at haiku rates)`.

### Step 5 — Return annotated output
Return the full annotated step list plus summary counts and savings estimate.

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `http://localhost:11434` | Probe + dispatch to the local Windows Ollama instance |
| Network | `http://<lan-host>:11434` | Route 14B+ steps to the Mac mini Ollama host |
| Filesystem | `<routines>/_lib_llm.py` (read) | Use the standard call_llm/embed host-selection helper |

## Handoffs

- **→ task-router** — this skill is called as a sub-step of task-router (Step 0 pre-flight)
- **→ local-runner** — execute the `[LOCAL]` steps via local-runner once annotations are confirmed
- **→ llm-selector** — for `[CLOUD]` steps, llm-selector picks the specific cloud model version

---

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `parse_plan_text` | Split plan text into step strings, strip markdown | ✅ | ❌ |
| `classify_steps` | Keyword match each step → classification | ✅ | ❌ |
| `apply_routing_table` | Map classification → LOCAL/CLOUD + model | ✅ | ❌ |

**Why ❌:** This skill requires a **locally-installed and running Ollama instance** to be meaningful. There is no value in running the routing logic on Lambda when the output is used to dispatch to `localhost:11434`. Keep local.

---

## Input / Output spec

**Input (option A — raw plan text):**
```json
{
  "plan_text": "1. Classify commit type\n2. Write unit test for auth middleware\n3. Draft release notes\n4. Review PR for security issues"
}
```

**Input (option B — SKILL.md path):**
```json
{
  "skill_md_path": "G:/AI/skills/wip/fathom-fetcher/SKILL.md"
}
```

**Output:**
```json
{
  "annotated_steps": [
    {
      "step": "Classify commit type",
      "route": "LOCAL",
      "model": "phi4-mini",
      "reason": "short classification task, deterministic"
    },
    {
      "step": "Write unit test for auth middleware",
      "route": "LOCAL",
      "model": "qwen2.5-coder:7b",
      "reason": "code generation"
    },
    {
      "step": "Draft release notes",
      "route": "CLOUD",
      "model": "sonnet",
      "reason": "narrative draft, local models drift"
    },
    {
      "step": "Review PR for security issues",
      "route": "CLOUD",
      "model": "opus",
      "reason": "security judgment, high-stakes"
    }
  ],
  "cloud_steps": 2,
  "local_steps": 2,
  "estimated_token_savings": "~1,000 tokens (~$0.0003 at haiku rates)"
}
```

---

## Host dimension (2026-05-22)

This skill decides **local-vs-cloud + which model**. It does NOT pick the
machine. Once a step is "local Ollama", the **host** (Windows vs Mac mini) is
chosen by `_lib_llm.py`:

```python
from routines._lib_llm import call_llm

result = call_llm(prompt, task_type="orchestrate")  # → qwen2.5:32b @ Mac mini
result = call_llm(prompt, task_type="code")          # → qwen2.5-coder:14b @ Mac mini
result = call_llm(prompt, task_type="classify")      # → phi4-mini @ local
result = call_llm(prompt, task_type="general")       # → qwen2.5:7b @ local (fallback)
```

`call_llm` auto-falls back to local qwen2.5:7b if Mac mini (<lan-host>) is unreachable.
File: `<routines>/_lib_llm.py` — use this as the standard import for all Ollama routing in scripts.
