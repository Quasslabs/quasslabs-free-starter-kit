# Functions — agent-setup-wizard

## Pure functions (Lambda candidates)

| Function | Signature | What it does | Lambda? |
|---|---|---|---|
| `validate_intake` | `validate_intake(data: dict) -> dict` | Checks task, expected inputs, expected outputs, frequency, users, AWS readiness, and codebase fields. | ✅ |
| `rank_skill_matches` | `rank_skill_matches(task: str, registry: list[dict]) -> list[dict]` | Scores candidate skills from the registry and returns ranked matches with rationale fields. | ⚠️ |
| `assign_ug-ug_level` | `assign_ug-ug_level(skill_type: str, runs_commands: bool, writes_human_file: bool, event_driven: bool) -> str` | Applies the wizard's fixed ug-ug rules to each selected skill. | ✅ |
| `select_memory_pattern` | `select_memory_pattern(use_case: str, cross_session: bool, agentcore: bool) -> dict` | Chooses none, MindPalace, agent-memory, or AgentCore SESSION_SUMMARY. | ✅ |
| `assign_model_route` | `assign_model_route(step: dict) -> dict` | Maps a step to haiku, sonnet, or opus using the GStack routing rules. | ✅ |
| `build_rate_limit_config` | `build_rate_limit_config(endpoint_type: str, users: str) -> dict` | Emits rate, burst, monthly quota, and reserved concurrency defaults. | ✅ |
| `render_operator_config` | `render_operator_config(plan: dict) -> str` | Renders the YAML routing, memory, logging, and rate-limit config. | ✅ |
| `render_claude_md` | `render_claude_md(plan: dict) -> str` | Produces the project CLAUDE.md draft from structured setup decisions. | ✅ |
| `build_gap_check` | `build_gap_check(skills: list[dict], aws_ready: bool) -> dict` | Reports missing skills, missing AWS/IAM work, and next skill handoffs. | ✅ |

## AI-assisted steps

| Step | Model | Why AI | Est. tokens |
|---|---|---|---|
| Interpret a plain-language automation request | sonnet | Needs to infer agent boundaries, outputs, and likely workflow from user language. | ~700 |
| Resolve skill discovery ambiguity | sonnet | Requires semantic matching when multiple skills appear relevant or gaps exist. | ~650 |
| Review architecture-critical setup choices | opus | Use only when the wizard must lock high-impact infrastructure, auth, memory, or model-routing tradeoffs. | ~900 |
| Draft CLAUDE.md and setup summary | sonnet | Produces readable project instructions from the structured setup plan. | ~800 |
| Format routing config from locked decisions | haiku | Converts known fields into YAML and checklist output. | ~250 |

## Agents and ug-ug

| Item | Value | Notes |
|---|---|---|
| Bot/agents | operator · any | Single entry point for new agents and automations. |
| Ug-ug mode | lite | Setup plans need enough prose for humans but compact routing output for machines. |
| Ug-ug recommendation | lite | Keep user-facing setup readable; make generated configs and skill lists dense and structured. |

## External services

| Service | Endpoint | Auth |
|---|---|---|
| Skill registry | `skills/` and `skills/` | local filesystem |
| skill-recommender | `skills/skill-recommender/SKILL.md` | local skill handoff |
| aws-account-bootstrap | `skills/aws-account-bootstrap/SKILL.md` | local skill handoff; AWS auth later |
| iam-advisor | `skills/iam-advisor/SKILL.md` | local skill handoff |
| infra-advisor | `skills/infra-advisor/SKILL.md` | local skill handoff |
| prompt-grader | `skills/prompt-grader/SKILL.md` | local skill handoff |

## Lambda-equivalent implementation

| Capability | Lambda equivalent | Status |
|---|---|---|
| Intake API | API Gateway plus Lambda validates setup JSON and returns missing fields. | Ready |
| Skill discovery | Lambda reads a registry snapshot from S3 or DynamoDB and returns ranked candidates. | Refactor needed |
| Ug-ug/model assignment | Pure Lambda helpers apply fixed routing rules. | Ready |
| Config generation | Lambda renders `operator-config.yaml` and CLAUDE.md to S3. | Ready |
| Multi-step setup | Step Functions chains intake, discovery, gap check, and config render. | Ready |
| Local file writes | Replace direct project-root writes with S3 artifacts or a Git PR workflow. | Refactor needed |

## Lessons learned

| Lesson | Why it matters |
|---|---|
| The wizard is a gate, not just a writer. | It prevents code work before skills, memory, models, rates, logging, and AWS readiness are settled. |
| Ug-ug and model routing should be assigned per step. | One automation often mixes terse ETL, human-readable docs, and high-stakes decisions. |
| Generated config should come from structured decisions. | CLAUDE.md and operator YAML are safer when rendered from a locked plan instead of freehand prose. |
| Gaps are valid output. | Missing skills or AWS/IAM prerequisites should stop the workflow and produce next steps rather than pretending setup is complete. |

## Lambda candidate assessment

Most of this wizard can be implemented as Lambda helpers behind a Step Functions workflow because intake validation, ug-ug assignment, model routing, rate-limit defaults, and config rendering are stateless. Skill discovery needs a registry source that is not the local `<workspace>` filesystem, so a Lambda version should index skill metadata into S3 or DynamoDB. The parts that need stronger AI are bounded: Sonnet handles semantic setup planning and Opus is reserved for irreversible architecture or security choices. Writing CLAUDE.md and operator config locally is the main blocker; return generated artifacts through S3 or a Git PR instead.