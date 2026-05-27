# FUNCTIONS — zoom-out

## Pure functions

| Function | Input | Output | Notes |
|---|---|---|---|
| `find_callers(symbol, repo_root)` | symbol name + repo path | list[file:line] | Reusable AST walker; could be a Lambda |
| `extract_domain_glossary(repo_root)` | repo path | list of glossary terms from CONTEXT.md / ADRs | Pure read |

## AI-assisted steps

| Step | Model | Reason | Tokens |
|---|---|---|---|
| Module-map summarization | haiku | Single-shot summary | ~3k in / ~500 out |

## External services

None.

## Note

This is a one-prompt skill (the source body is a single sentence). The richness lives in `find_callers` + `extract_domain_glossary` — they make the prompt's instruction actionable.
