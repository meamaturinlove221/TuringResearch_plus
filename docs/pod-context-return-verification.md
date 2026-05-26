# Pod Context Return Verification

Status: v1.0 prelaunch policy.

Pod output is accepted only as proposed return material for human review.

## Required Return Files

- `RETURN_MANIFEST.yaml`
- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

## Required Return Metadata

- `context_package_id`
- `route_id`
- `target_environment_label`
- `return_package_id`
- `sha256_manifest`

## Rules

- Missing `RETURN_MANIFEST.yaml` is a blocker.
- Metadata mismatch is a blocker.
- Proposed evidence updates are review inputs only.
- Returned failure reports are useful, but they do not prove experiment success.
- No returned file can auto-update the Evidence Ledger.
