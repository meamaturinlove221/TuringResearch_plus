# VGGT Public Case Study Builder Skill

Status: planning skill draft.

Use this skill for public-safe VGGT case study planning. It does not run VGGT
or claim unsupported SparseConv3D success.

## Inputs

- VGGT research knowledge pack
- dogfooding replay
- route DSL
- advisor pack
- paper assembly gate
- privacy scan report

## Outputs

- VGGTCaseStudyOutline
- VGGTCaseStudyEvidenceMap
- VGGTCaseStudySafetyReport

## Safety Rules

- Do not read private VGGT paths.
- Do not run VGGT or Modal experiments.
- Do not claim SparseConv3D success without evidence.
- Do not mark planned routes as observed.

## Related Contracts

- vggt_public_case_study.yaml
- vggt_evidence.yaml
- paper_writing_scaffold.yaml
