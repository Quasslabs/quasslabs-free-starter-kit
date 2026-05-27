# FUNCTIONS — improve-codebase-architecture

## Pure functions (Lambda candidates)

| Function | Input | Output | Notes |
|---|---|---|---|
| `module_metrics(repo_root)` | repo path | list[{module, interface_size, impl_size, leverage_ratio}] | AST-based, language-aware. Tree-sitter wrapper. |
| `find_pass_throughs(modules)` | module list | list[shallow_modules] | Heuristic: interface_size ≈ impl_size |
| `count_adapters(seam, repo_root)` | seam name + path | int | "One adapter = hypothetical seam. Two adapters = real seam." |
| `read_glossary(repo_root)` | repo path | dict[term, definition] | Reads CONTEXT.md domain glossary |
| `read_adrs(repo_root)` | repo path | list[{number, title, status, decision}] | Reads docs/adr/ |

## AI-assisted steps

| Step | Model | Reason | Tokens |
|---|---|---|---|
| Deepening proposal per shallow module | sonnet | Judgment about real vs. premature consolidation | ~5k in / ~2k out per module |
| Deletion-test reasoning | sonnet | "If I deleted this, what reappears?" | ~3k in / ~1k out |
| Glossary-consistency check on proposals | sonnet | Ensure proposed names match domain language | ~1k in / ~500 out |

## External services

None — fully local AST + LLM.

## Companion files

- `DEEPENING.md` — the deepening playbook
- `INTERFACE-DESIGN.md` — interface-first thinking
- `LANGUAGE.md` — full glossary (Module, Interface, Depth, Seam, Adapter, Leverage, Locality, Deletion Test)
