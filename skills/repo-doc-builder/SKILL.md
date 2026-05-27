# SKILL: repo-doc-builder

**Bot:** any
**Role:** (skill-specific - see body below)

**Namespace:** developer  
**Version:** 1.0.0  
**Model:** sonnet  
**Status:** beta
**Parallelizable:** yes - refine on next touch
**Ug-ug mode:** full (internal) · normal prose (generated docs)  
**Trigger phrases:** "generate repo docs", "build program docs", "document this repo", "repo map", "make process docs"

---


## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | (skill-specific - see Steps) | Per-skill read/write paths |
| Network | (skill-specific - see Steps) | Per-skill API calls |
| Bash | (skill-specific - see Steps) | Per-skill tools |

*Note: v2 backfill defaults 2026-05-20. Refine when skill is next edited.*



## When to invoke

- New GitHub repo needs onboarding docs (00-how-we-work.md + 01-repo-map.md)
- Repo doesn't have a current process docs setup
- "Generate process docs for this repo"

## Purpose

Scans a repository (local path or GitHub), classifies its type, and generates a set of process docs + a repo map that help both AI agents and humans get up to speed quickly. Output follows the AppsTango NestGenie process-doc standard: numbered markdown files with audience/purpose headers, ToC with anchor links, and no prose padding.

Docs are written with real content derived from the repo — not template stubs. Every section should be accurate to what's actually in the repo.

---

## Repo Types

| Type | Signals | Doc set |
|---|---|---|
| `skill-set` | `SKILL.md` files, `ready-for-review/` or `wip/` dirs | 00-how-we-work, 01-repo-map, 02-skill-lifecycle, 03-contributing, 04-license-guide |
| `bot-lambda` | Lambda handlers, `serverless.yml` or SAM template, no frontend | 00-how-we-work, 01-repo-map, 02-tech-stack, 03-deployment, 04-dev-setup, 05-testing |
| `bot-ecs` | Dockerfile, ECS task defs, no frontend | same as bot-lambda but deployment section differs |
| `full-stack` | Frontend + backend dirs, migrations, multiple runtimes | 00-how-we-work, 01-repo-map, 02-tech-stack, 03-deployment, 04-dev-setup, 05-testing, 06-contributing |
| `docs-only` | Mostly `.md`/`.html`, no source code | 00-how-we-work, 01-repo-map, 02-contributing |
| `library` | `package.json` / `setup.py` at root, no app runtime | 00-how-we-work, 01-repo-map, 02-dev-setup, 03-publishing |

---

## Inputs

- `repo_path` — local path to the repo root, OR
- `github_url` — `owner/repo` string (skill will read via `gh api`)
- `output_dir` — where to write docs (default: `{repo_path}/program-docs/`)
- `dry_run` — if true, show what would be generated without writing
- `overwrite` — if false (default), skip docs that already exist

---

## Phases

### Phase 1 — Orient

1. Identify input: local path exists? GitHub URL provided?
2. If GitHub-only: read structure via `gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1`
3. If local: use Glob to build a directory tree (max depth 4, exclude `node_modules`, `.git`, `dist`, `__pycache__`, `.next`)
4. Read key files that exist: `README.md`, `CLAUDE.md`, `AGENTS.md`, `package.json`, `requirements.txt`, `serverless.yml`, `terraform/`, `Dockerfile`, `LICENSE`

### Phase 2 — Classify

Apply the repo type signals table above. Output one of: `skill-set | bot-lambda | bot-ecs | full-stack | docs-only | library`

Emit: `REPO TYPE: {type}` before proceeding.

### Phase 3 — Scan (type-specific)

**For all types:**
- Directory tree (3 levels, annotated)
- Languages detected (by extension counts)
- Existing docs (any `.md` files in `program-docs/`, `_context/`, `docs/`)
- License file present?

**For skill-set:**
- List all skill names and their triad completeness (SKILL.md ✓ FUNCTIONS.md ✓ LESSONS.md ✓/✗)
- Count skills by lifecycle stage (wip / ready-for-review / live / kits)
- Detect any namespace SKILL.md files (routing skill)

**For bot-lambda / bot-ecs:**
- Entry points (handler files, Lambda function names)
- External APIs called (grep for `fetch`, `axios`, `requests.get`, `boto3`, endpoint URLs)
- Environment variables referenced (grep `process.env.`, `os.environ`)
- AWS services used (grep for `DynamoDB`, `S3`, `SQS`, `SNS`, `Bedrock`, `Lambda`)
- Test framework (jest, pytest, mocha)
- Deploy method (SAM, Serverless Framework, CDK, Terraform, manual)

**For full-stack:**
- Frontend stack (Next.js, React, Vue — from package.json)
- Backend stack (Express, NestJS, FastAPI — from package.json / requirements)
- Database (Postgres, DynamoDB, SQLite — from config/env)
- Deploy targets (frontend: S3/CloudFront/Vercel; backend: ECS/Lambda/EC2)
- Migration system (Knex, Alembic, Prisma)
- Auth system (Cognito, Auth0, JWT homebrew)

**For docs-only:**
- Doc categories present (by top-level dirs)
- Format mix (md / html / pdf)
- Any audience indicators in existing docs

### Phase 4 — Gap Check

For each doc in the target doc set:
- Check if it exists at `{output_dir}/NN-{slug}.md`
- If yes and `overwrite=false`: skip, note as "EXISTS"
- If yes and `overwrite=true`: mark as "OVERWRITE"
- If no: mark as "GENERATE"

Print a gap report table:

```
| Doc | Status |
|---|---|
| 00-how-we-work.md | GENERATE |
| 01-repo-map.md | GENERATE |
| 02-skill-lifecycle.md | GENERATE |
```

### Phase 5 — Generate Docs

For each doc marked GENERATE (or OVERWRITE):

Generate the full markdown content based on the template for that doc type and the scan data from Phase 3. Do NOT write template stubs — every section must contain real information from the repo.

**Universal doc header format:**
```
# NN — Title: Subtitle

**Audience:** {who reads this}
**Purpose:** {one-sentence purpose}

---

## Table of Contents
...
```

**Universal footer:**
```
*Last updated: YYYY-MM-DD · AppsTango · {project name}*
```

See **Doc Templates** section below for section-by-section guidance per doc type.

### Phase 6 — Write

For each generated doc:
1. Create `{output_dir}/` if it doesn't exist
2. Write the file
3. Confirm: `Written: {output_dir}/{filename}` (N lines)

If `dry_run=true`: print the generated content to stdout, do not write files.

### Phase 7 — Commit (optional)

If the repo is a git repo and the user confirms:
```bash
cd {repo_path}
git add program-docs/
git commit -m "docs: add program-docs via repo-doc-builder"
git push
```

---

## Doc Templates

### 00 — how-we-work.md

Sections:
1. **What this repo is** — 2-3 sentence description (from README/CLAUDE.md)
2. **Session structure** — plan → execute → review; how to pick up where you left off
3. **Task split** — table of what Taylor does vs what Claude Code does (repo-specific actions)
4. **Tools used** — table of CLI tools, APIs, services in this repo
5. **Credentials** — where they live (KeePass vault, env vars, AWS profiles)
6. **Context handoff** — which files to read when resuming a session (CLAUDE.md, OPEN-ITEMS.md, plan file)
7. **Key files to read when starting** — table: file → why
8. **Template prompts for recurring tasks** — 3-5 copy-pasteable prompt blocks for the most common tasks on this repo

### 01 — repo-map.md

Sections:
1. **Top-level structure** — annotated directory tree (3 levels)
2. **Key files** — table: file path → purpose → read-first priority (high/medium/low)
3. **Entry points** — for bots: handler files; for skill-sets: namespace SKILL.md; for full-stack: main server file + frontend entry
4. **What to ignore** — auto-generated dirs, build artifacts, lock files

For skill-set repos, add:
5. **Skill index** — table of all skills with: name | stage | role | trigger phrase | triad complete

### 02 (skill-set) — skill-lifecycle.md

Sections:
1. **Stages** — wip → ready-for-review → live pipeline
2. **What each stage means** — quality bar, audience, distribution rules
3. **Promotion criteria** — what it takes to move from wip to ready-for-review
4. **Skill triad** — SKILL.md + FUNCTIONS.md + LESSONS.md (what each file must contain)
5. **Naming conventions** — directory names, trigger phrases
6. **Kits** — what a kit is, how it differs from a standalone skill

### 02 (bot-lambda/ecs) — tech-stack.md

Sections:
1. **Runtime** — language + version
2. **Key dependencies** — top 10 from package.json/requirements.txt with purpose
3. **AI integration** — model(s) used, routing logic, fallback behavior
4. **Data storage** — databases, caches, S3 buckets
5. **External APIs** — list with auth method
6. **AWS services** — list with purpose
7. **Why these choices** — any documented ADR decisions

### 03 (skill-set) — contributing.md

Sections:
1. **How to add a new skill** — step by step (use skillmaster, build triad, lint, promote)
2. **Skill file requirements** — what SKILL.md must contain (title, trigger phrases, phases, handoffs)
3. **FUNCTIONS.md requirements** — pure functions, AI steps, external services
4. **LESSONS.md requirements** — corrections from production use
5. **Naming rules** — kebab-case, descriptive, no generic names
6. **Lint rules** — what skill-linter checks
7. **Review checklist** — before promoting to ready-for-review

### 03 (bot) — deployment.md

Sections:
1. **Architecture overview** — 1-para summary + component diagram (text-based)
2. **Environments** — dev / staging / prod and what differs
3. **Deploy method** — exact commands or AWS console steps
4. **Environment variables** — table: var → required → description → where it's set
5. **Post-deploy verification** — how to confirm it's working
6. **Rollback** — how to revert a bad deploy

### 04 (bot) — dev-setup.md

Sections:
1. **Prerequisites** — tools + versions table
2. **Quick start** — numbered steps to get running locally
3. **Environment file** — which vars are needed locally, what can be stubbed
4. **Running locally** — exact commands
5. **Testing locally** — exact test commands
6. **Common gotchas** — numbered list of hard-won lessons

---

## Handoffs

- After generating docs: optionally invoke `commit-and-push` or the user does it manually
- If the repo has a CLAUDE.md: update the "Supporting context files" section to reference `program-docs/NN-*.md`
- If the repo is in the skills hub: run `claude-md-sync` to register the new skill

---

## Lambda candidates

- `classify_repo_type(tree_json, key_files_content)` → `{type, signals, confidence}`
- `generate_skill_index(skill_dirs, triad_status)` → markdown skill index table
- `annotate_directory_tree(raw_tree, type_hints)` → annotated tree markdown
