# Test Plan: visual_evidence_auditor

## Unit tests

- `test_proxy_heatmap_classification`
- `test_mask_delta_board_classification`
- `test_full_pointcloud_proxy_classification`
- `test_true_region_pointcloud_closeup_classification`
- `test_unknown_visual_artifact_requires_human_review`
- `test_missing_visual_inventory_blocks_readiness`

## Contract tests

- `test_visual_evidence_audit_report_contract_fields`
- `test_visual_items_require_source_artifact_reference`

## Workflow tests

- Dry run from fake board inventory.
- Dry run with missing `local_scan_visual_inventory.md`.

## Fixtures

- Tiny fake PNG/JPG files.
- Visual sidecar labels.
- Missing visual inventory fixture.

## Non-goals

- No image generation.
- No image content inference beyond sidecar/metadata classification.
- No cross-machine sync.
