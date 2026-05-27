# SKILL: task-router

**Bot:** operator · any
**Role:** Pre-flight evaluator. Runs as Step 0 before any skill execution. Returns a routing card that assigns each sub-task to the right AI model, identifies human gates (red = immediate blocker, yellow = note and continue), and estimates cost. Prevents mid-task stalls caused by missing credentials or unclear requirements.
**Ug-ug mode:** lite
**Model:** haiku — routing is deterministic from a fixed decision table; no generation needed
**Tool compatibility:** Claude Code · Cursor · Codex
**Status:** beta
**Parallelizable:** no - routes work to a single local Ollama instance (one GPU); concurrent runs contend for model load

---

## Model

**Verdict:** `phi4-mini` — routing is deterministic from a fixed decision table; no generation needed.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Fixed decision table lookup; no generation needed |
| Local (installed) | phi4-mini | Fast; ideal for classify/route tasks |
| Local (ideal) | phi4-mini | Already installed; perfect fit |

---

## When to invoke

- Automatically: operator calls this before every routing decision (Step 0)
- Manually: "route this task", "who should do this?", "what do I need to unblock this?"
- Any time a new task, story, or skill sequence is about to begin

---

## AI assignment rules

Apply in order — first match wins:

```
Task type                                           → Model              Cost
─────────────────────────────────────────────────────────────────────────────
Classify / route / format / sort / short summarize  → phi4-mini          $0 (local)
Code gen / test write / code fix / PR draft         → qwen2.5-coder:7b  $0 (local)
Planning / orchestration / multi-step analysis      → gemma4:e2b         $0 (local)
Code review with judgment / ambiguous failure       → Sonnet             ~$0.03–0.10
Architecture decision / first-time skill writing    → Sonnet             ~$0.05–0.15
High-stakes judgment / complex trade-off            → Opus               ~$0.15–0.50
Human-only (see gate rules below)                   → ⛔ Human           N/A
```

**Default when uncertain:** try local first. If Ollama output quality is insufficient after 2 attempts, escalate to Sonnet. Log the escalation reason.

---

## Human gate rules

### 🔴 RED — Full blocker. Notify immediately. Do not proceed with this sub-task.

Trigger on any of:
- External service account not yet created (RevenueCat, Twilio, Stripe, Clerk, etc.)
- API key / secret not in Secrets Manager or `.env`
- Billing or legal approval required
- Irreversible action: prod deploy, DB schema migration, PR merge, `git push --force`
- Access credential not available (AWS profile, SSH key, device pairing)

**Action:** Call `notify.red_gate(task, blocker)` immediately. Continue other unblocked tasks. Re-check gate status before retrying the blocked sub-task.

### 🟡 YELLOW — Partial blocker. Note it, work around it, surface in report.

Trigger on any of:
- Config value unknown but can be mocked/stubbed for now
- Requirement ambiguous — can proceed with a stated assumption, flag for review
- Human checkpoint needed at a later stage (not blocking start)
- Environment variable needs confirmation but has a safe default
- External dependency not yet available but not needed until later in the pipeline

**Action:** Record the assumption or gap. Continue work. Include in the session report or morning digest.

---

## Output format

Emit a routing card before any skill execution:

```
┌─ TASK ROUTER ─────────────────────────────────────────────────────────┐
│ Task: [task description — 1 line]                                     │
│                                                                       │
│ AI assignment:                                                        │
│   [Sub-task 1]        → phi4-mini          ($0 local)                │
│   [Sub-task 2]        → qwen2.5-coder:7b  ($0 local)                │
│   [Sub-task 3]        → Sonnet             (~$0.05 cloud)            │
│                                                                       │
│ 🔴 Human gates (BLOCKING — notifying now):                           │
│   □ [Exact action required — e.g. "Add REVENUECAT_KEY to Secrets    │
│     Manager before entitlements step can run"]                       │
│                                                                       │
│ 🟡 Notes (non-blocking — will surface in report):                    │
│   • [Assumption or partial gap]                                      │
│                                                                       │
│ Est. cost: ~$X cloud  +  $0 local                                    │
└───────────────────────────────────────────────────────────────────────┘
```

If no human gates: omit the 🔴 section entirely (do not print "none").
If no yellow notes: omit the 🟡 section.
If fully local: show "Est. cost: $0 (fully local)".

---

## Step-by-step execution

### Step 1 — Parse the task

Extract:
- What is being built or done (the deliverable)
- What systems it touches (API, DB, external service, file, device)
- What the output is (code, report, deploy, PR, etc.)

### Step 2 — Break into sub-tasks

Split the task into the smallest independent steps. Each step gets its own model assignment.

Examples:
```
Task: "Implement entitlement gate on /api/word/save"
Sub-tasks:
  1. Plan implementation steps         → gemma4:e2b
  2. Write UserService.isEntitled()    → qwen2.5-coder:7b
  3. Add gate middleware               → qwen2.5-coder:7b
  4. Write unit + integration tests    → qwen2.5-coder:7b
  5. Review PR before merge            → Sonnet
```

### Step 3 — Check gates

For each sub-task, check:
- Does it require a credential, account, or external service that may not exist?
- Is it irreversible?
- Does it require a human decision before the AI can proceed?

Flag RED or YELLOW accordingly.

### Step 4 — Emit routing card

Print the routing card. If RED gates exist, call `notify.red_gate()` before printing.

### Step 5 — Hand off to operator

Operator uses the routing card to:
- Set the `FLAGS` in its routing block
- Override model selection in downstream skill calls
- Pause on RED-blocked sub-tasks; proceed with others

---

## Common task → model mappings (quick reference)

| Task | Model |
|---|---|
| Classify email as bug / addition / change | phi4-mini |
| Route a request to the right bot | phi4-mini |
| Generate user story from storyboard data | qwen2.5:7b |
| Write a code fix from a test failure | qwen2.5-coder:7b |
| Generate test stubs from AC | qwen2.5-coder:7b |
| Write a PR description | qwen2.5-coder:7b |
| Plan implementation steps for a feature | gemma4:e2b |
| Office hours on a new feature idea | gemma4:e2b |
| Review PR for production readiness | Sonnet |
| Diagnose ambiguous multi-file failure | Sonnet |
| Architecture decision (data model, service boundary) | Sonnet |
| Write a new SKILL.md from scratch | Sonnet |
| High-stakes legal / billing / security judgment | Opus |

---

## Key rules / constraints

- **Always emit the routing card before execution.** Skipping it means human gates surface mid-task and stall work.
- **RED gates trigger notify immediately.** Do not buffer them until the report.
- **Escalate local → cloud only after 2 failed attempts.** Log: model used, prompt summary, why output was insufficient.
- **Do not assign cloud model if local can do it.** Cost discipline is part of the routing decision.

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Network | `http://localhost:11434` | Assign + dispatch sub-tasks to the local Ollama models |
| MCP | `mcp__aws__*` | Check Secrets Manager presence when evaluating RED credential gates |

## Handoffs

| Next step | Skill |
|---|---|
| Execute routing decision | `skills/operator/SKILL.md` |
| Send red-gate alert | `skills/notify/SKILL.md` |
| Call local Ollama model | `skills/local-runner/SKILL.md` |
| Annotate plan steps with LOCAL/CLOUD routing | `skills/ollama-task-router/SKILL.md` |

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `parse_task` | Step 1 — extract deliverable, systems touched, output type from task string | yes | ✅ |
| `split_subtasks` | Step 2 — decompose task into independent steps for model assignment | yes | ✅ |
| `assign_model` | Step 2 — apply AI assignment rules table, return model per sub-task | yes | ✅ |
| `check_gates` | Step 3 — evaluate each sub-task for RED/YELLOW gate conditions | yes | ✅ |
| `emit_routing_card` | Step 4 — format and return the routing card block | yes | ✅ |
| `notify_red_gate` | Step 4 — call notify.red_gate() for each blocking gate (HTTP to Telegram API) | yes | ✅ |

All steps are stateless and deterministic from fixed rule tables — strong Lambda candidates. The full task-router pipeline fits in a single Lambda invocation: receive task → parse → split → assign models → check gates → emit card + notify. No Step Functions needed unless gate resolution requires waiting for human response (Step Functions WaitForTaskToken pattern).

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `task` | string | yes | Plain-language description of what needs to be done |
| `systems` | string[] | no | Known systems the task touches (API, DB, external service); inferred if omitted |
| `context` | object | no | Active session state: current slug, open gates, recent model escalations |

**Output:**
```json
{
  "status": "ok | blocked",
  "routing_card": {
    "task": "Implement entitlement gate on /api/word/save",
    "ai_assignment": [
      { "subtask": "Plan implementation steps", "model": "gemma4:e2b", "cost": "$0 local" },
      { "subtask": "Write UserService.isEntitled()", "model": "qwen2.5-coder:7b", "cost": "$0 local" },
      { "subtask": "Review PR before merge", "model": "Sonnet", "cost": "~$0.05 cloud" }
    ],
    "red_gates": [
      { "subtask": "Entitlements step", "blocker": "REVENUECAT_KEY not in Secrets Manager", "action": "Add to Secrets Manager us-east-1" }
    ],
    "yellow_notes": [
      "Assumption: existing User model has an id field"
    ],
    "estimated_cost": "~$0.05 cloud + $0 local"
  }
}
