# Lessons Learned — gstack

| Lesson | Why it matters | Source |
|---|---|---|
| Treat the documented failure modes as runtime guardrails. | The SKILL.md already names the mistakes this workflow is meant to prevent. | SKILL.md Common failure modes |
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for gstack. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## Repo additions — 2026-05-16 triage

Source: `<notes>/...` → "Full triage — 2026-05-16".

- **`algorithmicsuperintelligence/optillm` (3.8k★ Apache)** — inference-optimization proxy for LLMs (sits in front of any OpenAI-compatible endpoint; applies techniques like best-of-n, CoT routing, MoA to lift quality at fixed model). **Adopt:** document optillm as an optional proxy layer in the gstack routing chain — for hard tasks, route through optillm instead of upgrading the model tier (cheaper quality lift than jumping sonnet→opus). Add to model-selection decision: try optillm-on-sonnet before escalating to opus. Pairs with `local-runner` (optillm can front LocalAI/vLLM too).
