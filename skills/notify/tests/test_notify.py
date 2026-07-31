"""Tests for notify."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import notify  # noqa: E402


class _FakeResp:
    def __init__(self, code=200):
        self.status_code = code


def test_format_red_gate_includes_task_and_blocker():
    out = notify.format_red_gate("deploy", "missing key", "set env var")
    assert "deploy" in out
    assert "missing key" in out
    assert "DONE" in out


def test_format_checkpoint_numbers_options():
    out = notify.format_checkpoint("merge", "which branch?", ["main", "dev"])
    assert "1. main" in out
    assert "2. dev" in out


def test_send_rejects_invalid_level():
    result = notify.send("bogus", "hi")
    assert result["status"] == "error"
    assert result["delivered"] is False


def test_send_missing_env_returns_error(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    result = notify.send("report", "hi")
    assert result["status"] == "error"
    assert "missing" in result["error"]


def test_send_success(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    monkeypatch.setattr(notify.requests, "post", lambda *a, **k: _FakeResp(200))
    result = notify.send("report", "hi")
    assert result["status"] == "ok"
    assert result["delivered"] is True
