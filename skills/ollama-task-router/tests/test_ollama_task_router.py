"""Tests for ollama-task-router."""
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KIT / "lib"))
sys.path.insert(0, str(KIT / "skills" / "ollama-task-router" / "src"))

import _lib_llm  # noqa: E402
import ollama_task_router  # noqa: E402


def test_build_prompt_contains_task():
    p = ollama_task_router.build_prompt("classify an email")
    assert "classify an email" in p
    assert "JSON" in p


def test_route_local_response(monkeypatch):
    monkeypatch.setattr(
        _lib_llm, "call_llm_json",
        lambda prompt, model=None: {
            "target": "local", "model": "phi4-mini", "reason": "classification"
        },
    )
    monkeypatch.setattr(
        ollama_task_router, "call_llm_json", _lib_llm.call_llm_json
    )
    r = ollama_task_router.route("classify this")
    assert r["target"] == "local"
    assert r["model"] == "phi4-mini"


def test_route_cloud_response(monkeypatch):
    monkeypatch.setattr(
        ollama_task_router, "call_llm_json",
        lambda prompt, model=None: {
            "target": "cloud", "model": "claude-opus", "reason": "high-stakes"
        },
    )
    r = ollama_task_router.route("decide on architecture")
    assert r["target"] == "cloud"
    assert r["model"] == "claude-opus"


def test_route_fills_defaults_on_missing_keys(monkeypatch):
    monkeypatch.setattr(
        ollama_task_router, "call_llm_json",
        lambda prompt, model=None: {},
    )
    r = ollama_task_router.route("anything")
    assert set(r.keys()) == {"target", "model", "reason"}
