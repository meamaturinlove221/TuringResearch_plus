# TuringResearch Plus Feature Capsule: failure_taxonomy_engine

## Problem

Sprint 1 reports use several failure-like labels: hard-blocked,
not-enough-evidence, visual not-ready, missing input, fallback-only, and
requires-human-review. Sprint 2 needs a shared taxonomy so failures can drive
next actions instead of becoming loose notes.

## VGGT motivating example

V260 is hard-blocked, V999 is not final achievement, visual evidence is missing,
and SparseConv3D success remains not-enough-evidence. These are different
failure classes with different next actions.

## User story

As a TuringResearch Plus maintainer, I need consistent failure attribution so
advisor packs, route reports, and evidence ledgers can agree on why a route is
not ready.

## Inputs

- Evidence Ledger status records.
- Hard Gate validation reports.
- Experiment Route DSL reports.
- Artifact and Visual Evidence audit reports.
- Advisor Pack not-ready claims.

## Outputs

- `FailureAttributionReport`
- canonical failure labels
- severity mapping
- next-action recommendations
- Markdown failure summary

## Data model

- `FailureTaxonomy`
- `FailureCategory`
- `FailureInstance`
- `FailureAttributionReport`
- `FailureNextAction`

## Proposed commands / tools

- command: `turing failure analyze`
- tool: `experiment.failure_analyze`
- output: `FailureAttributionReport`

This is a capsule-local proposal and is not a frozen public MCP API until a
contracts-first round updates root contracts and `docs/mcp-tools.md`.

## Related contracts

- `contracts/failure_taxonomy.yaml`
- `contracts/hard_gates.yaml`
- `contracts/vggt_evidence.yaml`
- `contracts/advisor_pack.yaml`

## Related skills

- `turingresearch-fusion-stress-test`
- `turingresearch-master-orchestrator`
- `turingresearch-cache-and-ledger`

## Required tests

- Known failure labels normalize to canonical categories.
- Severity mapping is deterministic.
- Failure reports preserve blockers and next actions.
- Fast-return, fallback-only, report-only, visual-not-ready, and
  missing-evidence failures remain distinguishable.
- JSON and Markdown serialization are stable.

## Risks

- Taxonomy becomes subjective.
- Severity labels drift across modules.
- Next actions over-prescribe work that lacks evidence.

## Done criteria

- Failure labels are canonical and deterministic.
- Route DSL and Advisor Pack can consume failure reports.
- Missing evidence and hard blockers remain distinct.

## Release target

v0.2.0 Sprint 2.

## Upstream learning note

`docs/upstream-learning-report.md` is missing in the current checkout. This
capsule adopts only the documented internal Sprint 1 pattern: explicit failure
classes over vague readiness language.

## Relation to Sprint 1 modules

- Normalizes Evidence Ledger statuses.
- Consumes Hard Gate outputs.
- Improves Advisor Pack failure analysis.
- Keeps Visual Evidence missing items distinct from experiment failures.
