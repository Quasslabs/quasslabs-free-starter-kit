# Lessons Learned — session-handover

| Lesson | Why it matters | Source |
|---|---|---|
| Keep credentials and target scope outside generated artifacts. | This skill interacts with services where leaked tokens, wrong accounts, or wrong targets create real risk. | SKILL.md external service rules |
| Extract deterministic helpers before calling AI for session-handover. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |


## Repo additions — 2026-05-25 (Pull-in attribution — star triage)

- **`voidcraft-dev/memory-forge-rs` (291★ MIT)** — "edit the AI memory instead of resetting the chat"; local session manager for Claude Code. **Pattern-after.** Mine its editable-session-state model for `session-handover` (let the user curate what carries forward, not just an auto-dump). MIT = vendorable if useful.
