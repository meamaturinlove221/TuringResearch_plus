# Test Plan: failure_taxonomy_engine

## Unit tests

- `test_known_label_normalizes_to_category`
- `test_unknown_label_requires_human_review`
- `test_severity_mapping_is_deterministic`
- `test_next_action_preserved`
- `test_visual_not_ready_not_same_as_experiment_failure`

## Contract tests

- `test_failure_taxonomy_contract_fields`
- `test_failure_report_serializes_to_json_and_markdown`

## Workflow tests

- Analyze V260 hard-blocked fixture.
- Analyze missing visual evidence fixture.
- Analyze SparseConv3D not-enough-evidence fixture.

## Non-goals

- No VGGT execution.
- No success inference.
- No network.
