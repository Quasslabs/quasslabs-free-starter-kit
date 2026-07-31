# Functions — session-handover

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `render_handover(ctx)` | dict | str | Markdown template fill |
| `write_handover(out_path, ctx)` | path, dict | dict | Renders + writes |
| `generate_session_opener(ctx)` | dict | str | 3-5 sentence opener |

## AI-assisted steps

| Step | Model | Notes |
|---|---|---|
| Synthesize session opener from gathered context | any | Optional; can be supplied directly in ctx |

## External services

None.
