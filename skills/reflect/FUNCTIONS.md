# Functions — reflect

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `format_retro(project, sections, date)` | str, dict, str | str | Markdown template fill |
| `append_lessons(notes_path, entry)` | path, str | path | Creates `_context/LESSONS.md` if missing |
| `reflect(notes_path, entry, project, date)` | path, str, str, str | dict | Orchestrator |

## AI-assisted steps

| Step | Model | Notes |
|---|---|---|
| Synthesize four-part retro from session context | any | Optional; reflect can be called with pre-built entry text |

## External services

None.
