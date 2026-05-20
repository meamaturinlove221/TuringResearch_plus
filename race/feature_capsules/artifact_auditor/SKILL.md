---
name: tulingresearch-artifact-auditor
description: Use when planning or implementing the local artifact auditor capsule.
---

# TulingResearch Plus Skill: artifact_auditor

## Role

Maintain the read-only local artifact auditor capsule for VGGT Sprint 1.

## When to use

Use when a task touches artifact bundle manifests, checksums, sidecars, missing
files, or board inventory used by later evidence and advisor outputs.

## Inputs

- User-supplied local bundle path.
- Committed fake fixtures.
- Existing scan summaries.
- Evidence Ledger status model.

## Outputs

- `ArtifactAuditReport`
- Bundle manifest
- Missing item list
- Board inventory summary

## Required files

- `race/feature_capsules/artifact_auditor/FEATURE.md`
- `race/feature_capsules/artifact_auditor/contract.yaml`
- `race/feature_capsules/artifact_auditor/sop.mmd`
- `race/feature_capsules/artifact_auditor/test_plan.md`

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/vault_schema.yaml`

## Related lanes

- `lanes/14_v0.2_sprint_1.md`
- `lanes/16_vggt_feature_capsules.md`

## Required tests

- Zip validity.
- sha256 checksum.
- Missing `.npz`.
- No-write regression.

## Rules / constraints

- Do not run VGGT.
- Do not write into linked VGGT directories.
- Do not commit private artifacts.
- Do not implement Future Sync Adapters in Sprint 1.

## Done criteria

- Audit report is deterministic.
- Missing artifacts are explicit.
- Evidence Ledger can reference audit outputs.

