# Functions — local-model-route

## Pure functions (Lambda candidates)

| Function | Signature | What it does | Lambda? |
|---|---|---|---|
| `classify_task_type` | `classify_task_type(task: str) -> str` | Maps a task description to autocomplete, code-edit, PRD summary, estimate review, embeddings, or cloud exception categories. | ✅ |
| `parse_context_need` | `parse_context_need(context_tokens: int) -> str` | Classifies required context as small, medium, or large against the 4k and 16k local thresholds. | ✅ |
| `detect_gpu_conflict` | `detect_gpu_conflict(loaded_models: list[str]) -> dict` | Detects 14B and other 12GB VRAM conflicts before recommending another model. | ✅ |
| `choose_ollama_model` | `choose_ollama_model(task_type: str, context_need: str, privacy: str, loaded_models: list[str]) -> dict` | Applies the routing table and hard limits to pick a local model or cloud exception warning. | ✅ |
| `build_ollama_command` | `build_ollama_command(model: str, context: int | None, keep_alive: str | None) -> str` | Emits the `ollama run` or HTTP generate pattern for the selected model. | ✅ |

## AI-assisted steps

| Step | Model | Why AI | Est. tokens |
|---|---|---|---|
| Classify ambiguous user task descriptions | haiku | Short routing classification when the task type is not explicit. | ~250 |
| Explain a cloud exception without exposing sensitive context | sonnet | Requires judgment about privacy, context slicing, and escalation wording. | ~500 |

## Agents and ug-ug

| Item | Value | Notes |
|---|---|---|
| Bot/agents | any | Can be called by any agent before starting local Ollama work. |
| Ug-ug mode | lite | The skill is mostly a routing table with a few safety checks. |
| Ug-ug recommendation | lite | Extract the routing and VRAM checks, but leave rare cloud-exception judgment to the agent. |

## External services

| Service | Endpoint | Auth |
|---|---|---|
| Ollama local API | `http://localhost:11434/api/generate` | none |
| Ollama CLI | `ollama run`, `ollama serve` | local machine access |
| OpenCode/Aider handoff | local terminal agent loop | local repo access |
| Repomix/mem0-Qdrant handoffs | local tools and services | local config |

## Lambda-equivalent implementation

| Capability | Lambda equivalent | Status |
|---|---|---|
| Task-to-model routing | Lambda function with static routing table and model metadata in environment or DynamoDB | ✅ |
| VRAM/concurrency checks | DynamoDB-backed model lease table instead of local GPU process inspection | ⚠️ |
| Ollama command emission | Return shell/API instructions as JSON without executing them | ✅ |
| Local model execution | Bedrock or SageMaker endpoint invocation instead of local Ollama | ⚠️ |

## Lessons learned

| Lesson | Why it matters |
|---|---|
| Routing is cheap, but wrong routing can overload a 12GB GPU. | The deterministic layer should block 14B plus other generation models before anything launches. |
| Privacy can override model quality. | Proprietary client code should stay local unless a tightly redacted cloud exception is justified. |
| Context length is a resource decision, not just a model flag. | Raising local context to 16k should be explicit because it changes memory pressure. |

## Lambda candidate assessment

The routing portion of local-model-route is stateless and fits Lambda well because it is a fixed decision table plus a few threshold checks. The pieces that inspect actual loaded models or execute `ollama run` are local-machine concerns and are not directly Lambda-compatible. A cloud equivalent would store model availability in DynamoDB and return a routing decision rather than touching the GPU. For real inference, Lambda should hand off to Bedrock, SageMaker, or another managed endpoint rather than attempting to host Ollama.
