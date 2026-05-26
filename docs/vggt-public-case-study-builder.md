# VGGT Public Case Study Builder

Status: v0.7 minimal implementation.

Round 141 adds a local builder that converts the VGGT dogfooding material into a
public case study draft. The draft is sanitized, conservative, and review-only.
It is not a publication and does not claim experiment success.

## Inputs

- VGGT research knowledge pack.
- Evidence summary.
- Failure taxonomy.
- Advisor brief.
- Next actions.
- Privacy and compliance policy documents.

## Outputs

- `case_study_draft.md`
- `redaction_report.md`
- `claim_safety_report.md`

## Required Sections

- problem background
- why TuringResearch was useful
- route changes
- evidence management
- failures and blockers
- advisor pack
- what remains human work
- what not to claim

## Redaction And Claim Guard

The builder removes or marks:

- private local paths
- raw data references
- model file references
- advisor private feedback
- unsupported experiment claims
- non-public artifacts

The claim guard blocks:

- SparseConv3D success claims without evidence
- experiment success claims without evidence ledger support
- planned routes written as observed or executed

## Safety Boundary

- No publishing.
- No marketing overclaim.
- No experiment execution.
- No SparseConv3D success claim.
- No private path leak.
- No default networking.
- Human review remains required.

## VGGT Fixture

The committed fixture is written to:

- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/redaction_report.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`

The fixture is public-demo draft material. It does not include raw data, model
files, private paths, advisor private feedback, or non-public artifacts.
