# TuringResearch Plus Feature Capsule: hard_gate_library

## Problem

Sprint 1 repeated similar gates across evidence, artifact, visual, advisor, PDF,
and paper workflows. Without a shared gate library, routes can drift into
fast-return, report-only, or fallback-only states that look ready when they are
not.

## VGGT motivating example

V260 must remain hard-blocked. V999 long-run status cannot equal final target
achievement. SparseConv3D success cannot be claimed without real evidence. These
rules should live in reusable gates rather than scattered prose.

## User story

As a TuringResearch Plus maintainer, I need a shared gate library that validates
whether evidence is sufficient to promote a claim, route, method card, or
advisor note.

## Inputs

- Evidence Ledger entries.
- Artifact Audit reports.
- Visual Evidence reports.
- Advisor Pack claims.
- Route DSL gate bindings.
- Paper and PDF asset provenance.

## Outputs

- `HardGateValidationReport`
- `GateSpec`
- `GateResult`
- Markdown gate summary
- blocked / requires-human-review reasons

## Data model

- `GateSpec`
- `GateCondition`
- `GateInputRef`
- `GateResult`
- `HardGateValidationReport`

## Proposed commands / tools

- command: `turing gates validate`
- tool: `experiment.hard_gate_validate`
- output: `HardGateValidationReport`

This is a capsule-local proposal and is not a frozen public MCP API until a
contracts-first round updates root contracts and `docs/mcp-tools.md`.

## Related contracts

- `contracts/hard_gates.yaml`
- `contracts/vggt_evidence.yaml`
- `contracts/artifact_audit.yaml`
- `contracts/visual_evidence.yaml`
- `contracts/advisor_pack.yaml`

## Related skills

- `turingresearch-master-orchestrator`
- `turingresearch-cache-and-ledger`
- `turingresearch-fusion-experiment-execution`

## Required tests

- Gate passes with sufficient evidence.
- Gate blocks on hard blocker.
- Gate returns `requires-human-review` for ambiguous evidence.
- Gate preserves `not-enough-evidence`.
- Gate Markdown and JSON serialization are stable.
- Gate labels match Sprint 1 status language.

## Risks

- Duplicating existing checks instead of simplifying them.
- Over-generalizing gates before Route DSL is stable.
- Allowing ambiguous claims to pass.

## Done criteria

- Gates are deterministic and local-only.
- Sprint 1 safety regressions are covered.
- Route DSL can reference gate specs.
- Advisor Pack Builder can summarize gate results.

## Release target

v0.2.0 Sprint 2.

## Upstream learning note

`docs/upstream-learning-report.md` is missing in the current checkout. This
capsule remains based on Sprint 1 evidence discipline and documented source
hygiene rules.

## Relation to Sprint 1 modules

- Extracts repeated gate patterns from Evidence Ledger, Visual Evidence Auditor,
  Advisor Pack Builder, DocFlow, and PDF Phase B.
- Keeps missing inputs visible instead of crashing or promoting claims.
