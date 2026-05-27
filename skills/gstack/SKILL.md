---
name: gstack
description: Apply gstack AI engineering roles (CEO, architect, QA, designer, security) in a Think->Plan->Build->Review->Ship workflow. Invoke per-role or full pipeline.
---

## Model

**Verdict:** `phi4-mini` — model selection rules are deterministic lookup from a fixed table; no generation needed.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Deterministic rule application; no generation |
| Local (installed) | phi4-mini | Routing/classification from fixed model table |
| Local (ideal) | phi4-mini | Already installed; ideal for stage routing |

---

# gstack -- AI Engineering Team Framework

gstack transforms a single AI session into a virtual engineering team. Each role has
defined responsibilities, a trigger command, and a stop condition. Do not blend roles
in a single response -- one role, one job, one output.

Source: https://github.com/garrytan/gstack

---

## When to invoke

- "Use gstack for this"
- "Run office hours on this idea"
- "Do a CEO/eng/design review"
- "Run QA on this"
- "Security audit"
- "Ship this"
- Starting a new feature or project from scratch

---

## The core workflow

```
Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect
```

Do not skip stages. Each stage produces an artifact that the next stage consumes.

---

## Stage 1: Think -- Challenge assumptions before building

**Command:** `/office-hours`

Role: Skeptical product advisor. Challenge the idea before any code is written.

Produce:
- 3-5 hard questions the idea has not answered
- 1-2 alternative approaches worth considering
- A go/no-go recommendation with rationale

Stop condition: User has answered the hard questions or confirmed direction. Do not code.

---

## Stage 2: Plan -- Lock architecture and design before building

Run all three plan reviews. Each is a separate role.

**`/plan-ceo-review`** -- Business and product fit
- Does this solve a real problem?
- Is the scope right for the milestone?
- What is the simplest version that validates the hypothesis?

**`/plan-eng-review`** -- Technical architecture
- What is the data model?
- Where are the failure points?
- What dependencies are being introduced?
- What is the migration or rollback strategy?

**`/plan-design-review`** -- UX and interface
- What does the user flow look like?
- Where does this surface in the existing UI?
- Does it match the established design system?

Stop condition: All three reviews complete, decisions logged, ready to build.

---

## Stage 3: Build -- Implement

Standard development work. Apply relevant skills (android-build-deploy, staged-test-runner,
dev-server-hygiene, etc.) depending on the stack.

**`/careful`** -- Invoke before any destructive command (file deletes, DB migrations,
force pushes). Produces a warning and asks for explicit confirmation.

**`/guard [path]`** -- Lock edits to a specific directory. Prevents accidental changes
outside the intended scope.

---

## Stage 4: Review -- Catch production bugs before merge

**Command:** `/review`

Role: Senior engineer doing a production-readiness review.

Check in this order:
1. Does the implementation match the plan from Stage 2?
2. Are there null/undefined access paths that could throw?
3. Are error states handled (not just happy path)?
4. Are there N+1 query patterns or performance traps?
5. Is anything hardcoded that should be configurable?
6. Are secrets or credentials anywhere in the diff?

Produce: A numbered list of issues, severity labeled (blocking / non-blocking).
Stop condition: All blocking issues resolved.

---

## Stage 5: Test -- Browser and integration testing

**Command:** `/qa`

Role: QA engineer with browser access. Test with real interactions, not just code review.

Apply the `staged-test-runner` and `e2e-auth-cookie` skills. Then:
1. Walk the happy path manually (or via Playwright)
2. Test at least 2 error/edge cases
3. Test on mobile viewport if applicable
4. Verify auth flows with real cookies (not faked)

Produce: Pass/fail per scenario, list of found issues.

---

## Stage 6: Ship -- Deploy with test coverage audit

**Command:** `/ship`

Role: Release engineer.

Pre-ship checklist:
- [ ] Test coverage audit: no new untested code paths
- [ ] Environment variable audit: all new vars in .env.example
- [ ] Migration audit: any DB changes have a rollback path
- [ ] Branch rules: PR merged to dev, not pushed directly to main
- [ ] Build passes: type-check + test + build all green

Apply `deploy-readiness` skill if available. Do not ship if checklist has open items.

---

## Stage 7: Reflect -- Capture lessons

**Command:** `/reflect`

Role: Engineering lead doing a retrospective.

Produce:
- What worked well (do more of this)
- What caused friction (process to change)
- What was a near-miss (luck, not skill)
- 1-2 items to add to LESSONS.md or a SKILL.md failure table

Stop condition: Lessons written to the relevant context file.

---

## Specialist roles (invoke as needed)

| Command | Role | When to use |
|---|---|---|
| `/cso` | Chief Security Officer | OWASP + STRIDE audit before any public release |
| `/design-shotgun` | Design lead | Generate 4-6 visual variants before committing to one |
| `/design-html` | Frontend engineer | Convert approved design to production-quality HTML/CSS |
| `/architect` | Systems architect | When the data model or service boundary needs a second look |

---

## Key rules / constraints

- **One role per response.** Do not blend CEO review with eng review in the same output.
- **Stages are sequential.** Do not start Build until Plan reviews are complete.
- **`/careful` before destructive commands.** Always. No exceptions.
- **`/review` before `/qa`.** Code review first, then browser testing -- not the reverse.
- **Lessons must land somewhere.** `/reflect` output goes to LESSONS.md or a skill failure
  table. A reflection that is only in the chat is not a lesson -- it is noise.
- **`/guard` when working near shared code.** Any change to auth, middleware, or shared
  utilities should be guarded to prevent accidental scope creep.

---

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Blending plan and build | Architecture decided mid-implementation, causing rework | Run all plan reviews first; lock decisions before writing code |
| Skipping /office-hours | Building the wrong thing confidently | Always challenge assumptions before Stage 2 |
| /review skipped before /qa | QA finds bugs that a code review would have caught in 2 minutes | Review first, then test |
| /reflect skipped | Same mistake made on next project | Make /reflect non-optional; one lesson minimum per shipped feature |
| /careful not invoked | Destructive command executed without confirmation | Add /careful as a habit before any rm, DROP, force push, or migration |

---

## Bot ecosystem integration

gstack is the engineering team simulator. It does NOT replace the bot ecosystem -- it runs
INSIDE an agent session to give it structured roles. Use it together with the bots below.

### How gstack maps to our bots

| gstack stage/role | Our bot | Skill |
|---|---|---|
| Think (/office-hours) | ballparker | transcript-research, market-research |
| Plan (/plan-ceo-review, /plan-eng-review) | scope-master | engagement-bootstrap, storyboard-builder |
| Plan (/plan-design-review) | designer | screen-builder, interactive-proto |
| Build | developer | staged-test-runner, dev-server-hygiene, e2e-auth-cookie |
| Review (/review) | qa-auditor | dev-gate |
| Test (/qa) | qa-auditor | test-creator, staged-test-runner |
| Ship (/ship) | deployer | android-build-deploy, deployer runbooks |
| Reflect (/reflect) | any | memory-ladder (write lessons to context), ug-ug-compress |
| Security (/cso) | qa-auditor | release-gate (includes OWASP section) |

### How to invoke gstack within a bot session

From any bot context, invoke gstack by reading the skill:
  Read: skills/gstack/SKILL.md
  Then invoke the relevant stage command.

From operator routing table:
  Task: Multi-role team simulation -> any bot -> gstack skill
  Task: Engineering review         -> any bot -> gstack /review or /qa
  Task: Ship readiness             -> deployer -> gstack /ship then deployer runbook

### Improvements from our bot patterns (v2 additions)

**1. Ug-ug integration**
All gstack outputs default to ug-ug lite mode (terse, exact paths, no padding).
Switch: /full-output for verbose mode, /ultra for maximum compression.
See: skills/ug-ug/SKILL.md

**2. LLM targeting**
Each stage should target the appropriate model:
- /office-hours, /plan-*: claude-opus-4-6 (deep reasoning)
- /build, /review: claude-sonnet-4-6 (standard coding)
- /qa checklist, classify: claude-haiku-4-5 (fast, cheap)
- Token-heavy context: LLMLingua compression first

**3. Operator routing**
If gstack encounters a request that belongs to a different bot, hand off via operator:
- Bug triage -> qa-auditor/defect-triage
- Cost estimate -> ballparker
- Design artifact -> designer
See: skills/operator/SKILL.md (routing table)

**4. Memory handoff (/reflect enhancement)**
The /reflect output must land in one of:
- LESSONS.md (in the project root)
- memory-ladder (for cross-session persistence): skills/memory/memory-ladder/SKILL.md
- ug-ug-compress pass on the context file before any handoff

**5. QA enhancement (/qa + test-creator)**
Before running /qa, call test-creator to generate the expected test plan from scope docs:
  1. qa-auditor/test-creator reads scope -> generates test plan
  2. gstack /qa validates: does implementation cover the test plan?
  3. Dev-gate passes only when both match
See: skills/qa-auditor/test-creator/SKILL.md

**6. Deliverables (/ship enhancement)**
After /ship checklist passes, use deliverables-export for client-facing outputs:
  skills/deliverables-export/SKILL.md

## Handoffs

- **→ operator** after model selection to route the task to the selected model
- **→ llm-selector** for finer-grained selection when gstack routing is ambiguous
- **→ notify** if no suitable model is available for the task requirements

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `route_stage_command` | Any — map /command to stage and role | yes | ✅ |
| `office_hours` | Stage 1 — challenge assumptions, return 3-5 questions + go/no-go | yes | ✅ |
| `plan_ceo_review` | Stage 2 — business fit check, return structured verdict | yes | ✅ |
| `plan_eng_review` | Stage 2 — architecture review, return data model + failure points | yes | ✅ |
| `plan_design_review` | Stage 2 — UX review, return user flow + design system match | yes | ✅ |
| `review` | Stage 4 — production-readiness code review, return numbered issue list | yes | ✅ |
| `ship_checklist` | Stage 6 — evaluate pre-ship checklist, return pass/fail per item | yes | ✅ |
| `reflect` | Stage 7 — retrospective, return lessons + LESSONS.md write | yes | ✅ |
| `/careful` guard | Inline — intercept destructive command, return warning + confirmation prompt | yes | ✅ |
| `/guard` scope lock | Inline — lock edit scope to a directory, check each change against boundary | no | ❌ |

`/guard` requires stateful session tracking of which paths are in scope — not Lambda-compatible without external state. All review and planning stages are stateless LLM calls and are Lambda-compatible. The full gstack workflow (7 stages sequential) maps to a Step Functions state machine.

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `command` | string | yes | Slash command: `/office-hours`, `/review`, `/qa`, `/ship`, `/reflect`, `/cso`, etc. |
| `context` | string | yes | Code diff, feature description, PR content, or project brief depending on stage |
| `project_path` | string | no | Path to project root; used by `/guard` and `/reflect` for file writes |
| `ug-ug_level` | string | no | `lite` (default) \| `full` \| `ultra` — overrides output verbosity |

**Output:**
```json
{
  "status": "ok | blocked | stop",
  "stage": "think | plan | build | review | test | ship | reflect",
  "role": "office-hours | plan-ceo-review | plan-eng-review | review | qa | ship | reflect",
  "output": "...",
  "stop_condition_met": true,
  "blocking_issues": [
    { "severity": "blocking | non-blocking", "description": "..." }
  ],
  "next_stage": "plan | build | review | test | ship | reflect | done"
}
