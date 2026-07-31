"""skill-linter — slim SKILL.md validator.

Checks required header fields and required body sections.
The full hub linter is a separate tool with more strict-commercial checks.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_HEADER_FIELDS = [
    "Bot",
    "Role",
    "Ug-ug mode",
    "Model",
    "Status",
    "Parallelizable",
]

REQUIRED_SECTIONS = [
    "## When to invoke",
    "## Handoffs",
]


def check_header(text: str) -> list[str]:
    """Return list of missing header fields."""
    issues: list[str] = []
    # Only inspect the first ~30 lines for header fields
    head = "\n".join(text.splitlines()[:30])
    for field in REQUIRED_HEADER_FIELDS:
        pattern = re.compile(rf"^\*\*{re.escape(field)}:\*\*", re.MULTILINE)
        if not pattern.search(head):
            issues.append(f"missing header field: {field}")
    return issues


def check_sections(text: str) -> list[str]:
    """Return list of missing required sections."""
    issues: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in text:
            issues.append(f"missing section: {section}")
    return issues


def lint(path: str) -> list[str]:
    """Lint a SKILL.md file at `path`. Return list of issues."""
    p = Path(path)
    if not p.exists():
        return [f"file not found: {path}"]
    if not p.is_file():
        return [f"not a file: {path}"]
    text = p.read_text(encoding="utf-8")
    return check_header(text) + check_sections(text)


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: skill_linter <path-to-SKILL.md>\n")
        sys.exit(2)
    path = sys.argv[1]
    issues = lint(path)
    if not issues:
        print(f"PASS: {path}")
        sys.exit(0)
    print(f"FAIL: {path}")
    for issue in issues:
        print(f"  - {issue}")
    sys.exit(1)


if __name__ == "__main__":
    main()
