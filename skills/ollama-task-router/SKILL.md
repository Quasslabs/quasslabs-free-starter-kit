# SKILL: ollama-task-router

**Bot:** any
**Role:** Annotate a plan or skill step list with LOCAL vs CLOUD routing decisions and estimate token savings vs an all-cloud baseline
**Ug-ug mode:** full
**Model:** haiku — routing decisions are deterministic keyword matching; no deep reasoning required
**Tool compatibility:** Claude Code · Codex
**Status:** beta
**Parallelizable:** conditional — Mac mini M4 is primary Ollama host; Windows is fallback only. Concurrent runs are safe when tasks route to different hosts (e.g., Mac mini + Windows in parallel). Single-host tasks still contend for model load.

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

### Mac mini M4 (<lan-host>:11434) — PRIMARY for all text inference

All text models default to Mac mini. Windows is the fallback when Mac mini is unreachable. Keeps Windows GPU free for XTTS, ComfyUI, ebook2audiobook.

| Model | Best for |
|---|---|
| `phi4-mini` | Classification, routing, yes/no judgments, short structured output, field extraction. ≤500 token context. |
| `qwen2.5:7b` | General reasoning, QA, text analysis, summarization |
| `qwen2.5-coder:7b` | Code generation, review, debugging (7B tier) |
| `qwen3:8b` | General reasoning + planning; thinking mode (`/think` prefix) |
| `gemma3` | Deterministic reasoning, fast general use |
| `qwen2.5:32b` | Long-context orchestration, complex planning, multi-step reasoning |
| `qwen2.5-coder:14b` | Code generation/review at 14B quality tier |
| `qwen3:30b` | Reasoning upgrade — 30B MoE (A3B, 3B active), 262k context; pulling 2026-05-27; verify with `ollama list` before routing here |
| `nomic-embed-text` | Text embeddings (768-dim) — semantic search / RAG. Route via `embed()` |
| `mxbai-embed-large` | Higher-quality embeddings (1024-dim) — precision-critical retrieval. Route via `embed()` |

### Windows RTX 3060 (localhost:11434) — GPU-bound tasks only

| Model | Best for |
|---|---|
| `gemma4:e2b` | Multimodal (image + text); M4 MPS support incomplete for this model |

**Windows Ollama also serves as fallback** for all models above when Mac mini is unreachable.

**Standard import:** use `call_llm(prompt, task_type=)` from `<routines>/_lib_llm.py` — handles host selection, fallback to local qwen2.5:7b if Mac mini is unreachable.

**Embeddings:** use `embed(texts, model="nomic-embed-text")` from the same module — POSTs `/api/embeddings`, returns list-of-vectors, same Mac-mini-first + local-fallback host logic. Switch `model="mxbai-embed-large"` for precision-critical retrieval.

---

## Routing decision table

| Step type | Route to | Why |
|---|---|---|
| Classify / route / is-this-X | MAC MINI: phi4-mini | Fast, deterministic; offloads Windows GPU |
| Generate / refactor / review code (7B) | MAC MINI: qwen2.5-coder:7b | Code-trained; Mac mini first |
| Generate / refactor / review code (14B) | MAC MINI: qwen2.5-coder:14b | Higher quality; Mac mini has the VRAM |
| Extract fields from JSON or text | MAC MINI: phi4-mini | Structured extraction; Mac mini first |
| Summarize ≤500 tokens | MAC MINI: phi4-mini | Fast model; Mac mini first |
| Summarize >500 tokens / general QA | MAC MINI: qwen2.5:7b | Stronger general model |
| Reasoning / planning (ambiguous tasks) | MAC MINI: qwen3:8b | `/think` for chain-of-thought |
| Multimodal (image + text input) | WINDOWS LOCAL: gemma4:e2b | GPU multimodal; M4 MPS incomplete for this model |
| Long-context orchestration (14B+) | MAC MINI: qwen2.5:32b | Complex plans; use `call_llm(prompt, "orchestrate")` |
| Reasoning with extended context (30B MoE) | MAC MINI: qwen3:30b | A3B MoE; verify `ollama list` before routing; 262k ctx window |
| Draft narrative / research / creative | CLOUD: sonnet | Local models drift at open-ended creative tasks |
| Any step with >8k token context | CLOUD: sonnet | Local models hit quality cliff above this threshold |
| Multi-step reasoning chain (complex) | MAC MINI → CLOUD: qwen3:8b → sonnet | Mac mini first; escalate if quality insufficient |
| Security or compliance judgment | CLOUD: opus | High-stakes, needs best available model |
| XTTS / ebook2audiobook | WINDOWS LOCAL: direct binary | CUDA required — MPS doesn't support XTTS operations; 12GB RTX 3060 |
| ComfyUI / image gen | MAC MINI preferred: MPS | M4 24GB unified > RTX 3060 12GB for large diffusion models; MPS well-supported |

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
| Network | `http://<lan-host>:11434` | Primary — Mac mini handles all text inference |
| Network | `http://localhost:11434` | Fallback when Mac mini unreachable; also GPU-bound multimodal (gemma4:e2b) |
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
machine. Once a step is "local Ollama", the **host** (Mac mini vs Windows fallback) is
chosen by `_lib_llm.py`:

```python
from routines._lib_llm import call_llm

result = call_llm(prompt, task_type="orchestrate")  # → qwen2.5:32b @ Mac mini
result = call_llm(prompt, task_type="code")          # → qwen2.5-coder:14b @ Mac mini
result = call_llm(prompt, task_type="classify")      # → phi4-mini @ Mac mini
result = call_llm(prompt, task_type="general")       # → qwen2.5:32b @ Mac mini
```

**Default host is Mac mini** (<lan-host>). `call_llm` falls back to Windows qwen2.5:7b if Mac mini is unreachable. Windows Ollama is also used directly for `gemma4:e2b` (GPU multimodal).

File: `<routines>/_lib_llm.py` — standard import for all Ollama routing in scripts.

---

## Data collection (art-train)

Wire `log_pair()` after the routing decision, `update_outcome()` after the local call result.

```python
import sys; sys.path.insert(0, r"<workspace>/...")
from art_train_collector import log_pair, update_outcome

event_id = log_pair("ollama-task-router/route", task_description, route_decision, model="phi4-mini")

# After local model completes (no fallback needed):
update_outcome("ollama-task-router/route", event_id, "ok")

# If local model failed and cloud fallback was used:
update_outcome("ollama-task-router/route", event_id, "fallback")
```

**Training target:** `task-router-local` → phi4-mini fine-tune. Learns project-specific routing patterns that the generic decision table can't know.
