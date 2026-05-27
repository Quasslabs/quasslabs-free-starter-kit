# FUNCTIONS: repo-doc-builder

---

## Pure Functions (Lambda-ready)

### `classify_repo_type(tree_paths, key_files)`
- **Input:** `tree_paths: list[str]`, `key_files: dict[str, str]` (filename → content snippet)
- **Output:** `{type: str, signals: list[str], confidence: "high"|"medium"|"low"}`
- **Logic:**
  - `skill-set` → any path matches `*/SKILL.md` AND (`wip/` OR `ready-for-review/` in tree)
  - `bot-lambda` → `serverless.yml` OR `handler.py` OR `lambda_function.py` OR `template.yaml` (SAM)
  - `bot-ecs` → `Dockerfile` AND (`ecs-task-def.json` OR `docker-compose.yml`) AND no frontend dir
  - `full-stack` → dirs named `frontend`/`client`/`web` AND dirs named `backend`/`api`/`server`
  - `docs-only` → >80% of files are `.md`/`.html`/`.pdf`, no `.py`/`.ts`/`.js` source
  - `library` → `package.json` OR `setup.py` at root AND no app runtime files

### `detect_tech_stack(tree_paths, file_contents)`
- **Input:** `tree_paths: list[str]`, `file_contents: dict[str, str]`
- **Output:** `{languages: list[str], frameworks: list[str], databases: list[str], deploy: list[str], ai_services: list[str]}`
- **Logic:**
  - Languages: count extensions (`.ts`, `.py`, `.js`, `.rb`, etc.), report top 3
  - Frameworks: grep `package.json` for known names; grep `requirements.txt` for known packages
  - Databases: grep for `DynamoDB`, `postgres`, `sqlite`, `mysql`, `MongoDB`, `Prisma`, `knex`, `alembic`
  - Deploy: detect `serverless.yml` → Serverless; `template.yaml` → SAM; `cdk.json` → CDK; `Dockerfile` → container; `.github/workflows/` → GHA
  - AI: grep for `anthropic`, `openai`, `bedrock`, `ollama`, `claude`, `gpt`, `gemini`

### `scan_skill_triads(skill_dirs)`
- **Input:** `skill_dirs: list[str]` (paths to skill folders)
- **Output:** `list[{name, has_skill_md, has_functions_md, has_lessons_md, stage, trigger_phrases}]`
- **Logic:**
  - For each dir: check existence of `SKILL.md`, `FUNCTIONS.md`, `LESSONS.md`
  - Extract trigger phrases by grepping `SKILL.md` for `trigger phrases:` line
  - Stage: derived from parent dir name (`wip` / `ready-for-review` / `kits` / `live`)

### `build_annotated_tree(tree_paths, annotations)`
- **Input:** `tree_paths: list[str]`, `annotations: dict[str, str]` (path → description)
- **Output:** `str` — markdown code block with indented tree and inline annotations
- **Logic:**
  - Collapse deep paths (>3 levels) to `...`
  - Right-align annotations with `←` separator
  - Skip: `node_modules/`, `__pycache__/`, `.git/`, `dist/`, `.next/`, `*.lock`

### `extract_env_vars(source_dirs)`
- **Input:** `source_dirs: list[str]`
- **Output:** `list[{name, description, required, example}]`
- **Logic:**
  - Grep `.ts`/`.py`/`.js` files for `process.env.VAR`, `os.environ["VAR"]`, `os.getenv("VAR")`
  - Grep `.env.example` if present — extract var names and comments
  - Deduplicate; sort alphabetically

### `extract_external_apis(source_dirs)`
- **Input:** `source_dirs: list[str]`
- **Output:** `list[{service, endpoint_pattern, auth_method}]`
- **Logic:**
  - Grep for known service patterns: `api.anthropic.com`, `api.openai.com`, `api.fathomhq.com`, `atlassian.net`, `api.twilio.com`, `sendgrid`, `stripe.com`
  - Grep for `fetch(`, `axios.`, `requests.get(`, `http.get(` with URL strings
  - Infer auth method from context (Bearer, API key, OAuth)

---

## AI Steps (run by Claude Code, not Lambda)

### `generate_how_we_work(repo_type, scan_data, project_name)`
- Claude reads scan_data and writes a full `00-how-we-work.md`
- Must include real recurring task prompts specific to this repo
- No template stubs — every prompt should be copy-pasteable

### `generate_repo_map(tree, repo_type, skill_index)`
- Claude writes `01-repo-map.md` from annotated tree + detected entry points
- For skill-set: include skill index table
- Annotate each top-level dir with 1-line purpose

### `generate_contributing_guide(repo_type, scan_data)`
- Claude writes a `02-contributing.md` or `03-contributing.md` depending on slot
- Content: exact commands, file requirements, checklist items — no vague guidance

### `generate_deployment_doc(tech_stack, env_vars, aws_services)`
- Claude writes a deployment doc with exact CLI commands, not placeholders
- Include actual Lambda function names / ECS cluster names if detectable from code

---

## External Services / CLI

| Service | Purpose | Auth method |
|---|---|---|
| `gh` CLI | Read GitHub repo structure when no local clone | `gh auth` (TQuass account) |
| `git` | Commit and push generated docs | existing remote auth |
| Glob / Grep tools | Local file scanning | native |
| `skill-linter` | Validate generated SKILL.md when skill-builder mode is on | Python script at `skills/meta/skill-linter/lint_skill.py` |
