"""Tests for llm-selector."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from llm_selector import select, catalog  # noqa: E402


def test_classify_picks_local():
    r = select("classify")
    assert r["primary"] == "phi4-mini"
    assert r["estimated_cost_per_1k"] == 0.0


def test_code_picks_qwen():
    assert select("code")["primary"] == "qwen2.5-coder:7b"


def test_draft_is_cloud_with_cost():
    r = select("draft")
    assert r["primary"].startswith("claude")
    assert r["estimated_cost_per_1k"] > 0.0


def test_unknown_falls_back_to_reason():
    r = select("nonsense-task-type")
    assert r["primary"] == catalog()["reason"]["primary"]


def test_budget_downgrades_judge():
    r = select("judge", budget=0.005)
    assert r["primary"] == "claude-sonnet"  # first fallback
