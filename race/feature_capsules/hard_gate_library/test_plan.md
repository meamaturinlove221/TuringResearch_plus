# Test Plan: hard_gate_library

## Unit tests

- `test_gate_spec_validates_conditions`
- `test_gate_passes_with_required_evidence`
- `test_gate_blocks_on_hard_blocker`
- `test_gate_requires_human_review_for_ambiguous_input`
- `test_gate_preserves_not_enough_evidence`

## Contract tests

- `test_hard_gate_contract_fields`
- `test_hard_gate_status_labels_align_with_sprint1`

## Workflow tests

- Validate V260 hard-blocked fixture.
- Validate V999 non-final fixture.
- Validate SparseConv3D not-enough-evidence fixture.

## Non-goals

- No live execution.
- No network.
- No private VGGT path read.
