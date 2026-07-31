# Functions — skill-linter

## Pure functions (Lambda-ready)

| Function | Input | Output | Notes |
|---|---|---|---|
| `lint(path)` | str | list[str] | Returns list of issues; empty list = pass |
| `check_header(text)` | str | list[str] | Header-field-only check |
| `check_sections(text)` | str | list[str] | Section-presence check |

## AI-assisted steps

None. All checks are rule-based regex.

## External services

None.
