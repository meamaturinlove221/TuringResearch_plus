---
name: turingresearch-fusion-north-star
description: Use when converting vague research intent into North Star research briefs and direction candidates.
---

# TuringResearch Plus Skill: turingresearch-fusion-north-star

## Role

Maintain cold-start, warm-start, and hot-start North Star workflows with fake services.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-north-star` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/north_star/`

## Related contracts

- `contracts/fusion_workflows.yaml`

## Related lanes

- `lanes/04_yogsoth_fusion.md`

## Required tests

- `tests/unit/test_north_star_models.py`
- `tests/unit/test_north_star_service.py`
- `tests/workflow/test_north_star_dry_run.py`

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
