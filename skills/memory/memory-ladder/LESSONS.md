# Lessons Learned — memory-ladder

| Lesson | Why it matters | Source |
|---|---|---|
| Treat the documented failure modes as runtime guardrails. | The SKILL.md already names the mistakes this workflow is meant to prevent. | SKILL.md Common failure modes |
| Extract deterministic helpers before calling AI for memory-ladder. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |

---

## Repo additions — 2026-05-30 (star triage)

### thedotmack/claude-mem — cross-session memory compression pattern
Source: `<notes>/...` → "Star triage — 2026-05-30".
- **claude-mem (76k★ Apache-2.0):** captures everything the agent does during a session → AI-compresses it → injects compressed memory at the start of the next session. Stop hook triggers compression; UserPromptSubmit hook injects.
- **Alignment with memory-ladder:** claude-mem is essentially memory-ladder Layer 4 (cross-session compressed summaries) with automatic triggering via hooks. Our Layer 4 currently requires manual `session-handover` invocation.
- **Pattern to adopt:** add a Stop hook in `settings.json` that calls `memory-ladder compact <project-slug>` automatically — same effect as claude-mem's compression step. Eliminates the "remember to run session-handover" friction.
- **Compression strategy:** claude-mem uses Claude itself to compress (expensive per session). Our `compress-session` skill uses phi4-mini (local, $0). Prefer local compression for daily sessions; Claude-quality compression for major milestone handoffs only.
- **Injection strategy:** claude-mem injects at UserPromptSubmit. Our chat-primer already does this (Phase 1.5a reads memory). No change needed — confirm chat-primer's injection includes the compressed layer.

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

## 2026-05-30 — Mandatory 3-file persistence discipline (pattern-after a5c-ai/babysitter session-memory)

`session-memory` is a more opinionated, narrower take than our layered model: a fixed **3-file** memory surface in `.claude/cc10x/` with an "Iron Law" that EVERY workflow loads at start and updates at end. Worth adopting the *discipline*, not replacing our layers.

### The exact 3-file structure

| File | Role | Maps to memory-ladder |
|---|---|---|
| `activeContext.md` | Current focus · decisions · learnings · next steps · blockers | Layer 1–2 (working state) + handover seed |
| `patterns.md` | Project conventions · architecture decisions · common gotchas · reusable solutions | Layer 3 (project LESSONS) — the durable "how we do things here" |
| `progress.md` | Task completion tracking **with verification evidence** | Layer 2 (chronological session log) |

This is the same shape as the `planning-with-files` 3-file convention already noted above (`task_plan`/`findings`/`progress`), but session-memory's framing of the *middle* file as **patterns** (durable conventions) rather than **findings** (transient research) is the useful distinction — it separates "what I'm learning right now" from "what is permanently true about this project."

### The "mandatory on every session" discipline (the real lesson)

- **Iron Law:** LOAD at START (and before key decisions) · UPDATE at END (and after any learning/decision). No workflow is exempt. This is stronger than memory-ladder's current "update as needed" guidance and complements the 2-Action Rule already queued for v3.
- **Stable edit anchors:** pre-declare safe section headers (`## Recent Changes`, `## Learnings`, `## Common Gotchas`, `## Completed`, `## Verification`) so `Edit` operations have deterministic `old_string` targets — avoids the "anchor drifted, edit failed" problem on long-lived memory files.
- **Read-Edit-Verify loop:** Read file → confirm anchor exists → Edit with exact `old_string` → Read back to confirm. Worth encoding in memory-ladder's `save()` backend contract.
- **Permission-free by design:** `Write()` for NEW files, `Edit()` for EXISTING; never `Write()`-overwrite an existing memory file; never compound shell commands (`mkdir && cat`). Keeps memory updates from triggering permission prompts mid-session — directly relevant to our chat-primer auto-injection.
- **Verification evidence in progress.md** is the strongest borrow: don't just log "did X," log the proof X worked. Pairs with our reflect skill.
- Source: https://github.com/a5c-ai/babysitter (session-memory skill)

## 2026-05-30 - pattern-after: a5c-ai/babysitter session-memory (511 stars, live source)
- Mandatory 3-file memory structure per session (context / decisions / next-actions) - a hard convention, not optional. Reinforces our existing ladder: never end a session without writing all three. The discipline (always-write, never-skip) is the borrowed pattern.
