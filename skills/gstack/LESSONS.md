# Lessons Learned — gstack

| Lesson | Why it matters | Source |
|---|---|---|
| Treat the documented failure modes as runtime guardrails. | The SKILL.md already names the mistakes this workflow is meant to prevent. | SKILL.md Common failure modes |
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for gstack. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## Repo additions — 2026-05-16 triage

Source: `G:\AI\items_of_note\github-repos.md` → "Full triage — 2026-05-16".

- **`algorithmicsuperintelligence/optillm` (3.8k★ Apache)** — inference-optimization proxy for LLMs (sits in front of any OpenAI-compatible endpoint; applies techniques like best-of-n, CoT routing, MoA to lift quality at fixed model). **Adopt:** document optillm as an optional proxy layer in the gstack routing chain — for hard tasks, route through optillm instead of upgrading the model tier (cheaper quality lift than jumping sonnet→opus). Add to model-selection decision: try optillm-on-sonnet before escalating to opus. Pairs with `local-runner` (optillm can front LocalAI/vLLM too).

## 2026-06-18 — Pattern-after: revfactory/harness

- **Automatic role-assignment from task specs.** harness infers which agent roles (architect, QA, security, etc.) are needed for a given task and assembles them dynamically; gstack currently hardcodes its five-role panel. Worth exploring a spec-driven variant where the panel composition adapts to task type. Source: revfactory/harness. Not pulled in — TS/Go stack; pattern only.

## 2026-07-31 — Origin field corrected + attribution added

A live comparison against the actual upstream (github.com/garrytan/gstack, cloned read-only for the
check) found `**Origin:** original` undersold the actual relationship: the 12 role/stage command
names, their grouping, and the "Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect" pipeline
tagline are lifted verbatim from Garry Tan's repo — that's his specific expression, not generic
industry vocabulary, even though none of our actual stage content, checklists, or bot-integration
code was copied. Corrected `Origin:` to `derived-from:https://github.com/garrytan/gstack` and added
a `## Attribution` section with the MIT notice, satisfying MIT's copyright-notice-travels-with-copies
requirement without needing to relicense this skill's own (independently written) content. `_refs.md`
also had a stale local path (`G:\AI\repos\gstack`, pre-lane-reorganization) pointing nowhere — fixed
to reference the live upstream URL as the authoritative source.
