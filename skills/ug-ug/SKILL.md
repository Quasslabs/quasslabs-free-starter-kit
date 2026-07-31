# SKILL: ug-ug

**Bot:** any · output-mode
**Role:** Token-efficient output mode with 5 compression levels. Caveman language internally; normal prose for user chat unless escalated.
**Ug-ug mode:** none
**Model:** any
**Tool compatibility:** Claude Code · Codex · Cursor
**Status:** stable
**Parallelizable:** yes
**License:** mit
**Origin:** original
**Pack:** core
**Commercial:** ready
**Tier:** free

## When to invoke

Triggers:
- User says "caveman mode", "be more terse", "compressed output", "shorter responses", "ug-ug"
- Long internal reasoning steps need compression (plans, handovers, LESSONS files)
- Slash trigger: `/ug-ug`

## Levels

| Level | Compresses | Use case |
|---|---|---|
| `lite` | Trims openers, removes filler | Default-ish, conversational |
| `medium` | Bullets + symbols in plans + reasoning | Plans, internal docs |
| `full` | Max internal compression; chat replies stay normal prose | Long sessions, multi-step builds |
| `extra-ug` | Compresses chat replies too; deliverables protected | Token-tight sessions |
| `maximum-ug` | Compresses everything including deliverables | Emergency token squeeze |

## Steps

1. Read requested level from user message or slash arg.
2. Apply matching compression rules to non-chat output (plans, reasoning, LESSONS).
3. Keep code blocks + client-facing deliverables uncompressed unless at `maximum-ug`.
4. Never use banned openers: `Let me…`, `I'll go ahead and…`, `Certainly!`, `Sure!`, `Great!`.

## Input

- `level` — one of `lite | medium | full | extra-ug | maximum-ug | none`

## Output

- Compressed text per level, ready to emit.

## Handoffs

- `humanizer` — when output needs to be de-AI-ified for client delivery
- `session-handover` — uses `full` mode for handover docs

## Permissions

None.

## Lambda candidates

None — output transformer only.

## ROI claim

Rule-based pass reduces tokens 10-25% at `full` on prose-heavy inputs (banned openers + filler removed; whitespace collapsed). Defended in `evals/run.py`.
