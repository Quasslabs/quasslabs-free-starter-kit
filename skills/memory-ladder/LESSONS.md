# Lessons — memory-ladder

## 2026-06-11 — initial release

- File-based, not a database. Concurrent writers WILL clobber each other; Parallelizable: no is enforced for a reason.
- `~/.memory/` is created lazily; do not require the user to mkdir first.
- `append` is the most-used entry point; `save` should be rare (full-payload overwrite).
- Empty-dict on missing file is the right contract — callers should not have to try/except FileNotFoundError.
