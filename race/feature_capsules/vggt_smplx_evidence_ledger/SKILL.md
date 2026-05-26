---
name: turingresearch-vggt-smplx-evidence-ledger
description: Use when planning or implementing the VGGT/SMPL-X evidence ledger capsule.
---

# TuringResearch Plus Skill: vggt_smplx_evidence_ledger

## Role

Maintain the status-safe VGGT/SMPL-X evidence ledger capsule for Sprint 1.

## When to use

Use when a task touches V770/V129/V260/V900/V930/V999/V120/V121 status,
EvidenceRef preservation, or review-ready wording.

## Inputs

- Round 36 final scope and implementation order.
- VGGT dogfooding docs.
- Committed local scan summaries.
- Optional user-supplied local evidence ledger.

## Outputs

- `VGGTEvidenceLedger`
- Markdown/JSON summaries
- Missing evidence report

## Required files

- `race/feature_capsules/vggt_smplx_evidence_ledger/FEATURE.md`
- `race/feature_capsules/vggt_smplx_evidence_ledger/contract.yaml`
- `race/feature_capsules/vggt_smplx_evidence_ledger/sop.mmd`
- `race/feature_capsules/vggt_smplx_evidence_ledger/test_plan.md`

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/vault_schema.yaml`
- `contracts/race_features.yaml`

## Related lanes

- `lanes/14_v0.2_sprint_1.md`
- `lanes/16_vggt_feature_capsules.md`

## Required tests

- Status enum validation.
- Missing evidence blocks local-observed claims.
- Markdown and JSON serialization.

## Rules / constraints

- Do not run VGGT.
- Do not read private VGGT paths by default.
- Do not fabricate experiment results.
- Do not implement Future Sync Adapters in Sprint 1.

## Done criteria

- Contract draft approved.
- Tests cover status boundaries.
- Ledger output preserves evidence refs and review boundaries.
