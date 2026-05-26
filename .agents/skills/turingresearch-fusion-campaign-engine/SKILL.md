---
name: turingresearch-fusion-campaign-engine
description: Use when maintaining Campaign -> Strategy -> Tactic -> SOP runtime behavior.
---

# TuringResearch Plus Skill: turingresearch-fusion-campaign-engine

## Role

Maintain deterministic campaign runtime, quality gates, checkpoint hooks, artifacts, and budget checks.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-campaign-engine` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/campaign/`
- `src/turing_research_plus/subtask/`

## Related contracts

- `contracts/fusion_workflows.yaml`
- `contracts/artifact_schema.yaml`

## Related lanes

- `lanes/06_workflow_orchestration.md`

## Required tests

- `tests/unit/test_campaign_runner.py`
- `tests/unit/test_campaign_registry.py`
- `tests/unit/test_subtask_models.py`

## Rules / constraints

- Project display name is TuringResearch Plus.
- Core package is `turing_research` and Plus package is `turing_research_plus`.
- MCP server name is `turingresearch-plus`.
- Skill names must use the `turingresearch-` prefix.
- Keep work inside `TuringResearch/TuringResearch_plus`.
- Do not require real network access, external API keys, or live service calls in tests.
- Preserve EvidenceRef, ResearchArtifact, BudgetGate, and StateLedger boundaries when relevant.
- Use service protocols or adapters for external APIs.
- Update the owner lane and `lanes/00_master_ledger.md` after meaningful changes.

## Done criteria

- Implementation status: `locked`.
- Release requirement: `workflow-required`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TuringResearch Plus naming.

## Round 240 SOP Parity

- `workflow`: campaign catalog
- `when_to_use`: route research workflow intent to a campaign, skill, and
  precondition checklist without executing an agent runtime.
- `inputs`: task description, campaign catalog, preconditions, recommended
  skills, and safety notes.
- `outputs`: recommended campaign, recommended skill, expected outputs, tests,
  and human-review boundary.
- `safety`: campaign routing is advisory only; it must not call an LLM, start
  MCP, access the network, or execute skills.
- `non-goals`: no autonomous strategy runtime, no remote execution, no
  conversion of plans into observed evidence.
- `handoff`: cite campaign id, selected skill, missing preconditions, and docs
  to review before implementation.
- `tests`: campaign catalog model/router tests and skill SOP parity tests.
- `related_docs`: `docs/turingresearch-campaign-catalog.md`,
  `docs/campaign-routing-table.md`, `contracts/campaign_catalog.yaml`.
