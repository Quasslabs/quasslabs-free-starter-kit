"""Tests for skill-linter."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from skill_linter import lint, check_header, check_sections


GOOD_SKILL = """# SKILL: example

**Bot:** any
**Role:** does things
**Ug-ug mode:** lite
**Model:** any
**Status:** stable
**Parallelizable:** yes

## When to invoke

triggers.

## Handoffs

none.
"""


def test_lint_clean_file_returns_no_issues(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text(GOOD_SKILL, encoding="utf-8")
    assert lint(str(p)) == []


def test_missing_file_returns_issue(tmp_path):
    issues = lint(str(tmp_path / "does-not-exist.md"))
    assert len(issues) == 1
    assert "not found" in issues[0]


def test_missing_header_field_detected():
    text = GOOD_SKILL.replace("**Status:** stable", "")
    issues = check_header(text)
    assert any("Status" in i for i in issues)


def test_missing_section_detected():
    text = GOOD_SKILL.replace("## Handoffs\n\nnone.\n", "")
    issues = check_sections(text)
    assert any("Handoffs" in i for i in issues)


def test_lint_flags_multiple_issues(tmp_path):
    bad = "# SKILL: x\n\n**Bot:** any\n"
    p = tmp_path / "SKILL.md"
    p.write_text(bad, encoding="utf-8")
    issues = lint(str(p))
    assert len(issues) >= 5
