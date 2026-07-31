"""Tests for operator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from operator_skill import route


def test_route_lint_matches_linter():
    r = route("please lint this SKILL.md")
    assert r["skill"] == "skill-linter"


def test_route_draft_matches_builder():
    r = route("draft skill for X")
    assert r["skill"] == "skill-builder"


def test_route_compress_matches_ug_ug():
    r = route("compress this output please")
    assert r["skill"] == "ug-ug"


def test_route_no_match_returns_none():
    r = route("buy me a sandwich")
    assert r["skill"] is None
    assert "no keyword match" in r["reason"]


def test_route_empty_returns_none():
    r = route("")
    assert r["skill"] is None
