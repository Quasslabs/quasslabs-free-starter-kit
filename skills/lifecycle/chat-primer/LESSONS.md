# LESSONS: chat-primer

_(Seeded 2026-05-15. Append as the skill runs in production.)_

| Lesson | Why it matters | Source |
|---|---|---|
| **Ollama ping can return 200 but model list is empty right after `ollama serve` starts — wait 3s and retry once** | `ollama serve` starts the HTTP server before all models are loaded. A 200 response with `{"models":[]}` is a false positive. Add a 3s sleep + one retry before reporting `OLLAMA: ✓`. | Local testing 2026-05-15 |
| **`_references.md` regex extraction from CLAUDE.md often catches <workspace> paths inside code blocks — filter to actual path entries, not code snippets** | CLAUDE.md has many code blocks with illustrative paths that are not real project dependencies. Scaffold `_references.md` only from explicit `## Key paths` tables or `| Thing | Path |` table rows, not from inline code examples. | Internal design review |
| **Hub drift check: REGISTRY.md has no `Added:` date column — use file mtime of the skill's SKILL.md as the proxy for "when it was added to the hub"** | REGISTRY.md rows don't carry a timestamp. Use `os.path.getmtime(wip/{skill}/SKILL.md)` and compare to the project CLAUDE.md's `Last updated:` date. Skills with mtime after CLAUDE.md date = drift candidates. | Internal design 2026-05-15 |
