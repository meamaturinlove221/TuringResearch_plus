---
name: turingresearch-cache-and-ledger
description: Use when changing shared cache, failure ledger, BudgetGate, or StateLedger foundations.
---

# TuringResearch Plus Skill: turingresearch-cache-and-ledger

## Role

Protect deterministic cache keys, cache metadata, failure retries, budget gates, and state ledger append behavior.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-cache-and-ledger` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research/cache/`
- `src/turing_research_plus/budget/`
- `src/turing_research_plus/ledger/`

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

- `workflow`: artifact audit
- `when_to_use`: audit artifacts, evidence references, ledgers, manifests,
  export bundles, or privacy-sensitive file readiness.
- `inputs`: artifact paths, manifests, evidence ledger entries, privacy policy,
  expected hashes, and export criteria.
- `outputs`: artifact audit report, missing evidence notes, privacy findings,
  release blockers, and proposed remediation.
- `safety`: do not include raw data, secrets, private local paths, restricted
  model files, or fake observed results.
- `non-goals`: no deletion of user files, no automatic upload, no evidence
  fabrication, no private-data export.
- `handoff`: record included/excluded files, blockers, warnings, and required
  human review.
- `tests`: artifact audit, privacy scanner, export quality, and regression gate
  tests.
- `related_docs`: `docs/artifact-auditor.md`,
  `docs/privacy-data-policy-layer.md`, `docs/export-quality-gate.md`.
