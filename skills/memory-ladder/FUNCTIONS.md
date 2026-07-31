# Functions — memory-ladder

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `load(slug)` | str | dict | Reads `~/.memory/<slug>.json`; empty dict if missing |
| `save(slug, payload)` | str, dict | Path | Writes JSON; creates parent dir |
| `append(slug, entry)` | str, Any | int | Appends to `entries` list; returns new length |
| `memory_path(slug)` | str | Path | Resolves the per-slug file path |

## AI-assisted steps

None.

## External services

None — local filesystem only.
