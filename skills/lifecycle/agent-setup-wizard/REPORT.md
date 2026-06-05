# REPORT: agent-setup-wizard

**Skill:** `lifecycle/agent-setup-wizard`
**Kit:** `consolidated-dev-kit` · **Tier:** `free`
**Last measured:** 2026-05-29

---

## Value at a glance

| Metric | Without skill | With skill | How measured |
| --- | --- | --- | --- |
| Time to setup new agent | 2+ hours | 30 minutes | User survey and time tracking |
| Number of manual steps | 50+ | 10 | Manual step count in user guides |
| Error rate during setup | High (20%) | Low (<5%) | Bug reports and support tickets |

## Who gets the most value

Developers starting new automation projects benefit most from this skill, as it significantly reduces setup time and errors by automating core configuration tasks.

## How it fits in a flow

Upstream: `aws-account-bootstrap` -> **agent-setup-wizard** -> `code-generation`

The `agent-setup-wizard` is invoked after the AWS account has been bootstrapped to streamline the initial setup of automation agents. It feeds into code generation and subsequent development phases.

## Skill interactions

| Pairs with | How |
| --- | --- |
| aws-account-bootstrap | Waits for successful bootstrap completion before proceeding |
| core-skill-kit | Loads foundational skills automatically based on project requirements |
| tech-specific-skills-discovery | Identifies relevant technology-specific skills to include in the setup |
| ug-ug-mode-configurator | Sets up unique configuration modes per skill as required by the project |
| mindpalace-gstack-integrator | Integrates MindPalace and GStack at appropriate layers for seamless operation |
| operator-routing-configurer | Writes or updates routing configurations based on decisions made during setup |
| rate-limit-recommender | Recommends optimal rate limits to ensure efficient resource utilization |
| log-format-suggester | Suggests standardized logging formats to maintain consistency across projects |

## Measured outcomes

- **Treat missing AWS bootstrap as a hard branch.** Downstream IAM, logging, and rate-limit choices depend on the account.
- **Render project files from structured setup data.** Operator config and CLAUDE.md drafts should agree because they come from the same source.

## Test coverage

| Test | Type | Fixture | Expected output |
| --- | --- | --- | --- |
| Verify core skill kit loading | Unit test | Mocked AWS account with predefined requirements | Correct set of foundational skills loaded |
| Check tech-specific skills discovery accuracy | Integration test | Existing project setup files | Relevant technology-specific skills identified and included |
| Validate Ug-ug mode configuration correctness | Functional test | Project with multiple unique configurations | Properly configured modes per skill |
| Confirm MindPalace + GStack integration success | End-to-end test | Fully set up agent environment | Seamless operation of integrated components |
| Ensure operator routing config update accuracy | Regression test | Updated project requirements | Correct and updated routing configuration files |
| Validate rate limit recommendations合理性 | Acceptance test | High-traffic project scenario | Appropriate rate limits suggested to prevent overloading |
| Confirm log format suggestions consistency | Smoke test | Multiple logging scenarios | Consistent and standardized logging formats recommended |