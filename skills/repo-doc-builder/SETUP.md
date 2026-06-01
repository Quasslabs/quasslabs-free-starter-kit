# SETUP: repo-doc-builder

**Skill:** `repo-doc-builder`
**Setup tier:** light
**Last verified:** 2026-05-31

## Dependencies

| Dep | Install | Notes |
|---|---|---|
| git | present | repo history + structure scan |
| GitHub CLI | `gh` — install from https://cli.github.com | Push generated docs, PR creation |

## Credentials / vault

| Secret | Where | How used |
|---|---|---|
| GitHub token | `gh auth login` | Push commits + open PRs |

## How to run

```
Invoke skill: skills/repo-doc-builder/SKILL.md
```
Provide: GitHub repo URL → scans structure → writes 00-how-we-work + 01-repo-map + 02-skill-lifecycle docs → commits + pushes.

## Verify it works

1. `gh auth status` → authenticated.
2. Invoke on a small repo → at least one `00-*.md` doc created and committed.
