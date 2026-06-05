# SKILL: project-env-setup

**Bot:** operator · developer · any  
**Role:** Bootstrap a new project or repo with the core context and reference structure so any agent (Claude Code, Cursor, Codex) can orient themselves immediately. Installs: CLAUDE.md, AGENTS.md, .cursorrules, _refs.md, and a minimal mind palace pointing to the right skills.  
**Ug-ug mode:** full
**Model:** opus - high-stakes judgment or architecture trade-offs required
**Tool compatibility:** Claude Code · Cursor (primary target) · Codex
**Status:** beta
**Parallelizable:** conditional - yes if each run writes a distinct project_path; no if two runs scaffold the same path concurrently

## Model

**Verdict:** `phi4-mini` — context file generation from templates is a structured fill-in task suitable for a lightweight classifier/generator.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Template rendering from project context; no heavy reasoning |
| Local (installed) | phi4-mini | 2.5GB; handles structured template generation adequately |
| Local (ideal) | phi4-mini | Already installed; right-sized for scaffold generation |

---

## When to invoke

- "Set up context for this new project"
- "Bootstrap [project] for our agent stack"
- "Install the standard references"
- When starting any new repo or engagement in the AppsTango / Quass Labs ecosystem
- After `ballparker init <slug>` for new engagements

---

## What gets installed

| File | Purpose | Target tools |
|---|---|---|
| `CLAUDE.md` | Mind palace for Claude Code + Cowork | Claude Code, Cowork |
| `AGENTS.md` | Equivalent for Codex / OpenAI agents | Codex, any AGENTS.md reader |
| `.cursorrules` | Project context + skill pointers for Cursor | Cursor |
| `_refs.md` | Bot registry + sibling paths (if in a bot folder) | All |
| `LESSONS.md` | Empty template — fill via gstack /reflect | All |
| `HANDOVER.md` | Cross-session state template — populated by session-handover skill | All |
| `_context/WORKFLOW.md` | Boris Cherny workflow principles + GStack stage sequence | All |
| `_context/OPEN-ITEMS.md` | Active blockers / pending decisions | All |
| `_context/DECISIONS.md` | Sprint decisions log | All |
| `_context/ug-ug-rules.md` | Project-specific ug-ug level overrides | All |

---

## Step 1 — Gather project context

Ask (or infer from project structure):
```
1. Project name and slug
2. Client name (if engagement)
3. Primary tech stack (Node/Python/etc.)
4. Which bots are relevant (ballparker? qa-auditor? designer?)
5. Which LLMs to prefer (see LLM targeting below)
6. Primary language for code (TypeScript? Python?)
```

---

## Step 2 — Generate CLAUDE.md

```markdown
# Claude Code — `[PROJECT PATH]`

**Project:** [Project Name]  
**Client:** [Client Name] (if applicable)  
**Slug:** [slug]  
**Stack:** [Node/TypeScript/Python/etc.]

## Quick context

[1-3 sentences about what this project does]

## Agent instructions

- Use **ug-ug mode** for internal reasoning (skills/ug-ug/SKILL.md)
- Use **gstack** for structured engineering team roles (skills/gstack/SKILL.md)
- Use **memory-ladder** for cross-session handoffs (skills/memory/memory-ladder/SKILL.md)
- Route complex requests via **operator** (<project>/operator/README.md)

## LLM targeting

| Task | Preferred model |
|---|---|
| Long reasoning, architecture | claude-opus-4-6 or ollama (local) |
| Standard coding, review | claude-sonnet-4-6 |
| Fast/cheap ops (classify, format) | claude-haiku-4-5 |
| Context compression | LLMLingua (pilot) |

## Key paths

| Thing | Path |
|---|---|
| Skills hub | skills/ |
| This bot's skills | [bot-skills-path] |
| Operator skill | skills/operator/SKILL.md |
| Tech stack ref | <notes>/... |
| Starred repos | <notes>/... |

## Relevant skills for this project

[List from skill-recommender output]

## Sibling bots

[From _refs.md]
```

---

## Step 3 — Generate AGENTS.md (Codex / OpenAI convention)

```markdown
# AGENTS.md — [Project Name]

## Agent instructions

Read `CLAUDE.md` for full project context.

Key skills for this project:
- ug-ug: skills/ug-ug/SKILL.md (terse mode)
- gstack: skills/gstack/SKILL.md (team roles)
- operator: skills/operator/SKILL.md (routing)

## What not to modify

- Production configs (*.prod.env, terraform/*)
- DB migrations without explicit instruction
- Any file marked with "# DO NOT EDIT — generated"

## Standards

See CLAUDE.md → Agent instructions section.
All commits: use ug-ug-commit format (conventional commits, imperative, no body unless needed).
```

---

## Step 4 — Generate .cursorrules

```
# [Project Name] — Cursor rules

You are working in [Project Name], a [brief description].

## Context files to read first
- CLAUDE.md (mind palace — read before any task)
- _refs.md (bot registry — read when you need to hand off)

## Skills to use
- For terse/compressed output: read skills/ug-ug/SKILL.md
- For engineering team simulation: read skills/gstack/SKILL.md
- For this project's specific flows: read CLAUDE.md → Relevant skills section

## LLM routing
- Heavy reasoning tasks: prefer claude-opus-4-6 or local Ollama
- Standard coding: claude-sonnet-4-6
- Quick ops: claude-haiku-4-5

## Code conventions
[Stack-specific conventions — TypeScript strict mode, Python type hints, etc.]

## Never do
- Hardcode API keys or credentials
- Modify production configs without explicit instruction
- Skip type-check before running tests
- Commit directly to main

## Commit format (ug-ug-commit)
feat(scope): imperative description of what changed
fix(auth): fix what was broken
chore(deps): update thing
```

---

## Step 5 — Generate _refs.md (if in a bot folder)

```markdown
# [project-name] bot - refs

## Role
[1-line description]

## Skills
skills-path: skills/[bot-name]\
sync-script: skills/sync-skills.ps1

## Sibling bots
operator:       <project>/operator
[relevant bots based on project type]

## Skills hub
all-skills: the skills hub
```

---

## Step 6 — Generate LESSONS.md (empty template)

```markdown
# LESSONS.md — [Project Name]

Running log of lessons from each sprint or milestone.
Populated via gstack `/reflect` command.

---

<!-- lessons go here -->
```

---

## Step 7 — Generate memory-config.yaml skeleton

Create `_context/memory-config.yaml` with a skeleton that references the memory system to be selected:

```yaml
# _context/memory-config.yaml — [Project Name]
# Generated: [date]
# Status: TODO — run memory-recommender to populate this file

project_slug: [slug]

# Memory system selection
# One of: leann, onyx, memvid, milvus, memory-ladder, fathom-knowledge-graph, resolve-or-generate
memory_system: null  # TODO: run memory-recommender to decide

# MindPalace configuration (cross-session memory)
memory-ladder:
  enabled: true
  layer: 4+  # Layer 4+ for cross-session context preservation
  handover_path: ../HANDOVER.md
  snapshot_frequency: session-end
  context_limit_tokens: 100000

# Memory recommender TODO
# Instructions:
#   1. Run: python skills/memory/recommender/memory_recommender.py --project [slug]
#   2. It will analyze your project and recommend a system
#   3. It will update this file with the selected system and config
#   4. Then run memory-advisor to provision the system

notes:
  - All projects include memory-ladder (Layer 4+) for cross-session memory
  - Additional memory systems are project-dependent (see memory-recommender output)
  - For more info: skills/memory/advisor/SKILL.md
```

Also update `AGENTS.md` and `CLAUDE.md` to note that MindPalace is always enabled:

Add to CLAUDE.md:
```markdown
## Memory

This project uses **MindPalace Layer 4+** for cross-session context preservation.
See `_context/memory-config.yaml` for the full memory system configuration.

To select or update the memory system:
1. Run `memory-recommender` to analyze project characteristics
2. Run `memory-advisor` to provision the chosen system
3. Update this CLAUDE.md and _context/memory-config.yaml with the result
```

---

## Step 8 — Generate supporting context files

Create the following in `_context/`:

### `_context/WORKFLOW.md`

```markdown
# Workflow Rules — [Project Name]

## Workflow orchestration (Boris Cherny principles)

- **Plan first.** Plan mode for any task with 3+ steps. Write to tasks/todo.md.
- **Subagents for research.** One task per subagent. Offload exploration, parallel work.
- **Self-improvement loop.** After any correction: update LESSONS.md with the pattern.
- **Verify before done.** Prove it works. "Would a senior engineer approve this?"
- **Demand elegance.** Non-trivial changes: ask "is there a more elegant way?"
- **Autonomous bug fixing.** Fix it. Use logs/errors. Zero hand-holding.
- **/careful before destructive commands.** rm, DROP, force push, migrations — always confirm.
- **Compact at ~50% context.** Manual compact when half-full.

## GStack stage sequence

Think → Plan → Build → Review → Test → Ship → Reflect

Never skip stages. Each stage produces an artifact consumed by the next.
Full detail: `skills/gstack/SKILL.md`

## Commit format (ug-ug-commit)

feat(scope): imperative description
fix(auth): what was broken
chore(deps): what changed

One commit per file. No bundles.
```

### `_context/OPEN-ITEMS.md`

```markdown
# Open Items — [Project Name]

Active blockers, pending decisions, and yellow gates.
Updated during sessions. Cleared when resolved.

---

<!-- open items go here -->
```

### `_context/DECISIONS.md`

```markdown
# Decisions — [Project Name]

Architectural and product decisions made this sprint.
Populated during /reflect. Source of truth for ADR.md.

---

<!-- decisions go here -->
```

### `_context/ug-ug-rules.md`

```markdown
# Ug-ug Rules — [Project Name]

Project-specific ug-ug overrides. Global rules at ~/.claude/CLAUDE.md.

<!-- Add overrides here if this project needs different compression levels -->
<!-- Example: client-facing output uses 'none' even for internal reports -->
<!-- Example: this project's CLI tools always use 'ultra' -->

Default application (from global CLAUDE.md):
- Plans: ultra
- Internal reasoning: full
- User responses: normal prose
- Code: no change
```

---

Also update `CLAUDE.md` (generated in Step 2) to add a **Supporting files** section at the bottom referencing all `_context/` files as on-demand loads.

```markdown
## Supporting files (load on demand)

| File | Load when |
|---|---|
| `HANDOVER.md` | Session start — cross-session state |
| `LESSONS.md` | After any correction — update with pattern |
| `_context/ADR.md` | Architecture questions |
| `_context/OPEN-ITEMS.md` | Active blockers |
| `_context/DECISIONS.md` | Sprint decisions |
| `_context/WORKFLOW.md` | Complex multi-stage tasks |
| `_context/ug-ug-rules.md` | Project-specific ug-ug overrides |
| `_refs.md` | Bot handoffs / sibling bots |

<!-- HTML comments cost zero tokens. Use them for guidance notes. -->
<!-- Keep this CLAUDE.md under 200 lines. Move detail to _context/ files. -->
```

---

## LLM targeting reference

Match task to model based on cost + capability:

| Model | Use for | Cost tier |
|---|---|---|
| `claude-opus-4-6` | Architecture decisions, long reasoning, ambiguous problems | High |
| `claude-sonnet-4-6` | Standard coding, review, most tasks | Medium |
| `claude-haiku-4-5-20251001` | Classify, format, quick ops, log-watcher | Low |
| Local Ollama | Privacy-sensitive, no internet required, bulk operations | Free |
| LLMLingua | Context compression before LLM calls (pilot) | See tech-stack |

---

## Credentials — vault-first rule

Add to every generated `.env` template:

```bash
# ── KeePassXC vault (session-only, never commit) ──────────────────────────────
# KEEPASSXC_PASSWORD=<set in terminal session before running scripts>
# Vault: <your-secrets-vault>
# Covers: Jira · AWS (ql-bot-deployer · tq-at-bot-deployer) · Gmail · Fathom · GitHub · Telegram
# Usage: from _lib_data import get_secret; val = get_secret("Jira/pmlogs")
# Fallback: if not set → scripts read from env var / .env below (non-breaking)
```

Scripts that call external APIs should use `get_secret()` from `_lib_data.py` as the first credential source. See `skills/keepassxc-secrets/SKILL.md` for full entry map.

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `{project_path}\**` (write) | Write CLAUDE.md, AGENTS.md, .cursorrules, _refs.md, _context/ files |
| Filesystem | `<notes>/...` (read) | Reference canonical stack for generated context |

## Handoffs

| Next step | Skill |
|---|---|
| Recommend skills for the project | `skills/meta/skillmaster/SKILL.md` |
| Extract tech stack from existing project | `skills/tech-stack-extractor/SKILL.md` |
| Recommend memory system for this project | `skills/memory/recommender/SKILL.md` |
| Provision the chosen memory system | `skills/memory/advisor/SKILL.md` |
| Run operator for ongoing routing | `skills/operator/SKILL.md` |
| Audit creds in vault vs .env | `skills/secrets-audit/SKILL.md` |

---

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `gather_project_context` | Step 1 — collect project name, slug, stack, bots, LLM preferences | yes | ✅ |
| `generate_claude_md` | Step 2 — render CLAUDE.md template from project context | yes | ✅ |
| `generate_agents_md` | Step 3 — render AGENTS.md template from project context | yes | ✅ |
| `generate_cursorrules` | Step 4 — render .cursorrules template from project context | yes | ✅ |
| `generate_refs_md` | Step 5 — render _refs.md with sibling bot registry | yes | ✅ |
| `generate_lessons_md` | Step 6 — write empty LESSONS.md template | yes | ✅ |
| `generate_memory_config` | Step 7 — write memory-config.yaml skeleton | yes | ✅ |
| `generate_supporting_context` | Step 8 — write WORKFLOW.md, OPEN-ITEMS.md, DECISIONS.md, ug-ug-rules.md to _context/ | yes | ✅ |
| `write_files` | All steps — write generated files to project directory | yes | ⚠️ (Lambda-ready if writing to S3; local disk write for local repos) |

Note: All generation steps are stateless template renders. Full skill is Lambda-compatible as a scaffold generator writing to S3 or a git repo via API.

---

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `project_name` | string | yes | Human-readable project name |
| `project_slug` | string | yes | Short identifier used in file paths and config keys |
| `project_path` | string | yes | Absolute path to project root (e.g. `<project>/...`) |
| `client_name` | string | no | Client name for engagement projects |
| `tech_stack` | string | yes | Primary tech stack (e.g. `Node/TypeScript`, `Python`) |
| `relevant_bots` | string[] | no | Which bots apply to this project (e.g. `[ballparker, qa-auditor]`) |
| `llm_preferences` | object | no | Override default LLM routing table |
| `include_lessons_md` | bool | no | Whether to create LESSONS.md template (default true) |

**Output:**
```json
{
  "status": "ok | error",
  "result": {
    "files_written": [
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>",
      "<path>"
    ],
    "project_slug": "nestgenie",
    "next_steps": [
      "Run skill-recommender to populate the relevant skills section in CLAUDE.md",
      "Run memory-recommender to select memory system and populate _context/memory-config.yaml",
      "Run memory-advisor to provision the chosen memory system"
    ]
  }
}
```
