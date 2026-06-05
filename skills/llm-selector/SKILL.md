---
name: llm-selector
status: beta  # v2-backfill 2026-05-31: auto-inferred, verify before ready/ promotion
parallelizable: yes  # v2-backfill 2026-05-31: auto-inferred, verify before ready/ promotion
description: Recommend the optimal LLM for a skill with fallback chain + cost estimate. Use when picking a model or reviewing cost. Covers cloud + local providers.
---

## Model

**Verdict:** `phi4-mini` — model selection evaluation uses fixed tier rules and catalog lookups; no deep reasoning required.

| Tier | Pick | Notes |
|---|---|---|
| Cloud | haiku | Tier classification + catalog lookup is deterministic |
| Local (installed) | phi4-mini | Fast classification; fixed decision table |
| Local (ideal) | phi4-mini | Already installed; fits S0-level routing task |

---

# llm-selector — LLM Evaluation and Recommendation

You are evaluating a SKILL.md to determine the best LLM for it, produce a ranked
recommendation with reasoning, a fallback chain, validation tests, and a cost estimate.
The goal is to avoid defaulting to the most expensive model when a cheaper one is
sufficient — and to document the reasoning so it can be audited.

---

## When to invoke

- "Which LLM should I use for this skill?"
- "Is Sonnet the right choice here?"
- "Give me a model recommendation for this agent"
- "Optimize model selection for cost"
- "Run llm-selector on this skill"
- Any SKILL.md that does not include a `## Model Selection` section

---

## What this skill produces

1. **Task classification** — what type of work this skill actually does
2. **Model recommendation** — primary + ranked fallbacks with reasoning
3. **Validation test suite** — 3–5 prompts to run against candidate models
4. **Cost estimate** — per-run tokens, estimated time, estimated $ at current pricing
5. **Model selection block** — ready-to-paste `## Model Selection` section for the SKILL.md

---

## Step 1 — Read and classify the skill

Read the SKILL.md. Extract:
- **Output type**: code generation / text generation / data extraction / reasoning / classification / summarization / structured JSON / image analysis / multi-step orchestration
- **Context size**: how much input context is expected (small <8K / medium 8–32K / large 32K+)
- **Output length**: short <500 tokens / medium 500–2K / long 2K+
- **Reasoning depth**: none / shallow (1–2 hops) / moderate (3–5 hops) / deep (chain-of-thought, multi-step deduction)
- **Accuracy stakes**: low (draft/creative) / medium (internal tooling) / high (client-facing, financial, legal, medical)
- **Latency sensitivity**: batch-ok / interactive (< 5s) / real-time (< 1s)
- **Tool/function use**: none / basic (1–3 tools) / complex (4+ tools, nested calls)
- **Self-learning required**: yes / no (see agent-memory skill)

Assign a **complexity tier**:

| Tier | Profile |
|---|---|
| **S0 — Nano** | Classification, routing, short extraction, yes/no decisions. No multi-hop reasoning. Output < 200 tokens. |
| **S1 — Micro** | Structured extraction, simple summarization, templated generation. Moderate accuracy. Output < 1K tokens. |
| **S2 — Standard** | Multi-step reasoning, code generation, tool use, document analysis. Medium context. Output < 4K tokens. |
| **S3 — Advanced** | Deep reasoning, long-context synthesis, complex orchestration, high-stakes output. Output 4K+ tokens. |
| **S4 — Expert** | Financial modeling, legal analysis, autonomous multi-agent orchestration, PhD-level research. Errors are costly. |

---

## Step 2 — Select candidate models

Use the tier from Step 1 to determine the candidate pool.

### Model catalog (as of April 2026)

#### Anthropic (direct or via Bedrock)
| Model | Tier fit | Context | Strengths | $/1M in | $/1M out |
|---|---|---|---|---|---|
| Claude Haiku 4.5 | S0–S1 | 200K | Fast, cheap, good extraction | $0.80 | $4.00 |
| Claude Sonnet 4.6 | S2–S3 | 200K | Best all-round, coding, tool use | $3.00 | $15.00 |
| Claude Opus 4.6 | S3–S4 | 200K | Highest reasoning, complex orchestration | $15.00 | $75.00 |

#### OpenAI
| Model | Tier fit | Context | Strengths | $/1M in | $/1M out |
|---|---|---|---|---|---|
| GPT-4o mini | S0–S1 | 128K | Cheap, fast, good JSON | $0.15 | $0.60 |
| GPT-4o | S2–S3 | 128K | Strong coding + vision | $2.50 | $10.00 |
| o3-mini | S3–S4 | 200K | Deep reasoning, math, science | $1.10 | $4.40 |
| o1 | S4 | 200K | Research-grade reasoning | $15.00 | $60.00 |

#### AWS Bedrock (native / cheapest at scale)
| Model | Tier fit | Context | Strengths | $/1M in | $/1M out |
|---|---|---|---|---|---|
| Amazon Nova Micro | S0 | 128K | Fastest, cheapest on Bedrock | $0.04 | $0.14 |
| Amazon Nova Lite | S0–S1 | 300K | Low cost, multimodal | $0.06 | $0.24 |
| Amazon Nova Pro | S1–S2 | 300K | Balanced, good for enterprise workflows | $0.80 | $3.20 |
| Llama 3.3 70B | S1–S2 | 128K | Open weights, strong reasoning for cost | $0.72 | $0.72 |
| Llama 3.1 405B | S2–S3 | 128K | Near-frontier open model | $2.40 | $2.40 |
| Mistral Large 2 | S2–S3 | 128K | Strong code and multilingual | $2.00 | $6.00 |

#### Open / Self-hosted (via Bedrock, Ollama, or API)
| Model | Tier fit | Context | Strengths | Cost note |
|---|---|---|---|---|
| Qwen 2.5 72B | S1–S3 | 128K | Strong coding, multilingual, cost-efficient | Self-host or Bedrock |
| Qwen 2.5-Coder 32B | S2 | 128K | Best open-source code model | Self-host |
| DeepSeek R1 | S3–S4 | 64K | Near-o1 reasoning, much cheaper | $0.55 / $2.19 |
| DeepSeek V3 | S2–S3 | 128K | Strong general, coding | $0.27 / $1.10 |
| Llama 3.2 3B / 1B | S0 | 128K | Edge inference, near-zero cost | Self-host only |

---

## Step 3 — Generate validation tests

Write 3–5 test prompts that represent the skill's actual workload. For each:
- **Input**: a realistic sample input the skill would receive
- **Expected output shape**: what a correct response looks like (not exact text)
- **Pass criterion**: how you would judge whether the model succeeded

Test types to cover:
1. **Happy path** — standard input, typical output
2. **Edge case** — unusual input, boundary condition
3. **Accuracy check** — output that can be verified as correct/incorrect
4. (Optional) **Latency test** — flag if response time matters
5. (Optional) **Cost floor test** — run on the cheapest plausible model to see if it passes

Format:
```
TEST 1 — [test type]
Input: [sample input]
Expected: [shape of correct output]
Pass if: [judgment criterion]
Run on: [model(s) to test]
```

---

## Step 4 — Produce the recommendation

Output a ranked model list:

```
PRIMARY:   [Model name]
REASON:    [Why this model fits the task tier and profile]
PROVIDER:  [Anthropic / OpenAI / AWS Bedrock / self-hosted]

FALLBACK-1: [Model name]
REASON:     [Acceptable trade-off — slightly less capable but cheaper/faster]

FALLBACK-2: [Model name]
REASON:     [Budget fallback — use only if cost is the binding constraint]

DO NOT USE: [Model name(s)]
REASON:     [Overkill / wrong context size / latency mismatch / etc.]
```

---

## Step 5 — Estimate cost

For each candidate model, estimate per-run cost:

```
Model: [name]
Avg input tokens:  [estimate based on skill's context needs]
Avg output tokens: [estimate based on skill's output length]
Price per run:     $[in + out cost]
Est. time/run:     [seconds — rough estimate based on model speed tier]
Runs/day estimate: [if known from skill context]
Monthly cost est.: $[price/run × runs/day × 30]
```

Token estimation guide:
- 1 page of text ≈ 500 tokens
- 1 code file (100 lines) ≈ 700 tokens
- SKILL.md file ≈ 600–1500 tokens depending on length
- Typical agent tool call overhead ≈ 200–400 tokens/call

---

## Step 6 — Output the Model Selection block

Produce a ready-to-paste section for the skill's SKILL.md:

```markdown
## Model Selection

**Recommended:** [Model name] ([Provider])
**Complexity tier:** [S0–S4] — [tier label]
**Rationale:** [1–2 sentences on why this model fits]

**Fallback chain:**
1. [Fallback 1] — [one-line reason]
2. [Fallback 2] — [one-line reason]

**Cost estimate (per run):**
- Input: ~[N] tokens | Output: ~[N] tokens
- [Primary model]: ~$[X] per run
- [Fallback 1]: ~$[X] per run

**Do not use:** [Model(s)] — [reason]

**Validation tests:** See [llm-selector test output file, if saved]
```

Paste this section directly into the SKILL.md before deploying the skill.

---

## Step 7 — Save results (optional)

If the skill is being evaluated for a real deployment, save results to:
```
[skill-folder]/llm-eval/
  recommendation.md   ← the full Step 4–5 output
  tests.md            ← the Step 3 test suite
  results.md          ← actual test outcomes (fill in after running)
```

---

## Key rules / constraints

- **Never default to Sonnet.** Sonnet is the right choice for S2–S3 work. For S0–S1, it is
  waste. For S4, it may be insufficient. Always justify the tier.
- **Cost estimate is required.** A recommendation without cost numbers is incomplete.
- **Fallback chain is required.** Every deployment must have at least one fallback.
- **Validation tests must be runnable.** Do not write abstract criteria — write concrete
  inputs with concrete pass criteria.
- **Provider diversity matters.** If the primary model is Anthropic/Bedrock, consider an
  OpenAI or open-weights fallback for resilience.
- **Self-hosted is a valid choice.** Qwen, DeepSeek, and Llama running on Ollama or
  a dedicated instance can be near-zero marginal cost for high-volume S0–S2 tasks.
- **Re-evaluate at scale.** A model that costs $0.01/run at 10 runs/day costs $90/month
  at 300 runs/day. Flag volume breakpoints in the cost estimate.

---

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Sonnet on everything | Bills 5–10× higher than needed | Run llm-selector before deploying any agent |
| No fallback defined | Agent fails completely when primary provider is down | Always define fallback chain in SKILL.md |
| Wrong context estimate | Model truncates input silently | Check skill's actual input size; Haiku/Nova have shorter effective windows in practice |
| Ignoring latency | Batch-ok task using fast real-time model (overpaying) | Classify latency sensitivity in Step 1 |
| Ignoring accuracy stakes | Cheap model on high-stakes output | Tier S3–S4 work always validates with a strong model first |
| Cost estimate in isolation | Cheapest model chosen but inference time 3× longer | Time has cost too — factor developer wait time and user experience |

## Handoffs

- **→ gstack** if task needs model routing rather than one-time selection
- **→ operator** after model is selected to route the pending task
- **→ notify** if no available model meets the cost/quality requirements

## Lambda / Step Functions candidates

| Function | Step | Stateless? | Lambda? |
|---|---|---|---|
| `classify_skill` | Step 1 — extract output type, context size, reasoning depth, accuracy stakes, latency, tool use from SKILL.md | yes | ✅ |
| `assign_complexity_tier` | Step 1 — map profile to S0–S4 tier | yes | ✅ |
| `select_candidate_models` | Step 2 — return ranked candidate list for the tier from model catalog | yes | ✅ |
| `generate_validation_tests` | Step 3 — produce 3–5 test prompts with pass criteria for the skill's workload | yes | ✅ |
| `produce_recommendation` | Step 4 — output PRIMARY + fallback chain + DO NOT USE list | yes | ✅ |
| `estimate_cost` | Step 5 — compute per-run cost for each candidate model | yes | ✅ |
| `emit_model_selection_block` | Step 6 — format ready-to-paste `## Model Selection` section | yes | ✅ |
| `save_eval_results` | Step 7 — write recommendation.md + tests.md to skill folder | yes | ✅ |

All steps are deterministic lookups, structured reasoning over fixed input, or text formatting — Lambda-compatible. The full evaluation pipeline (Steps 1–7) can run as a single Lambda invocation or as a Step Functions sequence if human validation of test results is required between steps.

## Input / Output spec

**Input:**
| Field | Type | Required | Notes |
|---|---|---|---|
| `skill_md_path` | string | yes | Absolute path to the SKILL.md file to evaluate |
| `skill_md_content` | string | no | Raw SKILL.md text (alternative to path — use when calling from another agent) |
| `volume_estimate` | int | no | Expected runs per day; used for monthly cost projection in Step 5 |
| `save_results` | bool | no | If true, write eval output to `[skill-folder]/llm-eval/`; default false |

**Output:**
```json
{
  "status": "ok | error",
  "complexity_tier": "S0 | S1 | S2 | S3 | S4",
  "tier_label": "Nano | Micro | Standard | Advanced | Expert",
  "recommendation": {
    "primary": "claude-sonnet-4-6",
    "primary_reason": "S2 task: multi-step reasoning, code generation, 4K output",
    "provider": "Anthropic",
    "fallbacks": [
      { "model": "gpt-4o", "reason": "Comparable S2 capability, lower cost at volume" },
      { "model": "qwen2.5-coder:7b", "reason": "Self-hosted, near-zero cost for code tasks" }
    ],
    "do_not_use": ["claude-opus-4-6"],
    "do_not_use_reason": "Overkill for S2; 5× cost increase without quality gain"
  },
  "cost_estimate": {
    "primary_model": "claude-sonnet-4-6",
    "avg_input_tokens": 1200,
    "avg_output_tokens": 800,
    "price_per_run_usd": 0.016,
    "monthly_cost_usd_at_10_runs_per_day": 4.80
  },
  "model_selection_block_md": "## Model Selection\n\n**Recommended:** ...",
  "validation_tests": [
    { "type": "happy_path", "input": "...", "expected_shape": "...", "pass_criterion": "..." }
  ]
}

## Permissions

<!-- v2-backfill 2026-05-31: auto-inferred — verify before ready/ promotion -->

| Type | Pattern | Why |
|---|---|---|
| Bash | `python *` | Default — refine to actual commands |

---

## Data collection (art-train)

```python
import sys; sys.path.insert(0, r"<workspace>/...")
from art_train_collector import log_pair, update_outcome

event_id = log_pair("llm-selector/select", task_description, model_selected, model="phi4-mini")

# If no retry was needed:
update_outcome("llm-selector/select", event_id, "ok")

# If the selection was wrong and required escalation/retry:
update_outcome("llm-selector/select", event_id, "wrong")
```

**Training target:** Feeds `task-router-local` — teaches the router which model is right for each task pattern.
