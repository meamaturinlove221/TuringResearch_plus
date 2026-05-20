---
name: tulingresearch-fusion-subtask-runtime
description: Use when maintaining TaskProfile, prompt rendering, dry-run SubtaskRunner, or subtask quality gates.
---

# TulingResearch Plus Skill: tulingresearch-fusion-subtask-runtime

## Role

Maintain single-window role simulation, deterministic dry-run output, prompts, and quality checks.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `tulingresearch-fusion-subtask-runtime` or the matching TulingResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TulingResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/tuling_research_plus/subtask/`
- `docs/codex-multi-agent.md`

## Related contracts

- `contracts/fusion_workflows.yaml`

## Related lanes

- `lanes/06_workflow_orchestration.md`

## Required tests

- `tests/unit/test_subtask_runner.py`
- `tests/unit/test_subtask_quality.py`
- `tests/unit/test_subtask_models.py`

## Rules / constraints

- Project display name is TulingResearch Plus.
- Core package is `tuling_research` and Plus package is `tuling_research_plus`.
- MCP server name is `tulingresearch-plus`.
- Skill names must use the `tulingresearch-` prefix.
- Keep work inside `TulingResearch/TulingResearch_plus`.
- Do not require real network access, external API keys, or live service calls in tests.
- Preserve EvidenceRef, ResearchArtifact, BudgetGate, and StateLedger boundaries when relevant.
- Use service protocols or adapters for external APIs.
- Update the owner lane and `lanes/00_master_ledger.md` after meaningful changes.

## Done criteria

- Implementation status: `locked`.
- Release requirement: `workflow-required`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TulingResearch Plus naming.
