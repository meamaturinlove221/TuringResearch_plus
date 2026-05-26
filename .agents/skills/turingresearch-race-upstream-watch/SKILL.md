---
name: turingresearch-race-upstream-watch
description: Use when tracking public upstream changes relevant to TuringResearch Plus Race Mode.
---

# TuringResearch Plus Skill: turingresearch-race-upstream-watch

## Role

Maintain public-only upstream snapshot diffing, watch reports, version anomaly detection, and optional IdeaCards.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-race-upstream-watch` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/race/upstream_watch.py`
- `race/upstream_reports/`

## Related contracts

- `contracts/race_features.yaml`

## Related lanes

- `lanes/07_race_mode.md`

## Required tests

- `tests/unit/test_upstream_watch.py`

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

## Round 240 SOP Parity

- `workflow`: upstream watch
- `when_to_use`: scan, baseline, classify, or diff public upstream references
  when the round explicitly permits upstream scanning.
- `inputs`: watch targets, existing baselines, upstream reports, parity matrix,
  and operator-provided scan constraints.
- `outputs`: honest baseline/diff report, changed module summary, parity action
  notes, and lane/ledger updates.
- `safety`: do not claim added/modified/deleted without a prior baseline; do not
  treat unresolved targets as deleted; do not copy upstream code.
- `non-goals`: no feature implementation, no default networking outside an
  upstream scan round, no private source ingestion.
- `handoff`: record whether scan was live, skipped, unresolved, or
  baseline-created.
- `tests`: upstream watch/baseline/diff tests and name integrity.
- `related_docs`: `docs/upstream-strict-diff-v1.2.md`,
  `docs/original-reference-parity-matrix.md`, `upstream_watch/targets.yaml`.
