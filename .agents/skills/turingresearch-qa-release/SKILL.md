---
name: turingresearch-qa-release
description: Use when validating TuringResearch Plus tests, linting, typing, packaging, or release readiness.
---

# TuringResearch Plus Skill: turingresearch-qa-release

## Role

Run release gates and keep public release documentation, examples, contract tests, and workflow tests aligned.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-qa-release` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
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

- `workflow`: release gate
- `when_to_use`: run go/no-go, regression, privacy/security, docs, package,
  branch, release note, or public launch checks.
- `inputs`: target release scope, changed files, contracts, docs, test matrix,
  security/privacy policies, and known limitations.
- `outputs`: gate report, blockers, test summary, release notes, known
  limitations, and final human actions.
- `safety`: do not publish, tag, push, create child repos, or run live tests
  unless explicitly approved by the round.
- `non-goals`: no automatic PyPI release, GitHub release, default live tests,
  secret upload, or hidden release action.
- `handoff`: record decision, blockers, tests run, push status, and suggested
  commit message.
- `tests`: full pytest, mypy, name integrity, privacy/security gate, release
  contracts, and targeted pre-push checks.
- `related_docs`: `docs/v1.1.0-full-regression-report.md`,
  `docs/v1.1.0-release-notes.md`, `docs/v1.1.0-test-summary.md`.
