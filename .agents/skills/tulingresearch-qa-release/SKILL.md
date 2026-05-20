---
name: tulingresearch-qa-release
description: Use when validating TulingResearch Plus tests, linting, typing, packaging, or release readiness.
---

# TulingResearch Plus Skill: tulingresearch-qa-release

## Role

Run release gates and keep public release documentation, examples, contract tests, and workflow tests aligned.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `tulingresearch-qa-release` or the matching TulingResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TulingResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `docs/public-release-checklist.md`
- `docs/public-readme-draft.md`
- `docs/release-plan.md`
- `examples/`
- `tests/contract/`
- `tests/workflow/`

## Related contracts

- `contracts/core_tools.yaml`
- `contracts/fusion_workflows.yaml`
- `contracts/race_features.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/09_qa_release.md`

## Required tests

- `tests/contract/test_release_gate_contract.py`
- `tests/workflow/test_release_examples_fake_mode.py`

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
