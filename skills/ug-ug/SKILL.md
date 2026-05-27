---
name: ug-ug
description: Token-efficient output mode. Triggers - "ug-ug", "ug-ug medium/full", "ug-ug extra-ug", "ug-ug maximum", "be terse", "compress". 5 levels - lite, medium, full, extra-ug, maximum-ug.
---

# SKILL: ug-ug

**Bot:** any
**Role:** Graded terse-output mode — 5 levels from light brevity to full compression, with explicit carve-outs so client-facing deliverables stay readable. Patterned on JuliusBrussee/caveman, extended into a leveled system with an enforcement hook.
**Ug-ug mode:** none
**Model:** none — a style directive the host model (Claude / Codex / Cursor) applies natively; NO local infra required. `phi4-mini` is an OPTIONAL accelerator for the batch `ug-ug-compress` sub-skill only.
**Tool compatibility:** Claude Code · Cursor · Codex
**Origin:** derived-from:https://github.com/juliusbrussee/caveman
**Status:** stable
**Parallelizable:** yes — pure output-style directive, no shared state.

## Permissions

| Type | Pattern | Why |
|---|---|---|
| (none) | — | output-style directive; no tools, no infra, no network. Runs in-model. |

Source / pattern origin: https://github.com/juliusbrussee/caveman (the terse-output concept; this is an independent, leveled implementation).

---

## When to invoke

- "ug-ug" / "be terse" / "compress" / "save tokens" / "short answers"
- "ug-ug medium" · "ug-ug full" · "ug-ug extra-ug" · "ug-ug maximum" (pick a level)
- `ug-ug-commit` · `ug-ug-review` · `ug-ug-compress` (sub-skills)

---

## The 5 levels (ladder — each step compresses more)

| Level | Internal output (plans/reasoning/todos/LESSONS) | Your chat replies | Deliverables (code comments, client docs, commit msgs/PR replies) |
|---|---|---|---|
| **lite** | trim filler, keep grammar | trim filler | normal |
| **medium** | moderate compression (fragments OK) | normal prose | normal |
| **full** | max compression — telegraphic, symbols, no articles | **normal prose** | normal |
| **extra-ug** | max compression | **ug-ug too** | normal prose — **ALERT before compressing any of these** |
| **maximum-ug** | max compression | ug-ug | ug-ug — **nothing is exempt** |

- `none` = opt-out / full prose everywhere (default for client-facing skills like proposals, legal-docs, humanizer).
- **Default when a user says just "ug-ug"**: `full` (terse internal, normal chat). They must say `extra-ug`/`maximum-ug` to compress chat/deliverables.
- The jump from `full` → `extra-ug` is the one that changes what the USER sees in chat. `extra-ug` still protects deliverables (and warns first); `maximum-ug` removes all protection.

## Compression rules (full and above)

- Drop articles (`a`/`an`/`the`) + filler openers
- Fragments; symbols `->` `+` `~` `=` `/`; numbers over words
- Abbreviate when still exact (`cfg` `ctx` `env` `auth`); stack facts per line
- **Never** abbreviate commands, file paths, variable names — always exact
- Terse != wrong: every fact stays correct

## Deliverable safety (extra-ug)

At `extra-ug`, before compressing any of these, **alert the user first** ("note: ug-ug would compress this commit message / client doc — keep prose? [y/n]") and default to normal prose if unsure:
- code comments + docstrings
- client-facing / human-facing documentation
- GitHub commit messages + PR descriptions/replies
Only `maximum-ug` compresses these without asking.

---

## Enforcement — make it stick

The mode drifts over long sessions because nothing re-asserts it. The companion **ug-ug enforcement hook** re-injects the active level each turn:
- Active level stored in a small state file (e.g. `_context/ug-ug-level`).
- A Claude Code `UserPromptSubmit` hook reads it and prepends a one-line directive ("ACTIVE: ug-ug full — internal terse, chat normal") so the model can't forget.
- Setup via the `update-config` skill / `settings.json` hooks. No Ollama dependency.
- Without the hook, ug-ug still works but relies on instruction-following (may drift).

## Exiting

"normal mode" / "stop ug-ug" / "full responses" -> return to `none` immediately, no comment.

---

## Sub-skills

### ug-ug-commit
Terse Conventional Commits: `feat(auth): add cookie transport to backend middleware`. Type+scope+imperative+what. No "I added"/"This commit". (At `extra-ug`, commit messages stay prose unless the user opts in.)

### ug-ug-review
One-line PR comments, no preamble/praise: `Missing null check on line 42 -- throws if user.profile undefined.`

### ug-ug-compress
Rewrite memory/context docs ~46% smaller: single-line facts, drop soft language + rationale, keep all technical specifics. Run on CONTEXT.md/LESSONS.md/OPEN-ITEMS.md or any >200-line context file. **This is the only sub-skill with an optional local accelerator** (`phi4-mini` batch over files); everything else is in-model.

---

## BANNED openers (full and above) — hard enforcement

Never in plans/reasoning/handovers/internal docs when ug-ug active: "Let me…", "I'll go ahead and…", "I need to…", "Certainly!"/"Sure!"/"Great!", "Of course!", "I'll now…", "In order to…", "This will…", "Also need to…", "Let me explain…". Replace with an action bullet, `->`, or nothing.

**Applies to:** plans · handovers · TodoWrite · reasoning · LESSONS · NOTES.
**Does NOT apply to** (unless `maximum-ug`): chat replies (until `extra-ug`) · code · human-facing deliverables.

---

## Handoffs

- **→ gstack** — pick the model after setting the mode
- **→ operator** — if scope unclear before compressing
- **→ update-config** — install/adjust the enforcement hook

## Lambda / Step Functions candidates

None — in-session output directive. `ug-ug-compress` could batch-run over markdown files as a Lambda, but value is marginal (compression is context-dependent).

## Input / Output spec

Invoked by phrase, not payload. Effect: agent adopts the chosen level for the rest of the session (default `full`). Sub-skill outputs: `ug-ug-commit` -> one commit line; `ug-ug-review` -> one PR comment; `ug-ug-compress` -> rewritten doc, same facts ~46% smaller. Exit on "normal mode".
