# SKILL: chat-primer

**Bot:** any  
**Role:** "Session ready" ritual for any new chat. Auto-wires memory (via memory/recommender) and token-saving MCP servers (token-savior-mcp + context-mode) on first session per project. Idempotent — no-op when already configured. Confirms ug-ug ultra, verifies vault + Ollama, scaffolds missing reference files, flags drift + fine-tune candidates. Outputs a compact SESSION READY card showing what was auto-wired this session.  
**Ug-ug mode:** full  
**Model:** haiku — deterministic file reads + availability checks; delegates strategy steps to memory/recommender  
**Tool compatibility:** Claude Code · Cursor · Codex  
**Origin:** Internal — companion to agent-setup-wizard and session-handover
**Status:** beta
**Parallelizable:** no — writes per-project state (.mcp.json, memory-config.yaml, MEMORY.md); concurrent runs on the same project would race

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<project>/.mcp.json` | Write/merge MCP server config (Phase 4) |
| Filesystem | `<project>/_context/memory-config.yaml` | Write memory backend choice (Phase 5) |
| Filesystem | `<project>/_context/auto-wire.log` | Audit trail of what was auto-wired this session |
| Filesystem | `<project>/MEMORY.md`, `<project>/HANDOVER.md` | Seed on first session |
| Filesystem | `<project>/CLAUDE.md`, `<project>/_references.md`, `<project>/_context/*` | Read project signals |
| Filesystem | `~/.claude/projects/<slug>/memory/MEMORY.md` | Hydrate per-project memory index |
| Network | `http://localhost:11434/api/tags` | Phase 7 Ollama ping |
| Env | `KEEPASSXC_PASSWORD` | Phase 6 vault check |
| Handoff | `memory/recommender`, `memory/advisor`, `token-savior-mcp`, `context-mode` | Auto-wire delegation |

> **Auto-trigger:** fires at every new chat start on any project that has a CLAUDE.md. Invoked by `agent-setup-wizard` as its final phase (Phase 11).

---

## When to invoke

**Auto-trigger phrases:**
- Any new chat where project context is being established
- "I'm starting a new chat"
- "New session"
- "Resume from handover"
- "What's the state of [project]?"

**Conditions:**
- Project root has a CLAUDE.md → run full primer
- No CLAUDE.md → run `agent-setup-wizard` first; chat-primer is its final step

---

## Inputs

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `project_root` | path | cwd | Project root to load context from |
| `mode` | `full` \| `quick` | `full` | full = all phases; quick = handover + ug-ug gate only |
| `force_vault_check` | bool | false | Re-check vault even if password already confirmed this session |

---

## Phase 0 — Bot INBOX check (5s)

Before any other phase, check for `INBOX.md` in the bot's root folder (e.g. `<project>/<bot>/INBOX.md`):

- If present: read it; extract any 🔴 items not yet struck through
- Surface 🔴 items in the SESSION READY card under **"Pending actions"**
- 🟡 items: include as a collapsible note; don't block session start
- If absent: skip silently

**INBOX.md** is the cross-session async handover for bots. It accumulates task drops from other sessions without requiring the user to manually paste context. Always check before starting work.

Also check `<workspace>/...` for any pending machine-readable relay items addressed to this bot slug or "any". Surface these alongside INBOX items.

**Write side:** `skills/session-relay/SKILL.md` — sessions use this to dispatch items to other bots' INBOXes automatically (runs as Phase 0 of session-handover).

---

## Phase 1 — Context detection (30s)

Check for existence of these files in `project_root`:

```
CLAUDE.md           → load project name, bots, skills list
HANDOVER.md         → prior session state
_context/OPEN-ITEMS.md
_context/LESSONS.md
_context/ADR.md
_references.md      → external path map
```

If `HANDOVER.md` missing → create stub at Phase 6.  
If `_references.md` missing → scaffold at Phase 7.

---

## Phase 1.5a — Capability discovery (intent-match the opening task)

**Goal:** every new chat surfaces the established skills, runners, and functions
relevant to *what the user is actually starting* — so nothing gets rebuilt that
already exists. This is the discovery capability formerly in `skill-recommender`,
now automatic and intent-aware.

**Trigger:** run when the session has an opening task/prompt (not just a bare
"resume"). If no task is stated yet, defer until the user's first real request,
then run once.

**Match the stated task against FIVE corpora:**

1. **Skills** — `skills/REGISTRY.md` (slug · category · role · tags).
   Rank by keyword/intent overlap with the task. Exclude `[PARKED]` unless the
   task is clearly in that domain.
2. **Runners** — `<routines>/ROUTINES-INDEX.md` (name · purpose).
   Surface any routine whose purpose matches the task (e.g. "weekly report",
   "fathom sync", "contract scan"). If the index is missing/stale, regenerate:
   `python <routines>/gen_routines_index.py`.
3. **Functions** — `FUNCTIONS.md` across the hub. For specific verbs/nouns in the
   task (parse, embed, fetch, classify, dedupe…), grep the hub for a matching
   pure function before writing new code: search `skills/**/FUNCTIONS.md`.
4. **Past solutions (CROSS-PROJECT) — the key anti-amnesia step.** Other projects
   and sessions may have already solved this. Run BOTH recall layers:
   ```
   python <routines>/memory_index.py search "<one-line task>" --k 5
   python skills/project-knowledge-query/query.py "<one-line task>" --k 5
   ```
   - `memory_index` = dev LESSONS + per-project memory (the "how we built it" layer).
   - `project-knowledge-query` = Jira resolved tickets, Fathom call decisions, client
     emails, estimations, project-brain snapshots (the "what the client/project did"
     layer). Auto-detects a named project and leads with its data.
   Surface any hit above ~0.55 — it may already hold the fix, decision, or estimate.
   Rebuild if stale: `python <routines>/memory_index.py build` /
   `python <routines>/project_knowledge.py build`.
5. **Secrets already in the vault** — read `<your-secrets-vault>` (names
   only). If the task needs a credential that already exists there, use
   `get_secret("Group/Entry")` — do NOT ask the user or create a duplicate. If the
   index is stale, regenerate: `python <routines>/gen_vault_index.py`.

**Output** `_context/relevant-capabilities.md`:

```markdown
# Relevant capabilities — matched to: "<one-line task>"
Checked: <date>

## Skills (top 5)
| Skill | Why it matches |
|---|---|
| web-researcher | task mentions "scrape competitor sites" |

## Runners (top 3)
| Routine | Why it matches |
|---|---|
| contract-scout.py | task = "find new gov contracts" |

## Past solutions (cross-project memory — top 5)
| Score | Origin | Title |
|---|---|---|
| 0.69 | skill/aws-to-github-secret | how to set GH secrets via stdin piping |

## Functions to reuse (don't rewrite)
| Function | Skill | Signature |
|---|---|---|
| embed | _lib_llm | embed(texts, model=) |

## Vault credentials available (names only)
- `AWS/taylor-base` · `GitHub/TaylorQ` (fetch via get_secret at use time)
```

**Rule:** if a strong match exists in ANY corpus, reuse/build-on it BEFORE writing
new code or asking the user. The cross-project memory hit (#4) is the one that stops
sessions from re-solving what another project already figured out.
Surface the counts in the SESSION READY card (see Phase 12 CAPABILITIES line).

---

## Phase 1.5b — Hub drift check

Detect skills added to the hub since this project was last configured. Keeps projects from silently falling behind the hub.

**Steps:**

1. Read project `CLAUDE.md` — extract the skills list (any `wip/` paths referenced)
2. Detect the project's primary domains from the skill names (developer · deployer · qa-auditor · designer · marketing · etc.)
3. Read `skills/REGISTRY.md` — filter to same domains
4. Diff: hub skills for those domains minus project's current skills = **candidate additions**
5. Filter candidates by relevance:
   - Skip skills the project explicitly doesn't need (e.g. skyrim-* on a SaaS project)
   - Skip skills already in `_context/drift-ignored.md` (user-dismissed list)
   - Keep: same domain, not already included, added to hub after CLAUDE.md `Last updated:` date

6. Write candidates to `_context/hub-drift.md`:

```markdown
# Hub drift — [project slug]
Checked: [date]
CLAUDE.md last updated: [date from file]

## New hub skills not yet in this project

| Skill | Domain | Added | Role (1 line) | Add? |
|---|---|---|---|---|
| token-compressor | developer | 2026-05-15 | Compress code/prose to fit context budgets | [ ] |
| repo-security-scan | qa | 2026-05-15 | Pre-import CVE + scorecard + secrets audit | [ ] |
```

7. Surface count in SESSION READY card.

**Dismissal:** if user says "ignore [skill]" → append to `_context/drift-ignored.md` so it doesn't re-surface.

**Skip condition:** if CLAUDE.md `Last updated:` matches today → no new drift possible; skip read of REGISTRY.md.

Output in SESSION READY card:
```
DRIFT:     3 new hub skills available → _context/hub-drift.md
```
or:
```
DRIFT:     up to date ✓
```

---

## Phase 2 — Ug-ug gate (non-skippable)

Immediately output:

```
UG-UG: ULTRA ✓
─ all plans/reasoning/handovers: ultra compressed
─ user chat: normal prose
─ banned openers enforced
```

If project CLAUDE.md has a different ug-ug level → override to ultra for this session and note the override. Never downgrade from ultra once set.

---

## Phase 3 — Load prior session state

Read `HANDOVER.md`. Extract:
- `completed[]` — list of done items from last session
- `open_items[]` — active blockers / in-progress
- `decisions[]` — architecture choices locked
- `files_modified[]` — last session's changed files
- `next_action` — prescribed first step

If HANDOVER.md has content → surface the `open_items` and `next_action` in the SESSION READY card.  
If HANDOVER.md is stub/empty → report "no prior state".

---

## Phase 4 — Token-saving auto-wire (actuator, idempotent)

**Goal:** every project has token-savior-mcp + context-mode (where appropriate) auto-installed without manual setup.

### Step 4.1 — Determine the per-project profile

Detect project type from signals (in priority order, first match wins):

| Signal | Auto-wire profile | MCPs included |
|---|---|---|
| `skills/` in cwd | **skills-hub** | token-savior-mcp + skill-linter + skillmaster auto-active |
| `terraform/*.tf` present | **iac** | token-savior-mcp + careful-guard active |
| `package.json` + `next.config.*` | **nextjs** | token-savior-mcp + context-mode + ollama-mcp |
| `pyproject.toml` or `requirements.txt` | **python** | token-savior-mcp (no context-mode by default — Python files are smaller) |
| `engagement.json` present | **client** | token-savior-mcp + context-mode + engagement-config-setup auto-load |
| >50 source files OR ≥10k LOC | **large-codebase** | token-savior-mcp + context-mode |
| default | **small** | token-savior-mcp only |

### Step 4.2 — Write or merge `.mcp.json`

```python
# Pseudocode
target = project_root / ".mcp.json"
desired = profile_mcp_servers(profile_name)  # ordered dict of server configs

if not target.exists():
    target.write_text(json.dumps({"mcpServers": desired}, indent=2))
    log_auto_wire(f"created .mcp.json with {list(desired)}")
else:
    existing = json.loads(target.read_text())
    added = []
    for name, cfg in desired.items():
        if name not in existing.get("mcpServers", {}):
            existing.setdefault("mcpServers", {})[name] = cfg
            added.append(name)
    if added:
        target.write_text(json.dumps(existing, indent=2))
        log_auto_wire(f"merged into .mcp.json: {added}")
    else:
        log_auto_wire(".mcp.json already complete — no-op")
```

Canonical MCP server entries (used by every profile that includes them):

```jsonc
{
  "mcpServers": {
    "token-savior": {
      "command": "npx",
      "args": ["-y", "token-savior-mcp"],
      "env": {"DEDUP_THRESHOLD": "3"}
    },
    "context-mode": {
      "command": "npx",
      "args": ["-y", "@mksglu/context-mode"]
    },
    "ollama": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-ollama"],
      "env": {"OLLAMA_BASE_URL": "http://localhost:11434"}
    }
  }
}
```

### Step 4.3 — Audit log

Every action writes to `<project>/_context/auto-wire.log`:

```
2026-05-20T14:32:11 PHASE=4 PROFILE=nextjs ADDED=token-savior,context-mode FILE=.mcp.json
```

### Output

```
TOKEN MCPs:
  profile:   nextjs
  .mcp.json: ✓ wrote 3 servers (token-savior, context-mode, ollama)
  audit:     _context/auto-wire.log
```

Or, idempotent re-run:

```
TOKEN MCPs:
  profile:   nextjs
  .mcp.json: ✓ already configured (no-op)
```

For `token-compressor` (CLI tool, not MCP): mentioned in SESSION READY only as `[standby]` — it's invoked on demand for large doc injection, not auto-wired.

---

## Phase 5 — Memory auto-init (actuator, idempotent)

**Goal:** every project has a configured memory backend by end of session 1, without manual setup.

### Step 5.1 — Detect state

Check three sources, in order:

1. `<project>/_context/memory-config.yaml` — backend config
2. `<project>/MEMORY.md` — per-project memory index
3. `~/.claude/projects/<slug>/memory/MEMORY.md` — Claude Code's auto-memory surface

States:

| memory-config.yaml | MEMORY.md | State | Action |
|---|---|---|---|
| missing | missing | **first session** | auto-init via `memory/recommender` (Step 5.2) |
| missing | present | partial — config drift | invoke `memory/advisor` in `assess` mode to write config |
| present | missing | partial — seed never ran | invoke `memory/advisor` in `provision` mode to seed |
| present | present | configured | no-op; just hydrate (Step 5.3) |

### Step 5.2 — Auto-init (first session)

Invoke `skills/memory/recommender/SKILL.md` with project signals:

```json
{
  "project_slug": "<slug>",
  "task": "set-up",
  "constraints": {
    "corpus_size_mb": <from file walk>,
    "needs_rag": <from project profile: false unless docs-heavy>,
    "cross_user": <false for solo-dev>,
    "auto_invoked": true
  }
}
```

Recommender writes `_context/memory-config.yaml` with backend choice + tier map. Default for solo-dev workflows: `memory/memory-ladder`. Then hand off to `memory/advisor` in `provision` mode to seed `MEMORY.md` + Claude Code's `<slug>/memory/MEMORY.md`.

### Step 5.3 — Hydration (every session)

After config exists:

1. Read `_context/memory-config.yaml` → identify backend
2. Read `MEMORY.md` → count entries; surface last 5 for SESSION READY context
3. Read `HANDOVER.md` (already done in Phase 3) → surface open_items + next_action

### Step 5.4 — Audit log

```
2026-05-20T14:32:14 PHASE=5 STATE=first-session ACTION=auto-init BACKEND=memory/memory-ladder FILES=memory-config.yaml,MEMORY.md
```

### Output

First session:
```
MEMORY:
  state:    first session
  backend:  memory/memory-ladder  (auto-picked by memory/recommender)
  files:    _context/memory-config.yaml ✓ · MEMORY.md ✓ (seeded)
  hydrate:  HANDOVER.md not present (clean slate)
```

Returning session:
```
MEMORY:
  state:    configured
  backend:  memory/memory-ladder  (N entries in MEMORY.md)
  hydrate:  HANDOVER.md ✓ (N open, N completed) · last 5 MEMORY entries loaded
```

If memory-config.yaml backend is unreachable (e.g., future onyx config but onyx server down):
```
⚠ MEMORY:
  state:    backend unreachable (memory/onyx → <lan-host>:8080 ✗)
  fallback: temporarily routing to memory/memory-ladder
  fix:      check onyx server health or rerun memory/recommender
```

---

## Phase 6 — Secrets vault check

1. Check `KEEPASSXC_PASSWORD` env var: `echo $env:KEEPASSXC_PASSWORD` (PowerShell) or `echo $KEEPASSXC_PASSWORD` (bash)
2. If set → `VAULT: ✓ (pw set)`
3. If not set → `VAULT: ⚠ pw not in env — set KEEPASSXC_PASSWORD before credential calls`
4. Read project CLAUDE.md for credential references. List which vault entries are needed:
   - Jira, AWS, GitHub, Fathom, Gmail, Telegram — whichever appear in the CLAUDE.md
5. Attempt a smoke-test read of the first required entry: `get_secret("GitHub/TaylorQ")` — confirms vault file is reachable

Vault path: `<your-secrets-vault>`  
Wrapper: `skills/keepassxc-secrets/SKILL.md`

Output:
```
VAULT: ✓  pw=set · entries=6 (GitHub · Jira · AWS · Fathom · Gmail · Telegram)
```

---

## Phase 7 — Ollama availability

Ping `http://localhost:11434/api/tags`. Parse response for installed models.

Expected models (from <workspace> local-toolchain):
- `phi4-mini` — routing, classification
- `qwen2.5-coder:7b` — code repair loop
- `qwen3:8b` — reasoning + thinking mode
- `gemma3` — general
- `llama3.1:8b` — general

Output:
```
OLLAMA: ✓  phi4-mini · qwen2.5-coder:7b · qwen3:8b · gemma3 · llama3.1:8b
```

If Ollama is down:
```
OLLAMA: ✗  not responding — test loop will fall back to cloud (cost ↑)
  Start: ollama serve  (or restart Ollama Desktop)
```

If models missing:
```
OLLAMA: ⚠  qwen2.5-coder:7b not found — run: ollama pull qwen2.5-coder:7b
```

---

## Phase 8 — External references

Check for `_references.md` in project root. If missing, scaffold from CLAUDE.md paths:

```markdown
# References — [project slug]

| Label | Path | Notes |
|---|---|---|
| Skills hub | `skills/` | REGISTRY.md · CAPABILITY-MAP.md |
| Core skill kit | `skills/CORE-SKILL-KIT.json` | 24 foundational skills |
| Secrets vault | `<your-secrets-vault>` | keepassxc-secrets wrapper |
| Local models | `<workspace>/...` | gguf/ · loras/ · hf/ |
| Ollama | `http://localhost:11434` | phi4-mini · qwen2.5-coder:7b |
| [additional paths from CLAUDE.md] | ... | ... |
```

Write to `{project_root}/_references.md` if it doesn't exist.

Output:
```
REFS: _references.md ✓  (6 paths)
```

---

## Phase 9 — Skills fine-tuning scan

Scan the project's selected skills from CLAUDE.md. For each skill that:
- Calls phi4-mini or haiku for a **classification/routing** step → flag as fine-tune candidate (local ART training could replace the API call)
- Has a repetitive pattern with fixed input/output shape → flag as Lambda candidate

Write candidates to `_context/finetune-candidates.md` (create if missing):

```markdown
# Fine-tune candidates — [project slug]
Generated: [date]

| Skill | Step | Pattern | Fine-tune value | Training data source |
|---|---|---|---|---|
| task-router | intent classification | fixed 20-intent taxonomy | HIGH — 100% local if trained | project CLAUDE.md + operator logs |
| skill-recommender | skill matching | N skills vs task desc | MED — phi4-mini after ART | skill hub REGISTRY.md pairs |
```

If no candidates found → note "no fine-tune candidates identified".

Output:
```
FINE-TUNE: 2 candidates flagged → _context/finetune-candidates.md
```

---

## Phase 10 — Ollama test prep

Check for `test-config.json` in project root. If missing and project has tests, scaffold:

```json
{
  "project_root": "{project_root}",
  "test_command": "pytest tests/",
  "ollama_repair_model": "qwen2.5-coder:7b",
  "ollama_classify_model": "phi4-mini",
  "max_repair_attempts": 3,
  "escalate_to_cloud_after": 3,
  "cloud_model": "claude-sonnet-4-6",
  "ug-ug_log": true,
  "log_path": "{project_root}/_logs/test-loop.ug-ug.jsonl"
}
```

Cross-reference: `skills/test-loop-ug-ug-logger/SKILL.md`

Output:
```
TEST LOOP: test-config.json ✓  (phi4-mini → qwen2.5-coder:7b → sonnet escalate@3)
```

---

## Phase 11 — Handoff standard

Verify `session-handover` is wired. Check CLAUDE.md for session-handover reference.

If missing → add reminder:
```
⚠ HANDOFF: session-handover not referenced in CLAUDE.md
  Run /reflect or session-handover at context ~50% to write HANDOVER.md
  Skill: skills/lifecycle/session-handover/SKILL.md
```

If HANDOVER.md exists and is fresh (< 24h) → note last update timestamp.

---

## Phase 12 — SESSION READY card (output)

Emit the compact status card to chat. The `AUTO-WIRED THIS SESSION` block makes Phase 4 + Phase 5 actuator work visible:

```
SESSION READY ──────────────────────────────────────
PROJECT: [slug]          BOT: [bot name]      PROFILE: [nextjs|python|iac|client|skills-hub|small|large-codebase]
UG-UG: ULTRA ✓
────────────────────────────────────────────────────
AUTO-WIRED THIS SESSION:
  [✓ created .mcp.json (token-savior + context-mode + ollama)]
  [✓ memory/recommender → memory/memory-ladder; seeded MEMORY.md]
  [or: nothing — already configured (idempotent re-run)]
────────────────────────────────────────────────────
HANDOVER:  [loaded — N open / N done] | [no prior state]
TOKEN:     [context-mode + token-savior | token-savior only | ⚠ not configured]
MEMORY:    [memory/memory-ladder ✓ N entries | first session — seeded | ⚠ backend unreachable]
VAULT:     [✓ pw=set · entries=N] | [⚠ pw not set]
OLLAMA:    [✓ phi4-mini · qwen2.5-coder:7b · qwen3:8b] | [✗ offline]
REFS:      [_references.md ✓ N paths] | [✓ scaffolded N paths]
CAPABILITIES: [N skills · N runners · N functions · N past-solutions matched to "<task>" → _context/relevant-capabilities.md] | [no task stated yet]
RECALL:    [top cross-project hit: "<title>" (score) — already solved in <project>] | [no prior solution found]
VAULT:     [N entries available — see VAULT-INDEX.md] (already shown in Phase 6)
DRIFT:     [N new hub skills → _context/hub-drift.md] | [up to date ✓]
FINETUNE:  [N candidates → _context/finetune-candidates.md] | [none]
TEST LOOP: [test-config.json ✓] | [⚠ not configured]
────────────────────────────────────────────────────
OPEN ITEMS ([N]):
  • [item 1 from HANDOVER.md]
  • [item 2]

NEXT: [next_action from HANDOVER.md] | [run agent-setup-wizard]
─────────────────────────────────────────────────────
```

The `AUTO-WIRED THIS SESSION` line summarizes `_context/auto-wire.log` entries written by Phase 4 + Phase 5 during THIS run. If the log shows no new entries today, the line reads "nothing — already configured (idempotent re-run)."

---

## Output spec

| File | Condition | Description |
|---|---|---|
| `_context/relevant-capabilities.md` | created when a task is stated | Skills + runners + functions intent-matched to the opening task |
| `_context/hub-drift.md` | created/updated each session | New hub skills not yet in this project |
| `_context/drift-ignored.md` | appended on user dismissal | Skills the user has chosen not to add |
| `_references.md` | created if missing | External path map |
| `_context/finetune-candidates.md` | created if candidates found | Fine-tune flagged skills |
| `_context/test-config.json` | created if missing + tests present | Ollama test loop config |
| `HANDOVER.md` | stub created if missing | Session state template |

---

## Lambda candidates

| Function | Step | Lambda? |
|---|---|---|
| `check_file_exists(path)` | Phase 1 detection | ✅ pure |
| `ping_ollama(url)` | Phase 7 | ✅ HTTP only |
| `parse_handover(path)` | Phase 3 | ✅ pure |
| `select_token_mode(signals)` | Phase 4 | ✅ lookup table |
| `scaffold_references_md(claude_md)` | Phase 8 | ✅ pure |
| `scan_finetune_candidates(skills)` | Phase 9 | ✅ rule-based |

---

## Handoffs

| Next | When | Path |
|---|---|---|
| `agent-setup-wizard` | No CLAUDE.md found | `skills/lifecycle/agent-setup-wizard/SKILL.md` |
| `session-handover` | At ~50% context | `skills/lifecycle/session-handover/SKILL.md` |
| `memory/recommender` | **Phase 5 auto-init: memory not configured** | `skills/memory/recommender/SKILL.md` |
| `memory/advisor` | Phase 5 partial state (config or seed missing) | `skills/memory/advisor/SKILL.md` |
| `memory/memory-ladder` | Default solo-dev memory backend | `skills/memory/memory-ladder/SKILL.md` |
| `token-savior-mcp` | **Phase 4 auto-wire to .mcp.json** | `skills/developer/token-savior-mcp/SKILL.md` |
| `context-mode` | **Phase 4 auto-wire to .mcp.json (large-codebase/nextjs/client profiles)** | `skills/developer/context-mode/SKILL.md` |
| `token-compressor` | External doc injection needed (on-demand, not auto-wired) | `skills/developer/token-compressor/SKILL.md` |
| `keepassxc-secrets` | Vault pw not set | `skills/keepassxc-secrets/SKILL.md` |
| `test-loop-orchestrator` | Tests configured + ready to run | `skills/test-loop-orchestrator/SKILL.md` |
| `art-train` | Fine-tune candidates flagged | `skills/art-train/SKILL.md` |
