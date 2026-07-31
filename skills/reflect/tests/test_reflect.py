"""Tests for reflect."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import reflect  # noqa: E402


def test_reflect_creates_lessons_md(tmp_path):
    result = reflect.reflect(str(tmp_path), entry="worked: X", project="proj")
    lessons = tmp_path / "_context" / "LESSONS.md"
    assert lessons.exists()
    assert "Retro -- proj" in lessons.read_text(encoding="utf-8")
    assert result["appended"] is True


def test_reflect_appends_not_overwrites(tmp_path):
    reflect.reflect(str(tmp_path), entry="first", project="p")
    reflect.reflect(str(tmp_path), entry="second", project="p")
    text = (tmp_path / "_context" / "LESSONS.md").read_text(encoding="utf-8")
    assert "first" in text
    assert "second" in text


def test_format_retro_includes_date():
    out = reflect.format_retro("proj", "body text", "2026-06-11")
    assert "2026-06-11" in out
    assert "body text" in out


def test_reflect_returns_iso_date(tmp_path):
    result = reflect.reflect(str(tmp_path), entry="x", project="p", when="2026-06-11")
    assert result["date"] == "2026-06-11"
