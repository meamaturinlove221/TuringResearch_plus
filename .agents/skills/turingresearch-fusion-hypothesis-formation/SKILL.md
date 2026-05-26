---
name: turingresearch-fusion-hypothesis-formation
description: Use when maintaining hypothesis generation, falsifiability, FINER checks, or hypothesis portfolios.
---

# TuringResearch Plus Skill: turingresearch-fusion-hypothesis-formation

## Role

Maintain falsifiable hypotheses, operationalization, research questions, and evidence-backed portfolios.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-hypothesis-formation` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/hypothesis/`

## Related contracts

- `contracts/fusion_workflows.yaml`

## Related lanes

- `lanes/04_yogsoth_fusion.md`

## Required tests

- `tests/unit/test_hypothesis_models.py`
- `tests/unit/test_gap_prioritization.py`
- `tests/unit/test_falsifiability.py`
- `tests/unit/test_finer.py`
- `tests/unit/test_hypothesis_portfolio.py`

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
