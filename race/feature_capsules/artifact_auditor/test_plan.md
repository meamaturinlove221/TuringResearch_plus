# Test Plan: artifact_auditor

## Unit tests

- `test_valid_zip_bundle_passes`
- `test_broken_zip_bundle_reports_error`
- `test_sha256_is_stable`
- `test_manifest_completeness_detected`
- `test_missing_npz_is_warning_or_blocker`
- `test_sidecar_consistency_checked`
- `test_no_write_into_linked_project`

## Contract tests

- `test_artifact_audit_report_contract_fields`
- `test_artifact_records_preserve_source_path_metadata`

## Workflow tests

- Dry run with committed fixture bundle.
- Dry run with no artifacts scanned.

## Fixtures

- Tiny zip bundle.
- Broken zip bundle.
- Missing-npz bundle.
- Board inventory sidecar.

## Non-goals

- No VGGT execution.
- No remote sync.
- No private artifact commit.

