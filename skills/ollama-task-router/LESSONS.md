# Lessons Learned — ollama-task-router

| Lesson | Why it matters | Source |
|---|---|---|
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for ollama-task-router. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

## ollama-python AsyncClient — batch-05 2026-05-27

Source: `ollama/ollama-python` (dependency-only — check before writing raw httpx calls to Ollama).
- Official AsyncClient replaces raw httpx for Ollama calls: `from ollama import AsyncClient`
- Init: `client = AsyncClient(host='http://localhost:11434')`
- Generate: `response = await client.generate(model='phi4-mini', prompt='...')`
- Response is a Pydantic model; access `.response` for text; call `.model_dump()` to serialize
- When routing across hosts (Mac mini / Windows), instantiate separate AsyncClient per host with the target URL

---

## Repo additions — 2026-05-30 (star triage)

### BeehiveInnovations/pal-mcp-server — multi-model MCP dispatch pattern
Source: `<notes>/...` → "Star triage — 2026-05-30".
- **pal-mcp-server (11k★ Apache-2.0):** MCP server that dispatches a single prompt to multiple LLM providers simultaneously (Claude + Gemini + OpenAI + Ollama + custom) and returns the best or all results.
- **Relevance to task-router:** pal-mcp-server is the MCP equivalent of our `_lib_llm.py` fallback chain — but parallel instead of serial. For non-critical tasks where we want the fastest/cheapest response, parallel-dispatch + first-reply-wins is worth implementing.
- **Pattern:** when `task_type='classification'` and latency matters more than model quality, spawn parallel Ollama calls to phi4-mini (Windows) and phi4-mini (Mac mini) and take whichever responds first. Our current FALLBACK_CHAIN is serial; pal-mcp-server pattern confirms parallel is viable.
- **When NOT to use:** cost-sensitive tasks (billing per token; parallel doubles cost), stateful tasks (only one model should write state), tasks requiring reasoning coherence across steps.
