# SETUP: local-model-route

**Skill:** `local-model-route` (local-model-route)
**Setup tier:** simple (Ollama running + models pulled)
**Last verified:** 2026-05-31 (v2-backfill)

## Dependencies

| Dep | Version | Install | Notes |
|---|---|---|---|
| Ollama | any | (present, running) | `ollama serve` |
| Models | varies | Pull on demand | See routing table below |

## Installed models (RTX 3060 12GB)

```bash
ollama list
# Confirm these are present:
# qwen2.5-coder:3b    1.9 GB  — tab autocomplete / boilerplate
# qwen2.5-coder:7b    4.7 GB  — code edit / refactor (main coding model)
# qwen3:8b            5.2 GB  — general reasoning / PRD / PM
# qwen2.5:7b          4.7 GB  — general reasoning (alternative)
# phi4-mini           2.5 GB  — classification / routing
# nomic-embed-text    274 MB  — embeddings (always-on)
```

## Routing table (quick reference)

| Task | Model | Size |
|---|---|---|
| Tab autocomplete, boilerplate | `qwen2.5-coder:3b` | 1.9 GB |
| Code edit, refactor, focused build | `qwen2.5-coder:7b` | 4.7 GB |
| PRD draft, PM summary, scoped estimate | `qwen3:8b` | 5.2 GB |
| Estimate sanity check, spec critique | `deepseek-r1:8b` | 4.9 GB |
| Embeddings | `nomic-embed-text` | 274 MB |
| 14B edge (close others first) | `qwen2.5-coder:14b` | 9.0 GB |

## Hard limits

```
VRAM budget: 12 GB (RTX 3060)

NEVER run simultaneously:
  - 14B + any other gen model
  - Two 7B models (11.8 GB > 12 GB limit)

Default context: 4k
Raise to 16k ONLY for: OpenCode tool use, PRD work that needs full-doc context
  OLLAMA_CONTEXT_LENGTH=16384 ollama serve
```

## How to invoke

```
# Before starting a local session, ask:
"Which model should I use for [task description]?"
"Route this task to the right local model"
"What ollama model for reviewing this code diff?"
```

## Verify it works

```bash
# Check current VRAM usage
ollama ps
# Expected: shows running models and their VRAM consumption

# Test a routing call
echo "which model for: write a Python function to parse JSON" | \
  python "G:/AI/skills/wip/local-model-route/route.py"
# Expected: "qwen2.5-coder:7b — code generation task"
```

## Teardown

No persistent state. Model files remain in Ollama's store until `ollama rm <model>`.
