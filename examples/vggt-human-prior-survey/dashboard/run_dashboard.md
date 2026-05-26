# Run Dashboard: modal-sparseconv-fixture-001

[ROUTE_EXHAUSTED] [NOT_ENOUGH_EVIDENCE] [REQUIRES_HUMAN_REVIEW]

- Route id: `modal_sparseconv_v0`
- Run status: `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`
- Backend status: `real_backend_missing`
- Candidate count: `1`
- Best candidate: `fallback-proxy`
- Visual readiness: `blocked: visual proof insufficient`
- Advisor readiness: `not-ready: backend evidence missing`
- Next action: collect real sparse backend log before making success claims

## Hard Gates

- [x] `not_report_only` - passed in fixture metadata
- [ ] `not_fallback_only` - failed in fixture metadata
- [ ] `real_backend_required` - failed in fixture metadata
- [ ] `candidate_predictions_required` - failed in fixture metadata
- [ ] `visual_board_required` - failed in fixture metadata
- [ ] `cleanup_required` - failed in fixture metadata
- [ ] `real_sparse_backend_required` - real sparse backend log is required
- [x] `final_status.json_required` - required artifact present
- [x] `ranked_candidates.csv_required` - required artifact present
- [ ] `predictions.npz_required` - required artifact missing
- [ ] `board_inventory.md_required` - required artifact missing
- [x] `advisor_summary.md_required` - required artifact present
- [x] `failure_report.md_required` - required artifact present
- [ ] `sha256_manifest.txt_required` - required artifact missing
- [ ] `cleanup_report.md_required` - required artifact missing

## Artifact Completeness

- Present: `4`
- Missing: `4`

- missing `predictions.npz`
- missing `board_inventory.md`
- missing `sha256_manifest.txt`
- missing `cleanup_report.md`

## Failure Categories

- `REAL_BACKEND_UNAVAILABLE`
- `SPARSE_BACKEND_UNAVAILABLE`
- `MISSING_ASSETS`
- `VISUAL_PROOF_INSUFFICIENT`
- `PACKAGE_INCOMPLETE`

## Boundary

- Dashboard did not run Modal.
- Dashboard did not run VGGT.
- Dashboard displays already ingested evidence only.
- Dashboard is not an experiment result.
