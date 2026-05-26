---
name: tulingresearch-cache-and-ledger
description: Use when changing shared cache, failure ledger, BudgetGate, or StateLedger foundations.
---

# TulingResearch Plus Skill: tulingresearch-cache-and-ledger

## Role

Protect deterministic cache keys, cache metadata, failure retries, budget gates, and state ledger append behavior.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `tulingresearch-cache-and-ledger` or the matching TulingResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TulingResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/tuling_research/cache/`
- `src/tuling_research_plus/budget/`
- `src/tuling_research_plus/ledger/`

## Related contracts

- `contracts/core_tools.yaml`
- `contracts/error_schema.yaml`
- `contracts/artifact_schema.yaml`

## Related lanes

- `lanes/06_workflow_orchestration.md`

## Required tests

- `tests/unit/test_cache_keys.py`
- `tests/unit/test_cache_manager.py`
- `tests/unit/test_failure_ledger.py`
- `tests/unit/test_budget_models.py`
- `tests/unit/test_state_ledger.py`

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
- Release requirement: `release-critical`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TulingResearch Plus naming.
