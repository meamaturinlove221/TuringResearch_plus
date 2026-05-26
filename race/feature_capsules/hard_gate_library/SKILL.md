---
name: turingresearch-hard-gate-library
description: Use when planning or implementing reusable Sprint 2 hard gates.
---

# TuringResearch Plus Skill: hard_gate_library

## Role

Maintain reusable hard gate definitions and validation reports.

## When to use

Use when a task touches gate specs, promotion rules, blocked route semantics, or
requires-human-review outputs.

## Inputs

- Evidence Ledger entries.
- Audit reports.
- Route specs.
- Advisor claims.

## Outputs

- `GateSpec`
- `GateResult`
- `HardGateValidationReport`

## Required files

- `race/feature_capsules/hard_gate_library/FEATURE.md`
- `race/feature_capsules/hard_gate_library/contract.yaml`
- `race/feature_capsules/hard_gate_library/sop.mmd`
- `race/feature_capsules/hard_gate_library/test_plan.md`

## Related contracts

- `contracts/hard_gates.yaml`
- `contracts/vggt_evidence.yaml`
- `contracts/advisor_pack.yaml`

## Related lanes

- `lanes/25_v0.2_sprint_2_scope.md`
- `lanes/26_v0.2_sprint_2_feature_capsules.md`

## Required tests

- pass/block/requires-human-review validation
- missing evidence handling
- JSON and Markdown serialization

## Rules / constraints

- Do not treat missing evidence as pass.
- Do not encode live execution assumptions.
- Keep status labels aligned with Sprint 1.

## Done criteria

- Shared gates can be reused by Route DSL, Advisor Pack, and Paper workflows.
