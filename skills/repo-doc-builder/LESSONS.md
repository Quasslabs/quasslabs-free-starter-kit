# LESSONS: repo-doc-builder

---

## Production lessons

*(none yet — first run 2026-05-15)*

---

## Known gotchas to anticipate

- **Stub sections:** Claude will drift toward writing `[TODO]` or `[TBD]` in env var tables if it can't find the values. Force it: if a var is unknown, write a realistic placeholder and note `(confirm value)` inline, not `[TBD]`.
- **Overly deep trees:** repos with many nested dirs produce trees too long for one doc. Collapse anything beyond 3 levels to `...` and move the deep paths to "key files" table instead.
- **Duplicate classification signals:** a bot-lambda repo can also have a `docs/` dir, triggering docs-only detection. Apply signals in priority order: full-stack > bot-* > skill-set > library > docs-only.
- **GitHub API tree limit:** `gh api repos/.../git/trees/HEAD?recursive=1` truncates at 100k entries. For very large repos, switch to listing just the top 2 levels.
- **Windows paths in generated docs:** any local paths written into docs should be converted from `<project>/...` Windows format to forward-slash for cross-platform readers, OR use a `{repo_root}` placeholder that reads naturally.
