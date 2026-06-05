# REPORT: local-model-route

**Skill:** `local-model-route` (local-model-route)
**Kit:** none · **Tier:** free
**Last measured:** 2026-05-31 (v2-backfill, beta)

---

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Wrong model selected (OOM) | 14B + 7B running → OOM → crash | Hard rule: never run 14B + any other gen model | routing table enforcement |
| Model for ambiguous task | Trial and error | Task type → model table lookup | routing decision |
| Context length blowout | Default 4k silently truncates | Explicit guidance: raise to 16k only when needed | routing decision |
| Cloud fallthrough | Unnecessary sonnet calls | Local routing decision first, escalate consciously | routing flow |

---

## Who gets the most value

Any session before starting a local Ollama session when the right model isn't obvious — prevents the most expensive mistake (running the wrong model size and causing OOM or quality failures).

## How it fits in a flow

**Invoked before** any `ollama run` or Ollama API call when model isn't clear  
**Routing table:** qwen2.5-coder:3b/7b (code) · qwen3:8b (general) · deepseek-r1:8b (review/critique) · qwen2.5-coder:14b (edge) · nomic-embed-text (embeddings)

## Skill interactions

| Pairs with | How |
|---|---|
| `ollama-multi-host-router` | local-model-route picks which model; multi-host-router picks which machine |
| `ollama-task-router` | ollama-task-router annotates a plan list; this skill makes a single routing decision |

## Measured outcomes

Hard limits on 12GB VRAM documented and enforced: never run 14B + another gen model simultaneously. Context length rule: default 4k; only raise to 16k for OpenCode tool use or PRD work. These constraints come from direct RTX 3060 testing.

## Test coverage

| Test | Type | Expected output |
|---|---|---|
| "Code edit, refactor" | behavior | Routes to `qwen2.5-coder:7b` |
| "PRD draft, PM summary" | behavior | Routes to `qwen3:8b` |
| "Embeddings for search" | behavior | Routes to `nomic-embed-text` |
| "14B requested + 7B running" | behavior | Warning: close 7B first |
