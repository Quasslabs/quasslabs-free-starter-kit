# Credits + upstream licenses

These skills stand on a lot of other people's work. Below is the full attribution for every skill in this kit. Our implementations are clean-room rewrites in our own house format unless marked **direct import** (where the upstream license governs and that work is genuinely theirs).

If you're building your own skill library, treat this page + [`OTHER-REPOS.md`](OTHER-REPOS.md) as a curated reading list — these are the projects worth learning from.

---

## Direct imports (upstream license governs)

| Skill | Upstream | License |
|---|---|---|
| `developer/tdd` | [mattpocock/skills](https://github.com/mattpocock/skills) — `engineering/tdd` | MIT © Matt Pocock |
| `developer/zoom-out` | [mattpocock/skills](https://github.com/mattpocock/skills) — `engineering/zoom-out` | MIT © Matt Pocock |
| `developer/improve-codebase-architecture` | [mattpocock/skills](https://github.com/mattpocock/skills) — `engineering/improve-codebase-architecture` | MIT © Matt Pocock |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) v2.5.1 | MIT © blader |

> These retain their upstream MIT terms + copyright. If you redistribute them, keep the attribution above.

## Pattern / concept inspiration (clean-room, credited)

| Skill | Built on |
|---|---|
| `ug-ug` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) + [rtk-ai/rtk](https://github.com/rtk-ai/rtk) (Apache-2.0) — token-efficiency concept |
| `gstack` | [garrytan/gstack](https://github.com/garrytan/gstack) — multi-role full-stack workflow; + [algorithmicsuperintelligence/optillm](https://github.com/algorithmicsuperintelligence/optillm) (Apache-2.0) — model-optimization backing |
| `llm-selector` | [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT) — hardware-aware model fit as a pre-filter |
| `lifecycle/agent-setup-wizard` | [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) — onboarding pattern; + [google-labs-code/design.md](https://github.com/google-labs-code/design.md) (Apache-2.0) — DESIGN.md artifact format |
| `lifecycle/session-handover` | [voidcraft-dev/memory-forge-rs](https://github.com/voidcraft-dev/memory-forge-rs) (MIT) — editable-session-state model |
| `memory/memory-ladder` | 7-layer memory pipeline **patterned on [whiterabb17/mindpalace](https://github.com/whiterabb17/mindpalace)** (we renamed ours to avoid the name clash), then extended into a local-first system: Ollama (phi4-mini) compaction, a pluggable `memory/` backend namespace, cross-project semantic recall, Obsidian browsing, and Stop-hook auto-flush. Also mined: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) (MIT, 3-file convention) · [NirDiamant/Agent_Memory_Techniques](https://github.com/NirDiamant/Agent_Memory_Techniques) · [rowboatlabs/rowboat](https://github.com/rowboatlabs/rowboat) (Apache-2.0) |
| `meta/skill-builder` | [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) + [google/skills](https://github.com/google/skills) (Apache-2.0) + [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT) + [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) — skill-format + auto-draft-from-source patterns |
| `humanizer` (extends the import above) | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) — extra AI-tell detector patterns |

## Original (QuassLabs)

No external upstream — built here, licensed MIT (see `LICENSE.md`):
`lifecycle/chat-primer` · `lifecycle/project-env-setup` · `lifecycle/reflect` · `repo-doc-builder` · `task-router` · `ollama-task-router` · `notify` · `meta/skill-linter`

---

If you are an upstream author and want a credit added, corrected, or removed, open an issue. Everything original here is © 2026 QuassLabs / Taylor Quass, MIT.
