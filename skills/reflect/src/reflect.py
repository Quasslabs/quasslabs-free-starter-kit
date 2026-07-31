"""reflect — append a dated retro to _context/LESSONS.md."""
from __future__ import annotations

import sys
from datetime import date as _date
from pathlib import Path
from typing import Optional


def format_retro(project: str, entry: str, when: str) -> str:
    return (
        f"\n## Retro -- {project} -- {when}\n\n"
        f"{entry.strip()}\n"
    )


def append_lessons(notes_path: Path, block: str) -> Path:
    ctx = Path(notes_path) / "_context"
    ctx.mkdir(parents=True, exist_ok=True)
    lessons = ctx / "LESSONS.md"
    existing = lessons.read_text(encoding="utf-8") if lessons.exists() else "# Lessons\n"
    lessons.write_text(existing.rstrip() + "\n" + block, encoding="utf-8")
    return lessons


def reflect(notes_path: str, entry: str = "(no notes)", project: str = "session",
            when: Optional[str] = None) -> dict:
    """Append a dated four-part retro entry to LESSONS.md."""
    when = when or _date.today().isoformat()
    block = format_retro(project, entry, when)
    path = append_lessons(Path(notes_path), block)
    return {"path": str(path), "appended": True, "date": when}


def main() -> None:
    notes = "."
    entry = "(no notes)"
    project = "session"
    if "--notes-path" in sys.argv:
        notes = sys.argv[sys.argv.index("--notes-path") + 1]
    if "--entry" in sys.argv:
        entry = sys.argv[sys.argv.index("--entry") + 1]
    if "--project" in sys.argv:
        project = sys.argv[sys.argv.index("--project") + 1]
    result = reflect(notes, entry=entry, project=project)
    sys.stdout.write(str(result) + "\n")


if __name__ == "__main__":
    main()
