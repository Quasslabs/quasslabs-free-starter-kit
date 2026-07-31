# Functions — task-router

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `evaluate(task)` | str | dict | Returns red_gates, yellow_notes, estimated_cost, recommended_skill |
| `find_red_gates(task)` | str | list[str] | Keyword scan for missing-credential / irreversible signals |
| `find_yellow_notes(task)` | str | list[str] | Ambiguity / TODO / assumption signals |

## AI-assisted steps

None. Pure heuristic rules.

## External services

None.
