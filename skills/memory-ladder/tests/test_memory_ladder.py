"""Tests for memory-ladder."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import memory_ladder  # noqa: E402


def test_load_missing_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert memory_ladder.load("nope") == {}


def test_save_then_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    memory_ladder.save("proj", {"goal": "ship it"})
    assert memory_ladder.load("proj") == {"goal": "ship it"}


def test_append_grows_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert memory_ladder.append("proj", "first") == 1
    assert memory_ladder.append("proj", "second") == 2
    assert memory_ladder.load("proj")["entries"] == ["first", "second"]


def test_memory_path_under_home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    p = memory_ladder.memory_path("x")
    assert p == tmp_path / ".memory" / "x.json"
