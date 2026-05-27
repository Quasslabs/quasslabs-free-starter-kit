# SKILL: skill-builder

**Bot:** any  
**Role:** Draft, test, and iterate on new skills for the the skills hub hub. Knows ug-ug levels, MindPalace patterns, GStack model routing, RAG patterns, and checks items_of_note repos and tech-stack before building. Outputs a SKILL.md ready for wip\ promotion.  
**Ug-ug mode:** full  
**Model:** sonnet — drafting and reasoning required; structure + prior art checks use Haiku  
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** beta
**Parallelizable:** no — writes wip/ skill folders; serialize across concurrent runs

---


## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | (skill-specific - see Steps) | Per-skill read/write paths |
| Network | (skill-specific - see Steps) | Per-skill API calls |
| Bash | (skill-specific - see Steps) | Per-skill tools |

*Note: v2 backfill defaults 2026-05-20. Refine when skill is next edited.*


## Model

**Verdict:** `sonnet` — drafting new SKILL.md content requires reasoning and structured generation across multiple phases.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | sonnet | Drafting + prior art reasoning + checklist evaluation |
| Local (installed) | qwen2.5:7b | General reasoning; adequate for structured skill drafts |
| Local (ideal) | qwen2.5:72b (not installed) | Full reasoning capability for high-quality skill drafting |

---

## When to invoke

- "Build me a skill for X"
- "I need a new skill that does Y"
- "Write a SKILL.md for Z"
- "We're missing a skill for [task/bot/integration]"
- "Turn this workflow into a skill"
- Before building any new skill from scratch
- After `agent-setup-wizard` flags a missing skill in Phase 9 gap check

---

## Mode — draft from source (scaffolder)

To start from a scaffold instead of a blank page (pattern from `virgiliojr94/book-to-skill`):

```
python skills/meta/skill-builder/draft_skill.py --name <slug> --source <doc.md|.txt> --bot "<bots>"
python draft_skill.py --name <slug> --desc "<what it should do>" --bot reporter
```

Takes a source doc (repo README, parsed PDF, markdown) or a `--desc`, drafts a SKILL.md against
the house template via `qwen2.5-coder:14b` (Mac mini), and writes a `wip/<slug>/` triad.

**Draft gate (anti-sprawl — do not bypass):** output is ALWAYS `Status: draft`, never registered
and never auto-promoted. A mediocre auto-skill is worse than none. Required human path before it
reaches the hub: **review/edit → `lint_skill.py` → set `Status: beta` → registry-backfill + sync-audit.**
The scaffolder refuses to overwrite an existing folder and forces `Status: draft` even if the model emits otherwise.

---

## Phase −1 — Touched-skill rule (run BEFORE Phase 0 if editing existing skill)

If you are editing an EXISTING skill's SKILL.md (not creating a new one):

1. `python skills/meta/skill-linter/lint_skill.py <path-to-SKILL.md>`
2. If output contains `WARN [schema-v2]`: the file is on the old schema. As the FIRST edit, add:
   - `**Status:**` header (infer: wip → `beta` if LESSONS has dated entries, else `draft`; ready → `stable`; deprecated tag → `deprecated`)
   - `**Parallelizable:**` header (infer: read-only steps → `yes`; shared mutable state → `no`; bounded → `conditional — [reason]`)
   - `## Permissions` section (extract bash/MCP/file/network patterns from the existing Steps)
3. Re-run linter — must drop the `schema-v2` WARN.
4. Append a row to `skills/BACKFILL-LOG.md`.
5. ONLY THEN proceed with the original edit task.

If you are CREATING a new skill: skip this phase; the template in Phase 5 already includes the v2 fields.

See `skills/BACKFILL-LOG.md` for full rule + defaults.

---

## Phase 0 — Prior art check (always run this first)

Before writing a single line of SKILL.md:

### 1. Check skill inventory in CLAUDE.md

Read `skills/CLAUDE.md` → scan the wip\, ready\, and live\ tables. Does a skill already exist for this?
- If yes: extend or pattern-match against it, don't duplicate
- If close match: note what's different and add it as a variant or additional phase

### 2. Check items_of_note repos

Read `<notes>/...` — pull-in repos used as dependencies.  
Read `<notes>/...` — full triage table with verdicts.

Key questions:
- Is there a starred repo that already implements this pattern?
- Does anything in the triage table have a "pull in" verdict for this use case?
- If yes: reference it in the skill's Handoffs section and note the dependency

### 3. Check canonical tech stack

Read `<notes>/...`.

Key questions:
- Is the proposed skill using the canonical stack (Python, Lambda, DynamoDB, S3, Step Functions, Sonnet/Haiku)?
- If the skill requires a new technology not in the stack, flag it before building

### 4. Check Scope Master mirror

Read `<project>/Scope Master\docs\external-repos-scope-master-map.md`.

Key questions:
- Does the scope-master already have something similar for this domain?

---

## Phase 1 — Intake

Collect from the user or infer from the task description:

```
Skill name:        [kebab-case name]
Bot(s) it serves:  [ballparker | scope-master | deployer | qa-auditor | developer | any]
What it does:      [plain language — one paragraph]
Inputs:            [what data/files/params come in]
Outputs:           [what gets returned/written]
Frequency:         [one-off | on-demand | scheduled | pipeline step]
Users:             [human PM | agent | Lambda | Step Functions]
Existing examples: [any similar skills to pattern after]
```

---

## Phase 2 — Ug-ug level assignment

Pick the correct level based on who reads the output:

| Output audience | Ug-ug level | Output style |
|---|---|---|
| PM, client, human reads the result | `none` | Full prose, complete sentences, formatted nicely |
| Internal agent reasoning → structured output | `lite` | Compressed reasoning; exact paths; skip padding |
| Build/deploy/test pipelines | `full` | Max compression; terse commands; no explanation unless asked |
| Log-watcher, Lambda ops, real-time alert handlers | `ultra` | One-line outputs only; no prose; machine-readable first |

**Decision rules:**
- If a human PM or client will read the skill's output → `none`
- If skill routes to another skill or feeds a pipeline → `lite`
- If skill runs `terraform`, `aws`, `docker`, or `git` commands → `full`
- If skill processes CloudWatch, SQS, or EventBridge events → `ultra`

---

## Phase 3 — RAG assessment

Determine if the skill needs semantic retrieval, exact-match caching, or no caching:

| Pattern | Use when | Implementation |
|---|---|---|
| **No cache** | One-off tasks, user-specific context | Just run the LLM call |
| **Exact-match cache** | Same inputs produce same outputs (market research, competitor lists, milestone templates) | `resolve-or-generate` skill — SHA-256 fingerprint → DynamoDB + S3 |
| **RAG / semantic lookup** | Fuzzy matching, "find similar past X", knowledge base queries | AgentCore Knowledge Bases (native, no infra) or HKUDS/RAG-Anything (starred repo) |
| **Hybrid** | Cache exact hits, fall back to RAG for near-matches | resolve-or-generate with vector similarity layer |

**Decision rules:**
- Skill produces repeatable outputs from structured inputs → exact-match cache (`resolve-or-generate`)
- Skill retrieves from a growing corpus (past estimates, past transcripts, past designs) → RAG via AgentCore KB
- Skill does fuzzy matching or "similar to" lookups → RAG or difflib (for small sets)
- Skill is purely generative with unique context each time → no cache needed

If RAG applies: note the AgentCore KB ARN or S3 knowledge base path in the skill's Input spec. If using resolve-or-generate: reference `skills/resolve-or-generate/SKILL.md`.

---

## Phase 4 (formerly 3) — GStack model routing

Assign the right model to each step the skill will run:

| Model | Use when |
|---|---|
| `claude-haiku-4-5` | Deterministic extraction, formatting, routing from a fixed list, ETL, simple classification |
| `claude-sonnet-4-6` | Reasoning, drafting, research synthesis, code generation, semantic matching, multi-step logic |
| `claude-opus-4-6` | Architecture trade-offs, high-stakes judgment, ambiguous constraints, legal/contract review |

**Rules:**
- Step is deterministic (format, convert, route, classify from a fixed list) → Haiku
- Step requires understanding context or generating content → Sonnet
- Step requires judgment across competing constraints → Opus
- Default for new skills → Sonnet (upgrade if quality low, downgrade if it's pure formatting)

Include model recommendations in the skill's Lambda candidates section.

---

## Phase 4 — MindPalace pattern (if applicable)

Determine if the skill needs persistent memory across sessions:

| Use case | Memory approach |
|---|---|
| Single-run, stateless | None — no memory needed |
| Skill needs to remember prior decisions | Load HANDOVER.md at session start (`session-handover` skill) |
| Cross-session persistent state | `agent-memory` skill (DynamoDB + S3 by job_id) |
| Deployed AgentCore | SESSION_SUMMARY built-in |

For most wip\ skills: no memory needed — the pipeline input carries all context.  
For operator/orchestrator skills: reference HANDOVER.md and session-handover skill.

---

## Phase 5 — Write SKILL.md

Use this exact structure. Do not skip sections.

```markdown
# SKILL: [skill-name]

**Bot:** [bot-names separated by · ]  
**Role:** [one-line description — what it does, not how]  
**Ug-ug mode:** [none | lite | full | ultra]  
**Model:** [haiku | sonnet | opus] — [one-line reason]  
**Tool compatibility:** [Claude Code · Codex · Cursor — list what applies]

---

## When to invoke

- [trigger phrase 1]
- [trigger phrase 2]
- [condition: when X happens]

---

## Input spec

[JSON or table showing what comes in]

---

## Phase 1 — [First major step]

[Instructions]

---

## Phase N — [Last step]

[Instructions]

---

## Lambda candidates

[List which steps are deterministic enough to be functions — pure Python, ETL, formatting]
[Format: - Step name: reason it's a function candidate]
[If no steps qualify: "- None — all steps require LLM reasoning"]

---

## Handoffs

| Next step | Skill |
|---|---|
| [what comes next] | [path to that skill] |
```

**Required sections:** When to invoke, at least one Phase, Lambda candidates, Handoffs.  
**Optional:** Input spec, Output spec, examples/, templates/, schemas/ subdirs.

---

## Phase 6 — Self-check before saving

Run through this before writing the file to disk:

```
[ ] Required header fields present (# SKILL, **Bot:**, **Role:**, **Ug-ug mode:**, **Model:**, **Tool compatibility:**, **Status:**, **Parallelizable:**)
[ ] Status is one of: draft | beta | stable | deprecated (new wip/ skills default to `beta`; `draft` if untested)
[ ] Parallelizable is one of: yes | no | conditional — [reason]; declares shared-state conflicts explicitly
[ ] `## Permissions` section present with bash/MCP/file/network patterns the skill needs
[ ] Ug-ug level is appropriate for the output audience (Phase 2 rules)
[ ] RAG/cache decision made — exact-match cache, RAG, hybrid, or none (Phase 3 rules)
[ ] GStack model assigned to overall skill AND to each LLM step (Phase 4 rules)
[ ] MindPalace memory pattern decided — none, HANDOVER.md, agent-memory, or AgentCore (Phase 5 rules)
[ ] "When to invoke" has at least 3 trigger phrases
[ ] At least one Phase with step-by-step instructions
[ ] Lambda candidates section written (even if "None")
[ ] Handoffs section written with exact <path> paths
[ ] No hardcoded engagement-specific content (must be reusable across projects)
[ ] No duplicate — prior art check (Phase 0) confirmed this is new
[ ] Operating-principles block included at bottom of SKILL.md (study existing patterns · keep changes small · match style · validate early · favour readability · declare conflicts)
```

If any box is unchecked: fix it before saving.

---

## Phase 7 — Update skills hub

After saving the new skill file, call skills-hub-updater to keep the HTML dashboard current:

```
python skills/skills-hub-updater/update_hub.py --skill <path-to-new-SKILL.md>
```

skills-hub-updater reads the new SKILL.md header, determines the correct category, inserts a skill card, and updates the total count in `the skills hub-hub-summary.html`.

---

## Phase 8 — Queue integration suggestions

After the hub is updated, call skill-integration-advisor to identify wiring opportunities with existing skills:

```
skill: skill-integration-advisor
new_skill_path: <path-to-new-SKILL.md>
```

skill-integration-advisor compares the new skill against all existing skills and appends caller/callee/overlap suggestions to `skills/SUGGESTIONS.md`. These are reviewed at the start of the next skill-building session.

---

## Phase 7 — Evaluate and iterate (optional but recommended)

After writing the SKILL.md, optionally run a grading pass:

1. **prompt-grader**: Paste each Phase prompt into `skills/prompt-grader/SKILL.md` to score it 0-100. Target ≥85 before deploying.
2. **Test it**: Give the skill to the target bot with a real input. Does it produce the right output?
3. **Iterate**: If score < 85 or output is off, revise the prompts and re-grade.

The installed Cowork `skill-creator` skill can also run the draft→test→evaluate→improve loop with eval viewer and blind comparison. Use it for fine-tuning after the structure is set.

---

## Phase 8 — Add to CLAUDE.md inventory

After writing the skill to disk at `skills/[skill-name]\SKILL.md`:

1. Add a row to the **wip\ (under development)** table in `skills/CLAUDE.md`:
   ```
   | `skill-name` | [bot] | [one-line description] |
   ```
2. If the skill has Lambda candidates: add a row to the **Lambda / Step Functions Priority List**:
   ```
   | ⭐ | [bot / skill] | [why it's a function] | [EventBridge / Step Functions pattern] |
   ```
3. If the skill is for a new bot not in the registry: add the bot to the **Bot Registry** section.

---

## Output

The final deliverable is:

```
skills/[skill-name]\SKILL.md  ← the skill, ready to test
```

Optionally:
```
skills/[skill-name]\examples\   ← example inputs/outputs
skills/[skill-name]\templates\  ← reusable templates
skills/[skill-name]\schemas\    ← JSON schemas for input/output validation
```

---

## Memory

**Recommended:** context-engine — multi-turn skill construction sessions with large knowledge base

## Lambda candidates

- Phase 0 (prior art check): pure file reads → Lambda or pure Python
- Phase 6 (self-check): pure boolean checklist → Lambda
- Phases 1, 2, 3, 4: light LLM (Haiku for classification, Sonnet for drafting) → can be Lambda-triggered

Full skill-builder pipeline: API Gateway POST `{ task_description }` → Phase 0 lookup → Phase 1 intake → draft SKILL.md → Phase 6 self-check → return file.

---

## Handoffs

| Next step | Skill |
|---|---|
| Grade each prompt in the new skill | `skills/prompt-grader/SKILL.md` |
| Set up a new agent using the skill | `skills/lifecycle/agent-setup-wizard/SKILL.md` |
| Generate IAM roles if skill has Lambda steps | `skills/iam-advisor/SKILL.md` |
| Deploy the skill's Lambda candidates | `skills/deployer/ballparker-aws/SKILL.md` |
| Run draft→test→evaluate→improve loop | Cowork skill-creator (installed) |
