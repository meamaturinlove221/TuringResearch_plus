---
name: tulingresearch-advisor-pack-builder
description: Use when planning or implementing the VGGT advisor pack builder capsule.
---

# TulingResearch Plus Skill: advisor_pack_builder

## Role

Maintain the advisor-readable pack builder capsule for VGGT Sprint 1.

## When to use

Use when a task touches advisor pack sections, readiness wording, missing
evidence reporting, or review-ready boundaries.

## Inputs

- Evidence Ledger output
- Artifact Auditor output
- Visual Evidence Auditor output
- Dogfooding context

## Outputs

- `AdvisorPack`
- Markdown pack
- Missing evidence appendix

## Required files

- `race/feature_capsules/advisor_pack_builder/FEATURE.md`
- `race/feature_capsules/advisor_pack_builder/contract.yaml`
- `race/feature_capsules/advisor_pack_builder/sop.mmd`
- `race/feature_capsules/advisor_pack_builder/test_plan.md`

## Related contracts

- `contracts/paper_pipeline.yaml`
- `contracts/artifact_schema.yaml`

## Related lanes

- `lanes/14_v0.2_sprint_1.md`
- `lanes/16_vggt_feature_capsules.md`

## Required tests

- Required sections present.
- No promotion wording.
- Missing visual inventory blocks readiness.

## Rules / constraints

- Do not claim advisor approval.
- Do not fabricate experiment results.
- Do not bypass Evidence Ledger status.
- Do not implement Future Sync Adapters in Sprint 1.

## Done criteria

- Pack is evidence-linked.
- Missing evidence is explicit.
- Wording gates reject promotion claims.

