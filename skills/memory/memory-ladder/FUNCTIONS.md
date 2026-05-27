# Functions — memory-ladder

## Pure functions (Lambda candidates)

| Function | Signature | What it does | Lambda? |
|---|---|---|---|
| `build_record_key` | `build_record_key(scope_id: str, timestamp: str, record_type: str) -> str` | Generates stable keys for snapshots, memories, or knowledge records. | ✅ |
| `normalize_memory_record` | `normalize_memory_record(record: dict, schema: dict) -> dict` | Applies the expected schema before storing or comparing records. | ✅ |
| `detect_stale_records` | `detect_stale_records(records: list[dict], now: str, ttl_days: int) -> list[dict]` | Finds stale knowledge entries from timestamps and TTL settings. | ✅ |
| `diff_snapshots` | `diff_snapshots(previous: dict, current: dict) -> dict` | Computes added, changed, and removed fields between snapshots. | ✅ |
| `format_memory_context` | `format_memory_context(records: list[dict], limit: int) -> str` | Builds a bounded context block from selected memory records. | ✅ |

## AI-assisted steps

| Step | Model | Why AI | Est. tokens |
|---|---|---|---|
| Classify ambiguous request intent | haiku | Maps natural-language triggers to the documented workflow or handoff. | ~250 |
| Generate task-specific guidance | sonnet | Uses the SKILL.md workflow to produce a contextual recommendation or artifact. | ~600 |
| Summarize outcomes and next steps | haiku | Compresses structured results into a concise handoff. | ~250 |

## Agents and ug-ug

| Item | Value | Notes |
|---|---|---|
| Bot/agents | none | No role line found; derived from documented workflow. |
| Ug-ug mode | none | Declared by SKILL.md metadata. |
| Ug-ug recommendation | none | Use for extraction depth and handoff style. |

## External services

| Service | Endpoint | Auth |
|---|---|---|
| GitHub | https://api.github.com and gh CLI | GitHub token or gh auth |
| Google APIs | https://www.googleapis.com | OAuth or service account |
| AWS | AWS APIs via CLI/SDK | AWS profile or IAM role |
| Ollama | http://localhost:11434 | none for local API |
| Browser automation | local browser, CDP, or scraping runtime | local process access |

## Lambda-equivalent implementation

| Capability | Lambda equivalent | Status |
|---|---|---|
| Input validation | Lambda validates payload shape and required fields. | Ready |
| Deterministic transforms | Lambda runs parsing, grouping, routing, and formatting helpers. | Ready |
| Durable state | S3 or DynamoDB replaces local files when persistence is needed. | Refactor needed |
| AI judgment | Step Functions calls the selected model and passes structured results forward. | Refactor needed |

## Lessons learned

| Lesson | Why it matters |
|---|---|
| Treat the documented failure modes as runtime guardrails. |
| The SKILL.md already names the mistakes this workflow is meant to prevent. |
| Extract deterministic helpers before calling AI for memory-ladder. |
| Parsing, validation, routing, and manifests are cheaper and safer as pure functions. |
| Make handoffs explicit instead of relying on chat context. |
| Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. |

## Lambda candidate assessment

memory-ladder is partly Lambda-ready because its parsing, validation, routing, grouping, and formatting work can be implemented as stateless helpers. Any local file state should move to S3 and any repeated run state should move to DynamoDB. If the skill invokes AI, use Step Functions to pass deterministic inputs to the selected model and persist structured output. Local tools, desktop apps, or long-running commands should remain external runners invoked from the serverless workflow.
