# Lessons Learned — memory-ladder

| Lesson | Why it matters | Source |
|---|---|---|
| Treat the documented failure modes as runtime guardrails. | The SKILL.md already names the mistakes this workflow is meant to prevent. | SKILL.md Common failure modes |
| Extract deterministic helpers before calling AI for memory-ladder. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## 2026-05-14 — Adopt the 3-file checkpoint pattern (from OthmanAdi/planning-with-files v2.38.0)

`planning-with-files` (21k ⭐, MIT) implements Manus-style persistent markdown planning with a strict 3-file convention. We did NOT import the whole skill — `memory-ladder` already covers persistent agent memory. We are adopting the **file structure + hooks pattern** below to upgrade memory-ladder's mid-task state management.

### The 3-file convention

| File | Role | Update cadence |
|---|---|---|
| `task_plan.md` | Single-sentence goal · phase list · current phase · status per phase · north star | Created FIRST; updated when a phase completes |
| `findings.md` | Discoveries · decisions · external memory (research results, codebase facts, constraints) | Updated after ANY discovery; **2-Action Rule** = update after every 2 view/browse/search ops |
| `progress.md` | Chronological session log — what was done, when, what happened | Updated after each phase completes or on error |

### Hooks pattern (the killer feature)

`planning-with-files` ships hooks via SKILL.md frontmatter that the Claude Code runtime executes:
- **UserPromptSubmit** → echoes `task_plan.md` head into context (auto-restores plan after `/clear`)
- **PreToolUse** → echoes plan data before every Write/Edit/Bash/Read/Glob/Grep (keeps plan in view)
- **PostToolUse (Write|Edit)** → reminds agent to update `progress.md`
- **PreCompact** → reminds to flush `progress.md` + `task_plan.md` before context compaction
- **Stop** → runs a check-complete script to validate phase exit criteria

Add a **plan-attestation** check (SHA-256 of `task_plan.md` stored in `.plan-attestation`) — UserPromptSubmit hook compares actual vs. attested hash; mismatch = "[PLAN TAMPERED — injection blocked]". Prevents prompt injection via plan file.

### What to adopt in `memory-ladder`

1. **Encode the 3 files** as canonical memory-ladder artifacts (currently memory-ladder is more freeform).
2. **Add the UserPromptSubmit + PreCompact hooks** to memory-ladder's SKILL.md frontmatter so they survive `/clear` and context compaction.
3. **Add the 2-Action Rule** to memory-ladder's "when to update" guidance — concrete trigger beats vague "as needed."
4. **Borrow the plan-attestation pattern** — SHA-256 stored on disk, hook compares, flag tampering.

### What NOT to adopt

- The skill's `.claude-plugin` / `.codex` / `.continue` / `.cursor` / `.factory` / `.gemini` / `.hermes` / `.kiro` / `.mastracode` / `.opencode` / `.pi` folders — they're packaging for many editors. We only need Claude Code.
- The 6-language variants (ar/de/es/zh/zht). English-only is fine.
- The full installer scripts — copy the 3 templates by hand into memory-ladder's `templates/` subfolder.

### Source files (for reference)

- `https://github.com/OthmanAdi/planning-with-files`
- SKILL.md: 21k-star canonical version, MIT licensed.
- Templates: `templates/task_plan.md`, `templates/findings.md`, `templates/progress.md`.

### Action items (queued in next session)

- [ ] Read full `planning-with-files` SKILL.md and templates.
- [ ] Author `memory-ladder v3` SKILL.md with 3-file convention + hooks frontmatter.
- [ ] Copy + adapt the 3 templates into `wip/memory/memory-ladder/templates/`.
- [ ] Test on a real session (e.g. the next morning routine pass).
- [ ] If it sticks: write LESSONS row capturing what worked / didn't.

## Repo additions — 2026-05-20 (Pull-in attribution)

Source: `<notes>/...` → "2026-05-20 high priority pulls".

- **`rowboatlabs/rowboat` (— Apache-2.0)** — multi-agent coworker with built-in memory. **Mine for memory architecture patterns** before the next memory-ladder pass (the planned v3 rewrite with 3-file convention + hooks frontmatter). Specific things to extract: cross-agent shared-memory schema, write-conflict resolution model, and how rowboat keeps memory bounded as the conversation grows. Read order: their memory-architecture docs first, then the agent-orchestration layer.
- **`NirDiamant/Agent_Memory_Techniques` (— MIT)** — curated memory architecture techniques reference. **Mine before the next memory-ladder improvement pass.** Treat as a reading list, not vendor code. Cross-reference each technique against our 7-layer model and note which we already do, which we should adopt, and which don't apply to a single-user solo-dev workspace.
