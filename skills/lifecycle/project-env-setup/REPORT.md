# REPORT: lifecycle/project-env-setup

**Skill:** `lifecycle/project-env-setup` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Time to local stack bootstrap | 30–60 min | < 5 min | Timed |
| Manual config steps | 10+ | 1 (invoke the skill) | Step count |
| Missing .env / compose errors at day 1 | Common | Rare | Dev feedback |

## Who gets the most value

Developers starting a new project who want a local Postgres + Redis + service stack running in minutes, not an afternoon.

## How it fits in a flow

**Upstream:** `agent-setup-wizard` completes → **project-env-setup** → docker-compose.local.yml + .env.local → `docker compose up`

## Skill interactions

| Pairs with | How |
|---|---|
| `lifecycle/agent-setup-wizard` | wizard generates CLAUDE.md; env-setup adds the local Docker layer |

## Measured outcomes

- Bootstrap time cut from 30–60 min to under 5 min.
- Eliminates "I forgot to add the env template" onboarding gap.

## Test coverage

1. Invoke in a new project directory → docker-compose.local.yml + .env.local created.
2. `docker compose -f docker-compose.local.yml up -d` → services start without errors.
