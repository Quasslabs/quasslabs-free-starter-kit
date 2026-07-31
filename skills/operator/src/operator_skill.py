"""operator — keyword-based router over a small allowlist."""
from __future__ import annotations

import sys


# Order matters: more specific keywords first.
ROUTING_TABLE = [
    ("skill-linter", ["lint", "validate", "check skill"]),
    ("skill-builder", ["draft skill", "scaffold skill", "new skill", "build skill"]),
    ("ug-ug", ["compress", "terse", "shorter", "caveman", "ug-ug"]),
    ("operator", ["route", "orchestrate", "router"]),
]


def route(task: str) -> dict:
    """Return `{skill, reason}` matched against the allowlist."""
    if not task or not task.strip():
        return {"skill": None, "reason": "empty task"}
    lower = task.lower()
    for slug, keywords in ROUTING_TABLE:
        for kw in keywords:
            if kw in lower:
                return {"skill": slug, "reason": f"matched keyword: {kw!r}"}
    return {"skill": None, "reason": "no keyword match in allowlist"}


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: operator <task description>\n")
        sys.exit(2)
    task = " ".join(sys.argv[1:])
    result = route(task)
    print(f"skill: {result['skill']}")
    print(f"reason: {result['reason']}")


if __name__ == "__main__":
    main()
