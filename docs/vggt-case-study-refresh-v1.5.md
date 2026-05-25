# VGGT Case Study Refresh v1.5

Round: Optional 338.5
Date: 2026-05-25
Repository: TulingResearch Plus

## Purpose

Refresh a public-safe VGGT case study and split-ready draft from the latest local scan outputs. This round creates documentation only; it does not package data, copy artifacts, run VGGT, or promote claims.

## Inputs

| Input | Status | Notes |
| --- | --- | --- |
| Local scan summary | observed | Used as the primary case-study source. |
| Local scan artifact index | observed | Used only as metadata context. |
| Local scan missing-items report | observed | Missing and unconfirmed items remain guarded. |
| Local scan evidence ledger | observed | Used to preserve `local-observed` and `requires-human-review` statuses. |
| Local scan visual inventory | observed | Used as metadata only; no visual content copied. |
| Split-ready case directory | missing | Created this round as a draft documentation package. |
| Public safety checklist doc | missing | Recorded as a blocker for public release readiness. |
| Original replication progress report | missing | Recorded as a blocker for public release readiness. |

## Outputs

- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/redaction_report.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`
- `split_ready/turingresearch-vggt-case/CASE_STUDY.md`
- `split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md`
- `split_ready/turingresearch-vggt-case/PRIVACY.md`

## Public Safety Decision

- observed: documentation-only draft created.
- observed: no raw data, model files, huge artifacts, private paths, keys, or bundles are included.
- local-observed: VGGT work-stream evidence is summarized as metadata only.
- requires-human-review: SparseConv3D success, advisor approval, promotion, and release readiness.
- missing: public safety checklist and original replication progress report.

## Repository Posture

The main TulingResearch Plus repository remains flagship. The split case is a derived, review-focused documentation package and must not become a substitute for the main project history, contracts, tests, or ledgers.
