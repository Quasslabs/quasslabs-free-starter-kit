"""Tests for ug-ug compressor."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ug_ug import compress_text, strip_banned_openers


def test_banned_opener_removed():
    assert "Let me explain" not in compress_text("Let me explain how this works.", level="full")


def test_none_level_is_passthrough():
    text = "Let me explain how this works."
    assert compress_text(text, level="none") == text


def test_filler_stripped_at_full():
    out = compress_text("This is just a simple test.", level="full")
    assert "just" not in out
    assert "simple" in out


def test_multi_newline_collapsed_at_full():
    out = compress_text("a\n\n\n\nb", level="full")
    assert out.count("\n") <= 2


def test_strip_banned_openers_idempotent():
    once = strip_banned_openers("Sure! here we go")
    twice = strip_banned_openers(once)
    assert once == twice
