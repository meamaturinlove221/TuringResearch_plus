# VGGT Case Study Refresh v1.5

Round: Optional 338.5
Date: 2026-05-25
Repository: TuringResearch Plus

## Purpose

Refresh a public-safe VGGT case study and split-ready draft from local scan outputs, then carry that draft onto the newer TuringResearch Plus cloud baseline. This round creates documentation only; it does not package data, copy artifacts, run VGGT, or promote claims.

## Inputs

| Input | Status | Notes |
| --- | --- | --- |
| Local scan summary | observed | Used as the primary case-study source. |
| Local scan artifact index | observed | Used only as metadata context. |
| Local scan missing-items report | observed | Missing and unconfirmed items remain guarded. |
| Local scan evidence ledger | observed | Used to preserve `local-observed` and `requires-human-review` statuses. |
| Local scan visual inventory | observed | Used as metadata only; no visual content copied. |
| Split-ready case directory | observed | Newer cloud baseline already includes a split-ready draft; this round refreshes claim-safety posture. |
| Public safety checklist doc | observed | Present in the newer cloud baseline. |
| Original replication progress report | observed | Present in the newer cloud baseline. |

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
- requires-human-review: final publication, advisor approval, and claim upgrades.

## Repository Posture

The main TuringResearch Plus repository remains flagship. The split case is a derived, review-focused documentation package and must not become a substitute for the main project history, contracts, tests, or ledgers.
