# TuringResearch Plus Hard Gate Library

Status: implemented minimal for v0.2 Sprint 2.

The Hard Gate Library centralizes pass/block/requires-human-review and
not-enough-evidence checks for VGGT dogfooding routes. It keeps planned work,
missing evidence, hard blockers, and observed evidence separate.

## VGGT Gates

- `not_report_only`
- `not_fast_return`
- `not_identity_copy`
- `not_fallback_only`
- `no_promotion`
- `no_strict_registry`
- `no_v50_modification`
- `real_backend_required`
- `candidate_predictions_required`
- `visual_board_required`
- `npz_diff_required`
- `sha256_required`
- `zip_test_clean`
- `cleanup_required`
- `sparse_backend_probe_required`
- `smplx_alignment_risk_logged`
- `hairline_regression_checked`
- `hand_object_confusion_checked`

## Core Models

- `GateSpec`
- `GateCondition`
- `GateInputRef`
- `GateResult`
- `HardGateValidationReport`

## Rules

- Missing gate input does not pass.
- Hard-blocked input blocks.
- Planned or requires-real-experiment input is not enough evidence.
- Human-review input remains human-review.
- SparseConv3D success cannot be promoted without real evidence.

## Tool Boundary

Proposed capsule-local tool:

- command: `turing gates validate`
- tool: `experiment.hard_gate_validate`
- output: `HardGateValidationReport`

This is not a frozen public MCP API until root contracts and `docs/mcp-tools.md`
accept it.
