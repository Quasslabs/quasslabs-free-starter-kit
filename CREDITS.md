# Credits + upstream licenses

These skills stand on a lot of other people's work. Below is the full attribution for every skill in this kit. Our implementations are clean-room rewrites in our own house format unless marked **direct import** (where the upstream license governs and that work is genuinely theirs).

If you're building your own skill library, treat this page + [`OTHER-REPOS.md`](OTHER-REPOS.md) as a curated reading list — these are the projects worth learning from.

---

## Pattern / concept inspiration (clean-room, credited)

| Skill | Built on |
|---|---|
| `ug-ug` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) + [rtk-ai/rtk](https://github.com/rtk-ai/rtk) (Apache-2.0) — token-efficiency concept |
| `gstack` | Role/pipeline taxonomy (`/office-hours`, `/plan-ceo-review`, `/review`, `/qa`, `/ship`, etc.; Think → Plan → Build → Review → Test → Ship → Reflect) **adapted from [Garry Tan's gstack](https://github.com/garrytan/gstack)**, MIT © Garry Tan; + [algorithmicsuperintelligence/optillm](https://github.com/algorithmicsuperintelligence/optillm) (Apache-2.0) — model-optimization backing |
| `llm-selector` | [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT) — hardware-aware model fit as a pre-filter |
| `session-handover` | [voidcraft-dev/memory-forge-rs](https://github.com/voidcraft-dev/memory-forge-rs) (MIT) — editable-session-state model |
| `memory-ladder` | Layered memory pipeline **patterned on [whiterabb17/mindpalace](https://github.com/whiterabb17/mindpalace)** (we renamed ours to avoid the name clash), then extended into a local-first system: Ollama (phi4-mini) compaction, cross-project semantic recall, Obsidian browsing, and Stop-hook auto-flush. Also mined: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) (MIT, 3-file convention) · [NirDiamant/Agent_Memory_Techniques](https://github.com/NirDiamant/Agent_Memory_Techniques) · [rowboatlabs/rowboat](https://github.com/rowboatlabs/rowboat) (Apache-2.0) |
| `skill-builder` | [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) + [google/skills](https://github.com/google/skills) (Apache-2.0) + [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT) + [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) — skill-format + auto-draft-from-source patterns |

## Original (QuassLabs)

No external upstream — built here, licensed MIT (see `LICENSE.md`):
`task-router` · `ollama-task-router` · `notify` · `reflect` · `skill-linter` · `operator`

---

If you are an upstream author and want a credit added, corrected, or removed, open an issue. Everything original here is © 2026 QuassLabs / Taylor Quass, MIT.
