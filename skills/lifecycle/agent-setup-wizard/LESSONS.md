# Lessons Learned — agent-setup-wizard

| Lesson | Why it matters | Source |
|---|---|---|
| Run setup before code. | The skill explicitly exists to lock routing, memory, models, and guardrails before implementation starts. | `SKILL.md` Role and When to invoke |
| Treat missing AWS bootstrap as a hard branch. | Downstream IAM, logging, and rate-limit choices depend on the account baseline. | `SKILL.md` Phase 1 and Phase 9 |
| Render project files from structured setup data. | Operator config and CLAUDE.md drafts should agree because they come from the same plan. | `SKILL.md` Phases 7 and 8 |
| Use Opus sparingly. | Most setup drafting fits Sonnet; Opus is justified only for high-impact architecture choices. | `SKILL.md` Model routing |

---

## Repo additions — 2026-05-16 triage

Source: `<notes>/...` → "Full triage — 2026-05-16".

- **`google-labs-code/design.md` (13.9k★ Apache)** — a published `DESIGN.md` format spec that coding agents (Claude Code, Codex, Gemini) read for architectural intent. **Adopt:** the wizard should generate a `DESIGN.md` alongside `CLAUDE.md` + `AGENTS.md` for new projects — CLAUDE.md = operating rules, DESIGN.md = architecture/data-model/decisions the agent must respect. Add a new wizard phase: "Phase 8b — emit DESIGN.md from arch-decision/ADR data." Spec lives in the repo; mirror its section structure (Overview / Data Model / Constraints / Non-goals).
- This complements existing ADR.md output — DESIGN.md is the agent-facing distilled view; ADR.md stays the decision log.

---

## Repo additions — 2026-05-18 triage (Pull-in attribution)

Source: `<notes>/...` → "TQuass full triage — 2026-05-15".

- **`luongnv89/claude-howto` (30k★)** — visual, example-driven guide to Claude Code: basic→advanced agents, copy-paste templates. **Adopt:** reference as the onboarding companion the wizard points new agents/coworkers at — after the wizard emits CLAUDE.md/AGENTS.md/DESIGN.md, link claude-howto in the generated `_context/` onboarding note so a human ramping on Claude Code has a worked-example guide. Pattern/reference resource, not a dependency.