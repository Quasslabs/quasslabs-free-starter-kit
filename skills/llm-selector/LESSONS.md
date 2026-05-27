# Lessons Learned — llm-selector

| Lesson | Why it matters | Source |
|---|---|---|
| Treat the documented failure modes as runtime guardrails. | The SKILL.md already names the mistakes this workflow is meant to prevent. | SKILL.md Common failure modes |
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for llm-selector. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## Repo additions — 2026-05-17 triage (Pull-in attribution)

Source: `<notes>/...` → "2026-05-17 high priority pulls".

- **`AlexsJones/llmfit` (25k★ MIT)** — hardware-aware LLM model finder. One command to enumerate hundreds of models and providers and surface which ones fit on the current machine's GPU/RAM. **Adopt:** wire into the `llm-selector` model-selection step as a pre-filter — before recommending a local model, run `llmfit --vram <GB>` to confirm it fits on this machine. Prevents recommending models that would OOM. Install: `pip install llmfit` or build from source. Complements the Ollama model roster in `<workspace>/...`.
