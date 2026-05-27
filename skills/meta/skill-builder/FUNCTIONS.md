# Functions — skill-builder

## Pure functions (Lambda candidates)

| Function | Signature | What it does | Lambda? |
|---|---|---|---|
| `parse_task_scope` | `parse_task_scope(task: str, files: list[str]) -> dict` | Turns a scoped build request into file, test, and constraint metadata. | ✅ |
| `select_template_or_tool` | `select_template_or_tool(task_type: str, constraints: dict) -> str` | Chooses the deterministic template, CLI, or helper path for the task. | ✅ |
| `build_file_plan` | `build_file_plan(scope: dict, repo_state: dict) -> list[dict]` | Produces an ordered list of candidate file operations for review. | ✅ |
| `validate_generated_paths` | `validate_generated_paths(paths: list[str], root: str) -> tuple[bool, list[str]]` | Ensures generated paths stay inside the intended workspace. | ✅ |
| `summarize_diff_metadata` | `summarize_diff_metadata(changes: list[dict]) -> dict` | Counts touched files, modules, and test surfaces without interpreting code intent. | ✅ |

## AI-assisted steps

| Step | Model | Why AI | Est. tokens |
|---|---|---|---|
| Generate or refactor implementation plan | sonnet | Code changes require reasoning about existing patterns and contracts. | ~900 |
| Write code or test text | sonnet | Produces coherent code, test names, or template edits from structured inputs. | ~800 |
| Summarize diff intent | haiku | Condenses changed-file metadata into a fixed summary shape. | ~250 |

## Agents and ug-ug

| Item | Value | Notes |
|---|---|---|
| Bot/agents | any | Draft, test, and iterate on new skills for the the skills hub hub. Knows ug-ug levels, MindPalace patterns, GStack model routing, RAG patterns, and checks items_of_note repos and tech-stack before building. Outputs a SKILL.md ready for wip\ promotion. |
| Ug-ug mode | full | Declared by SKILL.md metadata. |
| Ug-ug recommendation | full | Use for extraction depth and handoff style. |

## External services

| Service | Endpoint | Auth |
|---|---|---|
| GitHub | https://api.github.com and gh CLI | GitHub token or gh auth |
| AWS | AWS APIs via CLI/SDK | AWS profile or IAM role |
| Anthropic / Claude | Anthropic API or Claude app runtime | API key or app session |
| Local container services | Docker daemon or localhost service ports | local machine access |

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
| Separate planning, execution, and verification outputs. |
| The skill is useful only when a later agent can see what changed and how it was checked. |
| Extract deterministic helpers before calling AI for skill-builder. |
| Parsing, validation, routing, and manifests are cheaper and safer as pure functions. |
| Make handoffs explicit instead of relying on chat context. |
| Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. |

## Lambda candidate assessment

skill-builder is partly Lambda-ready because its parsing, validation, routing, grouping, and formatting work can be implemented as stateless helpers. Any local file state should move to S3 and any repeated run state should move to DynamoDB. If the skill invokes AI, use Step Functions to pass deterministic inputs to the selected model and persist structured output. Local tools, desktop apps, or long-running commands should remain external runners invoked from the serverless workflow.
