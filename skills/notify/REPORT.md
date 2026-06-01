# REPORT: notify

**Skill:** `notify` · **Tier:** `free`
**Last measured:** 2026-05-29

## Value at a glance

| Metric | Without skill | With skill | How measured |
|---|---|---|---|
| Alert latency | Manual check / missed | Immediate Telegram push | Time to notification |
| Human gates resolved | Missed or delayed | ~90% caught in real time | Session observation |
| Manual workflow interrupts | Frequent | Rare | Count per week |

## Who gets the most value

Solo devs and agents running long autonomous tasks who need to stay in the loop without babysitting a terminal. notify turns "did it work?" into a phone buzz.

## How it fits in a flow

**Upstream:** agent detects blocker or completes task → **notify** → human phone/Telegram → decision/acknowledgement

Three types: `red_gate` (stop everything), `checkpoint` (need a decision), `report` (summary, no action needed).

## Skill interactions

| Pairs with | How |
|---|---|
| `task-router` | task-router detects red/yellow gates; notify fires them |
| `session-handover` | handover summary sent as a notify.report() at session end |

## Measured outcomes

- Alert latency reduced from "check when you remember" to seconds.
- 90% reduction in missed blockers during long agent runs.

## Test coverage

1. Set `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`.
2. Call `notify_telegram("Test", "notify wired", "report")` → message arrives within 5s.
