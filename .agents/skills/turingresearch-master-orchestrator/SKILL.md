---
name: turingresearch-master-orchestrator
description: Use when coordinating TuringResearch Plus lane work across contracts, models, tests, and ledgers.
---

# TuringResearch Plus Skill: turingresearch-master-orchestrator

## Role

Coordinate single-window TuringResearch Plus work across lanes and ensure every round updates contracts, tests, docs, and ledgers.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-master-orchestrator` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `lanes/`
- `contracts/`
- `docs/`

## Related contracts

- `contracts/core_tools.yaml`
- `contracts/fusion_workflows.yaml`
- `contracts/race_features.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/00_master_ledger.md`

## Required tests

- `tests/contract/test_release_gate_contract.py`
- `tests/contract/test_skills_integrity.py`

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

- `workflow`: master orchestrator
- `when_to_use`: coordinate multi-file rounds, gates, reports, contracts, tests,
  and ledgers when no narrower skill fully owns the request.
- `inputs`: user round request, relevant docs, contracts, tests, lanes, and
  current git/worktree state.
- `outputs`: scoped file updates, focused validation results, lane entry,
  master ledger entry, and final round summary.
- `safety`: do not run live network calls unless the round explicitly allows
  upstream scanning; do not read private VGGT paths unless explicitly allowed;
  do not convert planned work into observed results.
- `non-goals`: no hidden release, tag, child repo creation, remote execution, or
  undocumented feature expansion.
- `handoff`: record changed files, tests, blockers, push status, and next
  commit message.
- `tests`: name integrity, relevant focused unit/contract/workflow tests, and
  targeted pre-push checks.
- `related_docs`: `docs/skill-sop-parity.md`,
  `docs/turingresearch-campaign-catalog.md`, `lanes/00_master_ledger.md`.
