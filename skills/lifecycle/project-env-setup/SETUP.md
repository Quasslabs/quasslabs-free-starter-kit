# SETUP: lifecycle/project-env-setup

**Skill:** `lifecycle/project-env-setup`
**Setup tier:** none
**Last verified:** 2026-05-31

No setup required — invoke directly. project-env-setup generates docker-compose.local.yml,
.env templates, and memory-config.yaml; file-writes only.

## Dependencies

stdlib only — no install. The files it generates require Docker for the local stack they describe.

## Credentials / vault
None. Generated .env templates have placeholder values; fill from vault at use time.

## How to run
```
Invoke skill: skills/lifecycle/project-env-setup/SKILL.md
```
Run after agent-setup-wizard for a new project. Outputs docker-compose.local.yml + .env.local.

## Verify it works
1. Invoke in a new project directory → docker-compose.local.yml + .env.local created.
