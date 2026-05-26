---
name: turingresearch-visual-evidence-auditor
description: Use when planning or implementing the visual evidence auditor capsule.
---

# TuringResearch Plus Skill: visual_evidence_auditor

## Role

Maintain the visual evidence classification and advisor-readiness gate capsule.

## When to use

Use when a task touches visual evidence levels, region labels, V121 readiness,
or advisor pack visual summaries.

## Inputs

- `ArtifactAuditReport`
- Visual sidecars
- Optional local visual inventory
- Evidence Ledger rows

## Outputs

- `VisualEvidenceAuditReport`
- Classification table
- Missing visual evidence report

## Required files

- `race/feature_capsules/visual_evidence_auditor/FEATURE.md`
- `race/feature_capsules/visual_evidence_auditor/contract.yaml`
- `race/feature_capsules/visual_evidence_auditor/sop.mmd`
- `race/feature_capsules/visual_evidence_auditor/test_plan.md`

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/14_v0.2_sprint_1.md`
- `lanes/16_vggt_feature_capsules.md`

## Required tests

- Visual classification fixtures.
- Unknown visual artifact gate.
- Advisor readiness summary gate.

## Rules / constraints

- Do not fabricate image evidence.
- Do not claim V121 without local visual inventory.
- Do not package private images into docs.
- Do not implement Future Sync Adapters in Sprint 1.

## Done criteria

- Visual evidence levels are deterministic.
- Source artifact provenance is required.
- Advisor readiness is blocked when evidence is missing.
