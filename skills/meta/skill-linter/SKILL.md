# SKILL: skill-linter

**Bot:** operator · any  
**Role:** Validates SKILL.md files against the required header format and section checklist. Flags missing fields, malformed ug-ug levels, missing Handoffs sections, and skills without Lambda candidates noted. Pure Python — no LLM needed. Run before promoting wip → ready.  
**Ug-ug mode:** full  
**Model:** haiku - deterministic build/deploy commands; no generation needed
**Tool compatibility:** Codex · Claude Code · Cursor · Cowork
**Status:** beta
**Parallelizable:** conditional - read-only lint is fully parallel; --report runs serialize on the single output file

---

## Model

**Verdict:** `none` — pure Python regex/string validation; no LLM needed, skip API cost.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | none | Pure Python; no AI involved |
| Local (installed) | none | Pure Python; runs without Ollama |
| Local (ideal) | none | Pure Python; no model needed |

---

## When to invoke

- Before promoting any skill from wip → ready
- "Check if this skill is properly formatted"
- "Lint all skills in wip/"
- After writing a new SKILL.md
- As part of reflect skill's Phase 5 gap check
- Automated: pre-commit hook or CI step on the skills hub

---

## Required SKILL.md format (what this linter enforces)

### Required header (lines 1–6):
```
# SKILL: [skill-name]
[blank line]
**Bot:** [bot-name]
**Role:** [one-line description]
**Ug-ug mode:** [none | lite | full | ultra]
**Tool compatibility:** [Claude Code · Cursor · Codex — at least one] · Cowork
```

### Required body sections (H2 headings):
- `## When to invoke` — trigger phrases + conditions
- `## Handoffs` — which bot/skill to call next, with exact paths

### Strongly recommended sections:
- `## Lambda candidates` OR a note inside another section flagging Lambda suitability
- Input/output spec (any heading works: `## Input spec`, `## Output`, etc.)
- Phased steps (when the skill has >2 steps)

### Ug-ug mode valid values:
`none` | `lite` | `full` | `ultra`

---

## Phase 1 — Run the linter

```bash
# Lint a single skill
python skills/skill-linter/lint_skill.py \
  "skills/bill-monitor/SKILL.md"

# Lint all skills in wip\
python skills/skill-linter/lint_skill.py --all \
  --root "skills/wip"

# Lint all skills and write report
python skills/skill-linter/lint_skill.py --all \
  --root "skills/wip" \
  --report "skills/LINT-REPORT.md"
```

---

## Phase 2 — Linter implementation

```python
# lint_skill.py

import re, sys, os, argparse
from pathlib import Path

VALID_UG-UG_LEVELS = {"none", "lite", "full", "ultra"}

REQUIRED_HEADERS = [
    ("# SKILL:",          r"^# SKILL:\s+\S+"),
    ("**Bot:**",          r"^\*\*Bot:\*\*\s+\S+"),
    ("**Role:**",         r"^\*\*Role:\*\*\s+\S+"),
    ("**Ug-ug mode:**", r"^\*\*Ug-ug mode:\*\*\s+\S+"),
    ("**Tool compatibility:**", r"^\*\*Tool compatibility:\*\*\s+\S+"),
]

REQUIRED_SECTIONS = ["## When to invoke", "## Handoffs"]
RECOMMENDED_SECTIONS = ["## Lambda candidates", "## Input spec", "## Output"]

def lint_file(path: Path) -> list[dict]:
    """Returns list of issues: [{level, field, message}]"""
    issues = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # --- Header checks ---
    for name, pattern in REQUIRED_HEADERS:
        found = any(re.match(pattern, line) for line in lines[:15])
        if not found:
            issues.append({"level": "ERROR", "field": name,
                           "message": f"Missing or malformed header: {name}"})

    # Ug-ug mode value check
    ug-ug_line = next((l for l in lines[:15] if "**Ug-ug mode:**" in l), None)
    if ug-ug_line:
        val = ug-ug_line.split("**Ug-ug mode:**")[-1].strip()
        if val not in VALID_UG-UG_LEVELS:
            issues.append({"level": "ERROR", "field": "**Ug-ug mode:**",
                           "message": f"Invalid ug-ug level '{val}'. Must be: none | lite | full | ultra"})

    # Tool compatibility — warn if empty
    tool_line = next((l for l in lines[:15] if "**Tool compatibility:**" in l), None) · Cowork
    if tool_line and len(tool_line.split("**Tool compatibility:**")[-1].strip()) < 3: · Cowork
        issues.append({"level": "WARN", "field": "**Tool compatibility:**", · Cowork
                       "message": "Tool compatibility appears empty — add at least one tool"})

    # --- Required sections ---
    for section in REQUIRED_SECTIONS:
        if section not in text:
            issues.append({"level": "ERROR", "field": section,
                           "message": f"Missing required section: {section}"})

    # --- Recommended sections ---
    for section in RECOMMENDED_SECTIONS:
        if section not in text:
            issues.append({"level": "WARN", "field": section,
                           "message": f"Recommended section missing: {section} (add or note Lambda suitability inline)"})

    # --- Handoffs content check ---
    if "## Handoffs" in text:
        handoff_block = text.split("## Handoffs")[-1][:500]
        if "SKILL.md" not in handoff_block and "|" not in handoff_block:
            issues.append({"level": "WARN", "field": "## Handoffs",
                           "message": "Handoffs section exists but appears empty — add at least one handoff with path"})

    # --- Blank line after header check ---
    if len(lines) > 1 and lines[1].strip():
        issues.append({"level": "WARN", "field": "blank line",
                       "message": "Line 2 should be blank (after # SKILL: heading)"})

    return issues

def format_issues(path: Path, issues: list[dict]) -> str:
    if not issues:
        return f"✅ {path.name} — PASS"
    errors = [i for i in issues if i["level"] == "ERROR"]
    warns  = [i for i in issues if i["level"] == "WARN"]
    lines  = [f"{'❌' if errors else '⚠️ '} {path.name}"]
    for i in errors:
        lines.append(f"  ERROR  [{i['field']}] {i['message']}")
    for i in warns:
        lines.append(f"  WARN   [{i['field']}] {i['message']}")
    return "\n".join(lines)

def find_all_skills(root: Path) -> list[Path]:
    return sorted(root.rglob("SKILL.md"))

def main():
    parser = argparse.ArgumentParser(description="Lint SKILL.md files")
    parser.add_argument("path", nargs="?", help="Path to a single SKILL.md")
    parser.add_argument("--all",  action="store_true", help="Lint all SKILL.md files under --root")
    parser.add_argument("--root", default=".", help="Root directory for --all scan")
    parser.add_argument("--report", help="Write markdown report to this path")
    args = parser.parse_args()

    if args.all:
        paths = find_all_skills(Path(args.root))
    elif args.path:
        paths = [Path(args.path)]
    else:
        parser.error("Provide a SKILL.md path or use --all")

    all_output = []
    error_count = warn_count = pass_count = 0

    for p in paths:
        issues = lint_file(p)
        output = format_issues(p, issues)
        all_output.append(output)
        print(output)
        if any(i["level"] == "ERROR" for i in issues):
            error_count += 1
        elif issues:
            warn_count += 1
        else:
            pass_count += 1

    summary = (f"\n{'='*50}\n"
               f"Skills checked: {len(paths)} | "
               f"Pass: {pass_count} | Warn: {warn_count} | Error: {error_count}")
    print(summary)

    if args.report:
        report_path = Path(args.report)
        report_path.write_text(
            "# Skill Lint Report\n\n```\n" + "\n".join(all_output) + summary + "\n```\n",
            encoding="utf-8"
        )
        print(f"\nReport written to: {args.report}")

    sys.exit(1 if error_count else 0)

if __name__ == "__main__":
    main()
```

---

## Output format

```
✅ bill-monitor/SKILL.md — PASS

❌ output-composer/SKILL.md
  ERROR  [**Ug-ug mode:**] Missing or malformed header: **Ug-ug mode:**
  WARN   [## Lambda candidates] Recommended section missing: ## Lambda candidates

⚠️  scope-master/screen-builder/SKILL.md
  WARN   [## Handoffs] Handoffs section exists but appears empty

==================================================
Skills checked: 42 | Pass: 38 | Warn: 3 | Error: 1
```

Exit code: `0` if no errors (warns OK), `1` if any errors.

---

## Pre-commit hook (optional)

Add to `skills/.git/hooks/pre-commit`:
```bash
#!/bin/bash
python wip/meta/skill-linter/lint_skill.py --all --root wip/
if [ $? -ne 0 ]; then
  echo "Skill lint failed — fix errors before committing"
  exit 1
fi
```

---

## Promotion gate

Before `wip → ready`:
```bash
python skills/skill-linter/lint_skill.py "skills/[skill]\SKILL.md"
# Must exit 0 (no errors)
```

---

## Lambda candidates

- Fully stateless, pure file I/O — strong Lambda candidate
- Pattern: API Gateway POST `{ "skill_path": "..." }` → Lambda lint_skill → returns JSON issues array
- Useful for: CI integration, GitHub Action on PR, or pre-deploy gate in deployer pipeline

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Bash | `python *lint_skill.py *` | Run the linter over one skill or the whole hub |
| Filesystem | `skills/**/SKILL.md` (read) | Read SKILL.md files to validate format |
| Filesystem | `skills/LINT-REPORT.md` (write) | Write the optional markdown lint report |

## Handoffs

| Next step | Skill |
|---|---|
| Sync inventory after linting | `skills/meta/claude-md-sync/SKILL.md` |
| Promote passing skills | Manual: move wip → ready |
| Build missing sections | Return to the skill and add them |
