"""task-router — heuristic pre-flight evaluator."""
from __future__ import annotations

import re
import sys

RED_PATTERNS = [
    r"\bapi[_\- ]?key\b",
    r"\bsecret\b",
    r"\bcredential",
    r"\bdeploy(?:\s+to)?\s+prod",
    r"\bforce[- ]push",
    r"\bdrop\s+(?:table|database)\b",
    r"\bmigrate\s+prod",
]
YELLOW_PATTERNS = [
    r"\btodo\b",
    r"\btbd\b",
    r"\bmaybe\b",
    r"\bassume",
    r"\bif\s+possible\b",
    r"\bnot\s+sure\b",
]


def find_red_gates(task: str) -> list[str]:
    """Return labels for red-gate triggers found in task."""
    found = []
    for pat in RED_PATTERNS:
        if re.search(pat, task, re.IGNORECASE):
            found.append(pat.strip(r"\b"))
    return found


def find_yellow_notes(task: str) -> list[str]:
    """Return labels for yellow-note triggers found in task."""
    found = []
    for pat in YELLOW_PATTERNS:
        if re.search(pat, task, re.IGNORECASE):
            found.append(pat.strip(r"\b"))
    return found


def evaluate(task: str) -> dict:
    """Run pre-flight evaluation; return routing card payload."""
    return {
        "red_gates": find_red_gates(task),
        "yellow_notes": find_yellow_notes(task),
        "estimated_cost": 0.0,
        "recommended_skill": None,
    }


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: task_router.py <task>\n")
        sys.exit(2)
    task = " ".join(sys.argv[1:])
    import json
    sys.stdout.write(json.dumps(evaluate(task), indent=2))


if __name__ == "__main__":
    main()
