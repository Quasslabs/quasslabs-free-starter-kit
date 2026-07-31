"""Tests for task-router."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from task_router import evaluate, find_red_gates, find_yellow_notes  # noqa: E402


def test_clean_task_has_no_gates():
    result = evaluate("write a hello world function")
    assert result["red_gates"] == []
    assert result["yellow_notes"] == []


def test_api_key_triggers_red():
    assert find_red_gates("need an API key for stripe") != []


def test_force_push_triggers_red():
    assert find_red_gates("force-push the rebase") != []


def test_todo_triggers_yellow():
    assert find_yellow_notes("TODO: handle edge case") != []


def test_evaluate_returns_full_schema():
    r = evaluate("anything")
    assert set(r.keys()) == {"red_gates", "yellow_notes", "estimated_cost", "recommended_skill"}
    assert r["estimated_cost"] == 0.0
