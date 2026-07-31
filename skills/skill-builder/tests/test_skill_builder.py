"""Tests for skill-builder."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from skill_builder import draft_skill, suggest_layout, REQUIRED_FILES


def test_draft_returns_required_keys():
    h = draft_skill("My New Skill", "Does X")
    for key in ("name", "bot", "role", "ug_ug_mode", "status", "license", "tier"):
        assert key in h


def test_slug_is_kebab_case():
    h = draft_skill("My New Skill", "Does X")
    assert h["name"] == "my-new-skill"


def test_role_passed_through():
    h = draft_skill("foo", "Does Y for Z")
    assert h["role"] == "Does Y for Z"


def test_layout_includes_all_required():
    files = suggest_layout("foo-bar")
    for req in REQUIRED_FILES:
        assert req in files


def test_layout_includes_slash_command_file():
    files = suggest_layout("foo-bar")
    assert "commands/foo-bar.toml" in files
    assert "src/foo_bar.py" in files
    assert "tests/test_foo_bar.py" in files
