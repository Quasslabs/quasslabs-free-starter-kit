"""ug-ug output-mode transformer. Rule-based, no LLM."""
from __future__ import annotations

import re
import sys

BANNED_OPENERS = [
    r"^let me\b", r"^i'll go ahead\b", r"^i need to\b",
    r"^certainly[!\.]", r"^sure[!\.]", r"^great[!\.]", r"^of course\b",
    r"^i'll now\b", r"^also need to\b", r"^in order to\b",
    r"^this will\b", r"^let me explain\b",
]
BANNED_RX = re.compile("|".join(BANNED_OPENERS), re.IGNORECASE | re.MULTILINE)

FILLER_RX = re.compile(r"\b(just|simply|basically|essentially|actually|really)\s+", re.IGNORECASE)


def strip_banned_openers(text: str) -> str:
    """Remove the BANNED opener and any trailing space/comma."""
    return BANNED_RX.sub("", text).lstrip()


def _strip_filler(text: str) -> str:
    return FILLER_RX.sub("", text)


def compress_text(text: str, level: str = "full") -> str:
    """Apply level-appropriate compression."""
    if level == "none":
        return text
    out = strip_banned_openers(text)
    if level in ("lite", "medium", "full", "extra-ug", "maximum-ug"):
        out = _strip_filler(out)
    if level in ("full", "extra-ug", "maximum-ug"):
        out = re.sub(r"\n{3,}", "\n\n", out)
        out = re.sub(r"[ \t]{2,}", " ", out)
    return out


def main() -> None:
    level = "full"
    if "--level" in sys.argv:
        level = sys.argv[sys.argv.index("--level") + 1]
    text = sys.stdin.read()
    sys.stdout.write(compress_text(text, level=level))


if __name__ == "__main__":
    main()
