# SKILL: reflect

**Bot:** any (developer · qa-auditor · deployer · scope-master · ballparker)  
**Role:** Terminal retrospective step. Run at the end of any project, milestone, or significant flow to capture what worked, what caused friction, and what was a near-miss. Writes lessons to LESSONS.md in the project root and surfaces memory promotions to memory-ladder. Callable by any bot as its final step.  
**Ug-ug mode:** none  
**Model:** sonnet - reasoning, drafting, or research synthesis required
**Tool compatibility:** Claude Code · Cursor · Codex · Cowork
**Status:** beta
**Parallelizable:** conditional - yes across distinct projects; no for two concurrent retros appending the same LESSONS.md

## Model

**Verdict:** `sonnet` — retrospective writing requires synthesizing session context into coherent lessons; sonnet handles this narrative reasoning well.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | sonnet | Reflection and summary writing from session context |
| Local (installed) | llama3.1:8b | General-purpose model capable of structured retrospective writing |
| Local (ideal) | llama3.3:70b (not installed) | Better narrative quality for lesson synthesis |

---

## When to invoke

- At the end of a project, milestone, or sprint
- After a production incident is resolved
- "Run a retro", "reflect on this project", "capture lessons"
- As the terminal step in any bot flow (after ship, after release-gate, after ballpark delivery)
- After any /careful confirmation that was close to a bad outcome
- Invoked automatically by operator after a bot marks a flow as "complete"
- **Note — abrupt session end:** the `stop-hook` skill (`skills/memory/stop-hook/SKILL.md`) fires automatically on every Claude Code session close and handles the minimum flush (timestamp + compress). For a full retro, invoke this skill manually before closing. The stop-hook does NOT run reflect automatically — that is intentional (reflect is heavyweight; stop-hook is lightweight).

---

## Phase 1 — Gather context

Collect the inputs for the retrospective:

```
Project / feature:  [name or Jira project key]
Time period:        [sprint, milestone, or date range]
Bot(s) involved:    [which bots ran during this flow]
Key artifacts:      [SKILL.md files used, output docs, tickets closed]
Incidents:          [any /careful triggers, gate failures, rollbacks, production issues]
```

If running from a bot session, pull context from:
- The session's task list (completed vs. blocked tasks)
- Any GATE: HOLD / GATE: BLOCK verdicts from qa-auditor
- Any /careful confirmations that were required
- Jira tickets closed in this period (via jira-fetch-tickets)

---

## Phase 2 — Four-part retrospective

Produce four short sections. Each item is 1–2 sentences — no padding.

### What worked well (do more of this)
Things that made the flow faster, smoother, or produced better output than expected. Include specific skills, patterns, or decisions.

```
+ arch-review before build caught 2 schema issues before any code was written — saved ~4h
+ story-test-builder output was directly usable; no rewrite needed
+ email-pm-brief daily task list meant PM had zero unread Jira items by end of sprint
```

### What caused friction (change this process)
Anything that slowed down the flow, required rework, or created confusion. Name the specific step that failed, not just the symptom.

```
- ug-ug mode was left on during PM brief generation — PM couldn't parse terse output
- No arch-review before the auth refactor → migration had to be rewritten mid-PR
- /guard not activated → accidental edit to shared middleware caught late in review
```

### Near-misses (luck, not skill)
Things that almost went wrong but didn't. These are the highest-value lessons because they reveal unguarded risks.

```
⚠ git reset --hard almost ran without /careful — caught only because the command was in a script
⚠ Production Jira ticket submitted with wrong priority (Low instead of High for a bug) — caught in PM review
⚠ Slack message to wrong channel — no client saw it, but the risk was real
```

### Lessons to record (1–2 items max)
The 1–2 most important changes to make to a SKILL.md, CLAUDE.md, or LESSONS.md. Be specific — vague lessons don't change behavior.

```
→ LESSONS.md: always activate /guard before any auth or middleware edit
→ SKILL.md (email-pm-brief): add validation that ug-ug mode is OFF before PM brief generates
```

---

## Phase 3 — Write to LESSONS.md

Append the retrospective to `LESSONS.md` in the project root:

```
<project>/...]\LESSONS.md
```

Format:

```markdown
## Retro — [Project / Feature] — [Date]

**What worked:** [bullet list]
**Friction:** [bullet list]
**Near-misses:** [bullet list]
**Actions:**
  - [ ] [LESSONS.md or SKILL.md change] — owner: [bot or human]
  - [ ] [process change] — owner: [bot or human]
```

If `LESSONS.md` doesn't exist: create it.

---

## Phase 4 — Surface memory promotions (memory-ladder Layer 6)

For each friction item or near-miss, evaluate whether it qualifies for memory promotion:

**Promotion trigger:** same failure or near-miss has now occurred 2+ times across any project.

If triggered, produce a promotion block:

```
PROMOTE TO MEMORY:
  [feedback] arch-review must run before any DB migration — burned twice (NestGenie Apr 2026, Tusk Mar 2026)
  [feedback] /guard should be default-on for auth/ and middleware/ directories
  [skill-update] careful-guard SKILL.md: add "auth/" and "middleware/" to auto-guard list
```

Write these to the auto-memory system:
```
skills/.auto-memory/feedback_[topic].md
```

---

## Phase 5 — Skill gap check

At the end of the retro, run a quick skill gap pass:

For each friction point or near-miss, ask: **"Does a skill exist that would have prevented this?"**

If no → emit a skill suggestion:
```
SKILL GAP DETECTED:
  Gap:     No skill for validating ug-ug mode before PM-facing output
  Suggest: Add a pre-output mode validator to email-pm-brief or create a shared output-validator skill
  Priority: Medium
```

These suggestions feed `skill-recommender` on the next session.

---

## Output format (full)

```
REFLECT — [Project] — [Date]
Run by: [bot(s)]

WHAT WORKED
  + [item]
  + [item]

FRICTION
  - [item]
  - [item]

NEAR-MISSES
  ⚠ [item]

LESSONS
  → [specific change, owner]

MEMORY PROMOTIONS
  [list or "none"]

SKILL GAPS
  [list or "none"]

Written to: <project>/...]\LESSONS.md ✓
```

---

## Memory

**Recommended:** memory-ladder Layer 4 — reflection sessions accumulate insight across projects

## Lambda candidates

- Not a Lambda candidate in its current form — requires LLM reasoning and session context
- The **write-to-LESSONS.md** step is Lambda-ready (structured write to S3 or file) once the content is generated
- Pattern: Bedrock agent generates retro → Lambda writes LESSONS.md to GitHub repo via API → Lambda appends to BENCH-INDEX equivalent

---

## Permissions

| Type | Pattern | Why |
|---|---|---|
| Filesystem | `<project>/...` (write) | Append retrospective to the project LESSONS.md (Phase 3) |
| Filesystem | `skills/.auto-memory/feedback_*.md` (write) | Write memory promotions (Phase 4) |

## Handoffs

| Next step | Skill |
|---|---|
| Promote observations to memory | `skills/memory/memory-ladder/SKILL.md` (Layer 6) |
| Identify skill gaps | `skills/meta/skillmaster/SKILL.md` |
| Archive project output | `skills/output-composer/SKILL.md` |
| Next project kickoff | `skills/scope-master/engagement-bootstrap/SKILL.md` |
