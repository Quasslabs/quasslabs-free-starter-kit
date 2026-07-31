"""ollama-task-router — classify a task as local-Ollama or cloud."""
from __future__ import annotations

import sys
from pathlib import Path

# Make kit-level lib/ importable
_KIT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_KIT / "lib"))

from _lib_llm import call_llm_json  # noqa: E402


SCHEMA_HINT = (
    '{"target": "local" or "cloud",'
    ' "model": "model id like phi4-mini or claude-sonnet",'
    ' "reason": "one short sentence"}'
)


def build_prompt(task: str) -> str:
    """Construct the JSON-mode classifier prompt."""
    return (
        "Classify this task as best-run on a LOCAL Ollama model or a paid CLOUD API.\n"
        "Local-eligible: classify, extract, route, code gen, multi-step reasoning.\n"
        "Cloud-required: long-form narrative draft, high-stakes judgment.\n"
        f"Task: {task}\n"
        f"Reply as JSON matching this shape: {SCHEMA_HINT}"
    )


def route(task: str) -> dict:
    """Return routing decision: {target, model, reason}."""
    raw = call_llm_json(build_prompt(task), model="phi4-mini")
    return {
        "target": raw.get("target", "local"),
        "model": raw.get("model", "phi4-mini"),
        "reason": raw.get("reason", ""),
    }


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: ollama_task_router.py <task>\n")
        sys.exit(2)
    import json
    sys.stdout.write(json.dumps(route(" ".join(sys.argv[1:])), indent=2))


if __name__ == "__main__":
    main()
