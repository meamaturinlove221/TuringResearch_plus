---
name: turingresearch-race-source-hygiene
description: Use when maintaining public-source, license, NDA, private, or leak gates for Race Mode.
---

# TuringResearch Plus Skill: turingresearch-race-source-hygiene

## Role

Protect Race Mode from private, leaked, NDA, proprietary, or incompatible-license implementation sources.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-race-source-hygiene` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/race/source_hygiene.py`
- `docs/race_mode.md`

## Related contracts

- `contracts/race_features.yaml`

## Related lanes

- `lanes/07_race_mode.md`

## Required tests

- `tests/unit/test_source_hygiene.py`
- `tests/contract/test_race_tools_contract.py`

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
- Release requirement: `release-critical`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TuringResearch Plus naming.
