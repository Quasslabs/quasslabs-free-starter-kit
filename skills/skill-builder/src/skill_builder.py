"""skill-builder — draft a SKILL.md header stub and folder layout."""
from __future__ import annotations

import sys


REQUIRED_FILES = [
    "SKILL.md",
    "FUNCTIONS.md",
    "LESSONS.md",
    "INSTALL.md",
    "SETUP.md",
    "REPORT.md",
    "manifest.json",
]


def _slugify(name: str) -> str:
    out = []
    for ch in name.strip().lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "_", "-", "/"):
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def draft_skill(name: str, role: str) -> dict:
    """Return a SKILL.md header dict (schema v2.1)."""
    slug = _slugify(name)
    return {
        "name": slug,
        "bot": "any",
        "role": role,
        "ug_ug_mode": "lite",
        "model": "any",
        "tool_compatibility": "Claude Code",
        "status": "draft",
        "parallelizable": "yes",
        "license": "mit",
        "origin": "original",
        "pack": "core",
        "commercial": "needs-review",
        "tier": "free",
    }


def suggest_layout(name: str) -> list[str]:
    """Return list of files that should exist for the skill folder."""
    slug = _slugify(name)
    return REQUIRED_FILES + [
        f"commands/{slug}.toml",
        f"src/{slug.replace('-', '_')}.py",
        f"tests/test_{slug.replace('-', '_')}.py",
    ]


def main() -> None:
    if len(sys.argv) < 3:
        sys.stderr.write("usage: skill_builder <name> <role>\n")
        sys.exit(2)
    name, role = sys.argv[1], sys.argv[2]
    header = draft_skill(name, role)
    layout = suggest_layout(name)
    print(f"slug: {header['name']}")
    for k, v in header.items():
        if k == "name":
            continue
        print(f"{k}: {v}")
    print("files:")
    for f in layout:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
