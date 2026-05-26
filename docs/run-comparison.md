# Run Comparison

Status: v0.4 minimal metadata implementation.

The Run Comparison module compares VGGT / SMPL-X experiment runs at the metadata
and report level. It combines board availability, artifact completeness, hard
gate results, failure categories, claimed improvements, unsupported claims, and
next actions.

It does not run Modal, does not run VGGT, does not read private VGGT paths, and
does not perform image understanding.

## Outputs

`RunComparisonReport` contains:

- `compared_runs`
- `available_boards`
- `missing_boards`
- `artifact_completeness`
- `visual_completeness`
- `hard_gate_summary`
- `failure_summary`
- `claimed_improvements`
- `unsupported_claims`
- `next_actions`

## VGGT Rules

- V770 cannot be written as full human completion without evidence.
- V129 local positive findings must keep the regression warning.
- V260 hard-blocked routes are not comparable as successful runs.
- V999 long-run status is not promotion.
- SparseConv3D success requires real backend evidence.

## Example Use

The committed VGGT fixture compares V770, V129, V260, V999, and the Modal
SparseConv3D route dashboard. It intentionally keeps V999 and the Modal route as
not-enough-evidence review items, not successful SparseConv3D outcomes.

## Non-Goals

- No image classification.
- No pixel comparison.
- No automatic promotion.
- No final experiment conclusion.
- No private VGGT path reads.
