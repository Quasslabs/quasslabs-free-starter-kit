"""notify — Telegram alert primitive. Three levels: red_gate, report, checkpoint."""
from __future__ import annotations

import os
import sys
from typing import Optional

import requests

TELEGRAM_API = "https://api.telegram.org"
VALID_LEVELS = {"red_gate", "report", "checkpoint"}


def format_red_gate(task: str, blocker: str, action: str) -> str:
    return (
        f"*BLOCKER -- {task}*\n\n"
        f"Cannot proceed without:\n- {blocker}\n\n"
        f"*What to do:*\n{action}\n\n"
        "Reply *DONE* when complete or *SKIP* to continue without."
    )


def format_report(title: str, body: str) -> str:
    return f"*{title}*\n\n{body}"


def format_checkpoint(task: str, question: str, options: Optional[list] = None) -> str:
    opts = ""
    if options:
        opts = "\n" + "\n".join(f"  {i+1}. {o}" for i, o in enumerate(options))
    return (
        f"*CHECKPOINT -- {task}*\n\n"
        f"{question}{opts}\n\n"
        "Reply with your choice or any instruction to continue."
    )


def send(level: str, message: str) -> dict:
    """POST a formatted message to Telegram. Returns delivery status."""
    if level not in VALID_LEVELS:
        return {"status": "error", "level": level, "delivered": False,
                "error": f"invalid level: {level}"}
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return {"status": "error", "level": level, "delivered": False,
                "error": "missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}
    try:
        resp = requests.post(
            f"{TELEGRAM_API}/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=10,
        )
        ok = resp.status_code == 200
        return {"status": "ok" if ok else "error", "level": level,
                "delivered": ok, "error": None if ok else f"http {resp.status_code}"}
    except Exception as e:
        return {"status": "error", "level": level, "delivered": False, "error": str(e)}


def main() -> None:
    level = "report"
    message = "notify ready"
    if "--level" in sys.argv:
        level = sys.argv[sys.argv.index("--level") + 1]
    if "--message" in sys.argv:
        message = sys.argv[sys.argv.index("--message") + 1]
    result = send(level, message)
    sys.stdout.write(str(result) + "\n")


if __name__ == "__main__":
    main()
