"""memory-ladder — file-based per-slug cross-session memory."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def memory_path(slug: str) -> Path:
    """Resolve the JSON file path for a given slug."""
    return Path.home() / ".memory" / f"{slug}.json"


def load(slug: str) -> dict:
    """Load payload for slug. Returns empty dict if file missing."""
    p = memory_path(slug)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save(slug: str, payload: dict) -> Path:
    """Write full payload to slug file. Creates parent dir."""
    p = memory_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return p


def append(slug: str, entry: Any) -> int:
    """Append entry to payload['entries']. Returns new length."""
    payload = load(slug)
    entries = payload.setdefault("entries", [])
    entries.append(entry)
    save(slug, payload)
    return len(entries)


def main() -> None:
    if "--slug" not in sys.argv:
        sys.stderr.write("usage: memory_ladder.py --slug NAME [--append TEXT | --load]\n")
        sys.exit(2)
    slug = sys.argv[sys.argv.index("--slug") + 1]
    if "--append" in sys.argv:
        text = sys.argv[sys.argv.index("--append") + 1]
        n = append(slug, text)
        sys.stdout.write(f"appended (entries={n})\n")
    else:
        sys.stdout.write(json.dumps(load(slug), indent=2))


if __name__ == "__main__":
    main()
