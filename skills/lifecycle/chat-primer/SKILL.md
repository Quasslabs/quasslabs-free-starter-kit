# SKILL: chat-primer

**Bot:** any  
**Role:** "Session ready" ritual for any new chat. Auto-wires memory (via memory/recommender) and the verified-real local Ollama MCP (`ollama-mcp`) on first session per project. (NOTE 2026-06-03: token-savior-mcp + context-mode are NOT installable — pattern-source repos only; no longer auto-wired.) Idempotent — no-op when already configured. Confirms ug-ug, verifies vault + Ollama, scaffolds missing reference files, flags drift + fine-tune candidates. Outputs a compact SESSION READY card.  
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

## Invocation mechanism

**This skill is model-driven, NOT a Claude Code settings.json hook.**

The trigger is the global `CLAUDE.md` instruction at `~/<path>`:

```
At every new chat start:
1. Check if cwd (or referenced project) has a CLAUDE.md
2. If yes  → invoke chat-primer immediately
3. If no   → invoke agent-setup-wizard
```

Claude reads this instruction at the start of every session and invokes the skill accordingly. There is no `PreSession`, `PreToolUse`, or other hook entry in `settings.json` — the model itself is the trigger.

**What this means in practice:**
- Works in Claude Code, Cursor, Codex — anywhere the global CLAUDE.md is loaded
- Does NOT fire in bare API calls (no CLAUDE.md injection there)
- Can be skipped by the user with "skip primer" — model-driven triggers are soft
- Re-firing mid-session: invoke manually if context was lost ("re-run chat-primer")

**To add to a new project:** add this block to the project's CLAUDE.md:
```markdown
## Session start
If this project has a CLAUDE.md → invoke `chat-primer` immediately.
```

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

## Phase 0.3 — Skillmaster dispatch inbox (5s — Skillmaster sessions only)

**Only runs when:** `project_root` is `skills/` or `<workspace>/...` (Skillmaster context detected).

Scan `skills/_inbox/` for `.md` files with frontmatter `status: wip` or `status: blocked`:

```bash
# List inbox files with status != done
grep -rl "^status: " G:/AI/skills/_inbox/ --include="*.md"
```

- `done` items: skip silently (already completed)
- `wip` or `blocked` items: surface in SESSION READY card under **"Dispatch inbox"** with skill slug + status + todos
- No files → skip silently

**Also:** scan `skills/_dispatch/` for unread `*-starter.md` files (dispatched but not yet opened). Count + list slugs.

---

## Phase 0.5 — Agent mailbox check (5s)

Check for unread cross-machine messages from the other Claude instance (Windows hub ↔ Mac mini):

```bash
python skills/agent-mailbox/mailbox.py read --unread   # Windows
python3 ~/AI/skills/wip/agent-mailbox/mailbox.py read --unread    # Mac
```

- Any messages → surface in the SESSION READY card under **"Messages from other instance"**
- `[STALE]` banner means the canonical thread (on the Mac) was unreachable — note it, don't block
- None / command absent → skip silently
- This also auto-flushes any offline-queued outbox messages (Windows side) as a side effect

Mid-session, re-run the same command to pick up messages that arrived after start.
Skill: `skills/agent-mailbox/SKILL.md`.

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

## Phase 1.5c — Context pressure check

**Goal:** catch large context dumps before they fill the window, offer compression before any work begins.

Estimate opening context size: count characters across all files read so far in Phase 1 + 1.5a + 1.5b.

| Context size | Action |
|---|---|
| < 30k chars | No-op — continue |
| 30k–50k chars | Note in SESSION READY: `CONTEXT: moderate pressure — monitor` |
| > 50k chars | Offer compression: "Opening context is large (~Xk chars). Run token-compressor to reduce by 60-90%? (y/n)" |

If user approves (or context > 80k chars, auto-run without asking):
```bash
python <routines>/token_compressor.py --mode code --stdin < [largest context file]
# or pipe the HANDOVER.md + OPEN-ITEMS.md through it
```

Log in SESSION READY:
```
CONTEXT:   [size]k chars | [compressed → Yk chars | token-compressor] or [within budget]
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

> **CORRECTED 2026-06-03.** Prior versions of this phase auto-wired `token-savior-mcp`,
> `@mksglu/context-mode`, and `@modelcontextprotocol/server-ollama` — ALL THREE 404 on npm
> and were never installable. Any `.mcp.json` written before this date may reference dead
> packages; re-run this phase to clean them. Only verified-installable servers are wired now.

**Goal:** every project has the verified-real local Ollama MCP wired (where useful) without manual setup. token-savior / context-mode are NOT installable (pattern-source repos only) — do not add them to any `.mcp.json`.

### Step 4.1 — Determine the per-project profile

Detect project type from signals (in priority order, first match wins):

| Signal | Auto-wire profile | MCPs included (verified-installable only) |
|---|---|---|
| `skills/` in cwd | **skills-hub** | ollama-mcp (skill-linter + skillmaster are skills, not MCPs) |
| `terraform/*.tf` present | **iac** | ollama-mcp |
| `package.json` + `next.config.*` | **nextjs** | ollama-mcp |
| `pyproject.toml` or `requirements.txt` | **python** | ollama-mcp |
| `engagement.json` present | **client** | ollama-mcp |
| >50 source files OR ≥10k LOC | **large-codebase** | ollama-mcp |
| default | **small** | (none — skip .mcp.json write) |

> Context dedup is currently handled by Claude Code's built-in auto-compact (75% via
> `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`) + the PreCompact `smart_compressor.py`. A dedicated
> mid-session dedup MCP is a future clean-room build (see token-savior-mcp LESSONS).

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

Canonical MCP server entry (verified installable — `ollama-mcp` resolves on npm, v2.1.0):

```jsonc
{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"],
      "env": {"OLLAMA_HOST": "http://localhost:11434"}
    }
  }
}
```

> Before writing, verify the package still resolves: `npm view ollama-mcp version`.
> If it 404s, skip the write rather than producing a broken `.mcp.json`.
> NEVER write `token-savior-mcp`, `@mksglu/context-mode`, or `@modelcontextprotocol/server-ollama` — all dead.

### Step 4.2.5 — Heal dead entries

If `.mcp.json` already exists, scan it for the three dead package names above and REMOVE those entries (they cause Claude Code MCP-connect failures). Log what was removed.

### Step 4.3 — Audit log

Every action writes to `<project>/_context/auto-wire.log`:

```
2026-06-03T14:32:11 PHASE=4 PROFILE=nextjs ADDED=ollama REMOVED=token-savior,context-mode FILE=.mcp.json
```

### Output

```
MCP WIRE:
  profile:   nextjs
  .mcp.json: ✓ wrote ollama-mcp [+ removed 2 dead entries]
  audit:     _context/auto-wire.log
```

Or, idempotent re-run:

```
MCP WIRE:
  profile:   nextjs
  .mcp.json: ✓ already correct (no-op)
```

For `token-compressor` (a real local Python CLI, not an MCP): auto-offered in Phase 1.5c when context > 50k chars; auto-run when > 80k chars. This is the genuine token-saving path.

**Phase 4 is no longer a hard gate.** Wiring ollama-mcp is useful but optional; a missing `.mcp.json` does not block work. The real context controls are auto-compact (75%) + smart_compressor + token-compressor (Phase 1.5c).

---

## Phase 4.5 — Active skills block auto-wire (actuator, idempotent)

**Goal:** every project CLAUDE.md has a `<!-- skill-audit-candidates -->` block so the 8-prompt skill audit hook has a candidate list to check against. Without this block, the hook fires but does nothing.

### Step 4.5.1 — Check for existing block

Read `{project_root}/CLAUDE.md`. Search for `<!-- skill-audit-candidates -->`.

If found → skip entirely (idempotent). Log: `SKILLS BLOCK: already present`.

### Step 4.5.2 — Detect project type

Reuse the same signals from Phase 4:

| Signal | Project type | Candidate set |
|---|---|---|
| `skills/` in cwd | skills-hub | skillmaster · skill-builder · skill-linter · ps1-sanitizer · session-skill-auditor |
| `engagement.json` present | client / scope | scope-phase-runner · storyboard-taskcrafter · estimate-chat-primer · scope-vetter · session-skill-auditor |
| `terraform/*.tf` present | iac | terraform-safe · deployer/terraform-validator · qa-auditor/security-gate · ps1-safe-script · session-skill-auditor |
| `package.json` + `next.config.*` | nextjs / web-app | developer/careful-guard · qa-auditor/dev-gate · code-reviewer · ps1-safe-script · session-skill-auditor |
| `package.json` + `react-native` in deps | mobile-rn | developer/careful-guard · android-build-deploy · qa-auditor/dev-gate · ps1-safe-script · session-skill-auditor |
| `pyproject.toml` or `requirements.txt` | python / data | developer/careful-guard · qa-auditor/dev-gate · qa-auditor/supply-chain-scanner · ps1-safe-script · session-skill-auditor |
| `.github/workflows/*.yml` present | any with CI/PRs | + ollama-pr-gemini-watcher · ollama-pr-replier · code-reviewer |
| default (no strong signal) | general | developer/careful-guard · qa-auditor/dev-gate · ps1-safe-script · session-skill-auditor |

Always include `ps1-safe-script` (this machine is always Windows + Git Bash) and `session-skill-auditor` (self-reinforcing).

### Step 4.5.3 — Write the block

Append to `{project_root}/CLAUDE.md` (before the last `---` or at end of file):

```markdown
## Active skills

<!-- skill-audit-candidates -->
- developer/careful-guard — before editing existing source files
- qa-auditor/dev-gate — before QA handoff
- code-reviewer — before opening a PR
- ps1-safe-script — before any PowerShell output
- ollama-pr-gemini-watcher — auto-triggers on gh pr create via hook
- session-skill-auditor — periodic check that all relevant skills are active
<!-- /skill-audit-candidates -->
```

Replace the skill list with the project-type-appropriate set from Step 4.5.2.

Add one-line description per skill using this format: `- {skill-name} — {when it applies in ≤8 words}`

### Step 4.5.4 — Log

Write to `_context/auto-wire.log`:
```
{ts} PHASE=4.5 PROFILE={project_type} WROTE=active-skills-block FILE=CLAUDE.md
```

Report in SESSION READY card:
```
SKILLS BLOCK: wrote 6-skill candidate list (nextjs profile) → CLAUDE.md
```
or if already present:
```
SKILLS BLOCK: already configured
```

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
SKILLS:    [wrote 6-skill candidate list (nextjs) → CLAUDE.md] | [already configured]
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
