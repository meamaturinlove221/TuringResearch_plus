# Test Plan: vggt_smplx_evidence_ledger

## Unit tests

- `test_status_enum_accepts_planning_labels`
- `test_missing_local_evidence_marks_v120_v121_requires_human_review`
- `test_observed_and_local_observed_are_distinct`
- `test_review_ready_proxy_is_not_promotion`
- `test_ledger_serializes_to_markdown_and_json`

## Contract tests

- `test_vggt_evidence_ledger_contract_fields`
- `test_vggt_evidence_ledger_preserves_evidence_refs`

## Workflow tests

- Dry run from committed `local_scan_summary.md` and
  `local_scan_artifact_index.md`.

## Fixtures

- Fake milestone rows for V770, V129, V260, V900, V930, V999, V120, V121.
- Missing evidence ledger fixture.

## Non-goals

- No VGGT execution.
- No cross-machine sync.
- No private path reading by default.
