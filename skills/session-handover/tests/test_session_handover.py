"""Tests for session-handover."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import session_handover as sh  # noqa: E402


def test_write_handover_creates_file(tmp_path):
    out = tmp_path / "HANDOVER.md"
    result = sh.write_handover(str(out), {"bot": "x", "project": "p",
                                          "next_action": "do thing"})
    assert out.exists()
    assert result["written"] is True
    text = out.read_text(encoding="utf-8")
    assert "Session Handover" in text
    assert "do thing" in text


def test_render_handover_includes_decisions_and_files():
    text = sh.render_handover({
        "decisions": [{"decision": "use SQLite", "reason": "single-file portability"}],
        "files_modified": [{"path": "src/app.py", "change": "added auth"}],
    })
    assert "use SQLite" in text
    assert "src/app.py" in text


def test_generate_session_opener_uses_next_action():
    opener = sh.generate_session_opener({"bot": "B", "project": "P",
                                         "next_action": "run tests",
                                         "completed": ["a", "b"]})
    assert "run tests" in opener
    assert "P" in opener


def test_write_handover_creates_parent_dirs(tmp_path):
    out = tmp_path / "nested" / "dir" / "HANDOVER.md"
    sh.write_handover(str(out), {"bot": "x", "project": "p"})
    assert out.exists()
