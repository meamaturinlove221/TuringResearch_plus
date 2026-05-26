---
name: turingresearch-pod-workflow-pack
description: Use when designing or implementing structured pod workflow packages for TuringResearch Plus.
---

# TuringResearch Plus Skill: turingresearch-pod-workflow-pack

## Role

Design structured pod workflow packages and output return policies.

## When to use

Use for v0.3 Sprint 1 pod workflow design, output package validation, and
Run Ingestor integration planning.

## Inputs

- `docs/pod-workflow-design.md`
- `docs/structured-output-return-policy.md`
- `contracts/pod_workflow.yaml`

## Outputs

- Pod workflow specs
- Structured output return checks
- Review-only proposed updates

## Rules / constraints

- Do not execute remote pods.
- Do not control Modal or RunPod.
- Do not accept report-only outputs as promotion-ready.
- Do not auto-apply evidence updates.

## Done criteria

- Pod output package is auditable.
- Missing artifacts are visible.
- Run Ingestor can consume returned summaries.
