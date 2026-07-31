"""session-handover — render a structured HANDOVER.md from session context."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def render_handover(ctx: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    completed = ctx.get("completed") or ["(none recorded)"]
    open_items = ctx.get("open_items") or []
    decisions = ctx.get("decisions") or []
    files = ctx.get("files_modified") or []
    lines = [
        f"# Session Handover -- {now}",
        f"**Bot:** {ctx.get('bot', 'unknown')}",
        f"**Project:** {ctx.get('project', 'unknown')}",
        "",
        "## Completed This Session",
        *[f"- {item}" for item in completed],
        "",
        "## Current State",
        ctx.get("current_state", "(not recorded)"),
        "",
        "## Open Items",
        *[f"{i+1}. {item}" for i, item in enumerate(open_items)],
        "",
        "## Key Decisions",
        *[f"- **{d.get('decision','?')}** -- {d.get('reason','')}" for d in decisions],
        "",
        "## Files Modified",
        *[f"- `{f.get('path','?')}` -- {f.get('change','')}" for f in files],
        "",
        "## Next Action",
        f"> {ctx.get('next_action', '(define before closing session)')}",
        "",
        "---",
        "## Session Opener (paste at start of next session)",
        "",
        "```",
        ctx.get("session_opener") or generate_session_opener(ctx),
        "```",
        "",
    ]
    return "\n".join(lines)


def generate_session_opener(ctx: dict) -> str:
    bot = ctx.get("bot", "agent")
    project = ctx.get("project", "this project")
    next_action = ctx.get("next_action", "review the handover")
    completed = ctx.get("completed") or []
    summary = ", ".join(completed[:2]) if completed else "no recorded items"
    open_items = ctx.get("open_items") or []
    top = open_items[0] if open_items else "(none)"
    return (
        f"Continuing {bot} session for {project}. Last session completed: {summary}. "
        f"The most important open item is {top}. Start by {next_action}."
    )


def write_handover(out_path: str, ctx: Optional[dict] = None) -> dict:
    """Render and write HANDOVER.md."""
    ctx = ctx or {}
    text = render_handover(ctx)
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return {"path": str(path), "written": True}


def main() -> None:
    out = "./HANDOVER.md"
    if "--out-path" in sys.argv:
        out = sys.argv[sys.argv.index("--out-path") + 1]
    result = write_handover(out, {"bot": "demo", "project": "demo",
                                  "next_action": "review HANDOVER.md"})
    sys.stdout.write(str(result) + "\n")


if __name__ == "__main__":
    main()
