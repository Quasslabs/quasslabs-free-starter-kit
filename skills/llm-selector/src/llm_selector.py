"""llm-selector — pure lookup table for model + fallback + cost."""
from __future__ import annotations

import sys

CATALOG: dict[str, dict] = {
    "classify": {
        "primary": "phi4-mini",
        "fallback": ["qwen2.5:7b", "claude-haiku"],
        "estimated_cost_per_1k": 0.0,
    },
    "extract": {
        "primary": "phi4-mini",
        "fallback": ["qwen2.5:7b", "claude-haiku"],
        "estimated_cost_per_1k": 0.0,
    },
    "code": {
        "primary": "qwen2.5-coder:7b",
        "fallback": ["claude-sonnet"],
        "estimated_cost_per_1k": 0.0,
    },
    "reason": {
        "primary": "qwen2.5:7b",
        "fallback": ["claude-sonnet", "claude-opus"],
        "estimated_cost_per_1k": 0.0,
    },
    "draft": {
        "primary": "claude-sonnet",
        "fallback": ["claude-haiku"],
        "estimated_cost_per_1k": 0.003,
    },
    "judge": {
        "primary": "claude-opus",
        "fallback": ["claude-sonnet"],
        "estimated_cost_per_1k": 0.015,
    },
}


def catalog() -> dict:
    """Return the full task-type catalog (a copy)."""
    return {k: dict(v) for k, v in CATALOG.items()}


def select(task_type: str, budget: float = 0.0) -> dict:
    """Pick primary + fallback + estimated cost for a task_type.

    If budget > 0 and primary exceeds it, downgrade to the first fallback.
    """
    entry = CATALOG.get(task_type, CATALOG["reason"])
    result = {
        "primary": entry["primary"],
        "fallback": list(entry["fallback"]),
        "estimated_cost_per_1k": entry["estimated_cost_per_1k"],
    }
    if budget > 0.0 and result["estimated_cost_per_1k"] > budget and result["fallback"]:
        new_primary = result["fallback"][0]
        result["primary"] = new_primary
        result["fallback"] = result["fallback"][1:]
        # Downgraded tier; assume free unless explicitly cloud
        result["estimated_cost_per_1k"] = 0.0 if not new_primary.startswith("claude") else 0.003
    return result


def main() -> None:
    if "--task" not in sys.argv:
        sys.stderr.write("usage: llm_selector.py --task TYPE [--budget FLOAT]\n")
        sys.exit(2)
    task = sys.argv[sys.argv.index("--task") + 1]
    budget = 0.0
    if "--budget" in sys.argv:
        budget = float(sys.argv[sys.argv.index("--budget") + 1])
    import json
    sys.stdout.write(json.dumps(select(task, budget), indent=2))


if __name__ == "__main__":
    main()
