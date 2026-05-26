# TuringResearch Plus Feature Capsule: experiment_route_dsl

## Problem

VGGT long-running experiment routes are currently described in prose and
advisor notes. That makes it too easy to blur planned work, blocked routes,
fallback-only routes, and observed results.

## VGGT motivating example

The SMPL-X feature encoding pivot needs a structured way to describe routes such
as V260, V770, V999, and Modal Real SparseConv3D without running VGGT or claiming
success. The route must record expected evidence, hard gates, stop conditions,
and what remains human-review.

## User story

As a TuringResearch Plus maintainer, I need to compile a VGGT route into a
deterministic route spec and controller prompt draft so the same experiment
intent can be reviewed, gated, and audited before execution.

## Inputs

- VGGT route intent.
- Evidence Ledger entries.
- Artifact Audit reports.
- Visual Evidence reports.
- Hard Gate Library gate definitions.
- Failure Taxonomy labels.

## Outputs

- `ExperimentRouteSpec`
- `ControllerPromptDraft`
- route Markdown summary
- route gate checklist
- route stop conditions

## Data model

- `ExperimentRouteSpec`
- `ExperimentRouteStep`
- `RouteGateBinding`
- `RouteExpectedArtifact`
- `ControllerPromptDraft`

## Proposed commands / tools

- command: `turing route compile`
- tool: `experiment.route_compile`
- output: `ExperimentRouteSpec / ControllerPromptDraft`

This is a capsule-local proposal and is not a frozen public MCP API until a
contracts-first round updates root contracts and `docs/mcp-tools.md`.

## Related contracts

- `contracts/experiment_routes.yaml`
- `contracts/hard_gates.yaml`
- `contracts/failure_taxonomy.yaml`
- `contracts/vggt_evidence.yaml`

## Related skills

- `turingresearch-fusion-experiment-execution`
- `turingresearch-master-orchestrator`
- `turingresearch-cache-and-ledger`

## Required tests

- Route spec validates required fields.
- Route parser accepts a minimal VGGT fixture.
- Unknown gate labels are rejected.
- Route Markdown export includes steps, expected artifacts, gates, and stop
  conditions.
- V260 remains hard-blocked when evidence says hard-blocked.
- Modal Real SparseConv3D remains planned, not observed.

## Risks

- Route DSL becomes too broad.
- Planned routes are mistaken for observed evidence.
- Controller prompts imply execution readiness without gates passing.
- Private VGGT paths leak into route examples.

## Done criteria

- Route outputs serialize to JSON and Markdown.
- Route gates reference Hard Gate Library definitions.
- Missing evidence is explicit.
- No route compile step runs VGGT.
- No planned route is written as observed.

## Release target

v0.2.0 Sprint 2.

## Upstream learning note

`docs/upstream-learning-report.md` is missing in the current checkout. This
capsule keeps the upstream learning boundary conservative: adopt workflow and
testing patterns only, never copy incompatible code.

## Relation to Sprint 1 modules

- Uses Evidence Ledger statuses to avoid promoting missing results.
- Links route expected artifacts to Artifact Auditor outputs.
- Uses Visual Evidence Auditor readiness for visual gates.
- Feeds Advisor Pack Builder with route summaries and next actions.
