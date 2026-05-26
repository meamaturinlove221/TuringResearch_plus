---
name: turingresearch-experiment-route-dsl
description: Use when planning or implementing the Sprint 2 Experiment Route DSL capsule.
---

# TuringResearch Plus Skill: experiment_route_dsl

## Role

Maintain the Experiment Route DSL capsule for structured VGGT route planning.

## When to use

Use when a task touches route specs, route gate bindings, controller prompt
drafts, stop conditions, or VGGT route dry-runs.

## Inputs

- Route intent.
- Evidence Ledger entries.
- Artifact and visual audit reports.
- Hard Gate Library outputs.

## Outputs

- `ExperimentRouteSpec`
- `ControllerPromptDraft`
- route Markdown summary

## Required files

- `race/feature_capsules/experiment_route_dsl/FEATURE.md`
- `race/feature_capsules/experiment_route_dsl/contract.yaml`
- `race/feature_capsules/experiment_route_dsl/sop.mmd`
- `race/feature_capsules/experiment_route_dsl/test_plan.md`

## Related contracts

- `contracts/experiment_routes.yaml`
- `contracts/hard_gates.yaml`
- `contracts/failure_taxonomy.yaml`

## Related lanes

- `lanes/25_v0.2_sprint_2_scope.md`
- `lanes/26_v0.2_sprint_2_feature_capsules.md`

## Required tests

- route schema validation
- route compile dry-run
- route markdown export
- no planned-to-observed promotion

## Rules / constraints

- Do not run VGGT.
- Do not read private VGGT paths by default.
- Do not implement Modal live execution.
- Do not claim route success without evidence.

## Done criteria

- Route plans serialize to JSON and Markdown.
- Gates and failure labels are explicit.
- Advisor pack can consume route summaries.
