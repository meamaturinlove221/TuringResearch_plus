---
name: turingresearch-failure-taxonomy-engine
description: Use when planning or implementing Sprint 2 failure taxonomy and attribution.
---

# TuringResearch Plus Skill: failure_taxonomy_engine

## Role

Maintain canonical failure categories, severity mapping, and next-action
language.

## When to use

Use when a task touches blockers, route failures, visual not-ready findings,
advisor failure analysis, or hard gate failures.

## Inputs

- Gate reports.
- Route reports.
- Evidence Ledger records.
- Audit reports.

## Outputs

- `FailureTaxonomy`
- `FailureAttributionReport`
- failure Markdown summary

## Required files

- `race/feature_capsules/failure_taxonomy_engine/FEATURE.md`
- `race/feature_capsules/failure_taxonomy_engine/contract.yaml`
- `race/feature_capsules/failure_taxonomy_engine/sop.mmd`
- `race/feature_capsules/failure_taxonomy_engine/test_plan.md`

## Related contracts

- `contracts/failure_taxonomy.yaml`
- `contracts/hard_gates.yaml`

## Related lanes

- `lanes/25_v0.2_sprint_2_scope.md`
- `lanes/26_v0.2_sprint_2_feature_capsules.md`

## Required tests

- canonical category normalization
- severity mapping
- next-action preservation
- JSON and Markdown serialization

## Rules / constraints

- Do not collapse distinct failure classes.
- Do not invent experiment results.
- Do not treat missing input as failed experiment.

## Done criteria

- Advisor Pack and Route DSL can share failure vocabulary.
