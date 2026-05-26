# VGGT Run Comparison

This report compares metadata, boards, artifacts, hard gates, and failure labels.
It does not perform image understanding and is not an experiment result.

## Compared Runs

- `V770`
- `V129`
- `V260`
- `V999`
- `modal-sparseconv-fixture-001`

## Boards

- Available boards: `0`
- Missing or weak boards: `5`

- `V770` missing/weak `v770_proxy_mask.png`: `proxy-only`
- `V129` missing/weak `v129_hairline_delta.png`: `proxy-only`
- `V260` missing/weak `board_inventory`: `missing`
- `V999` missing/weak `board_inventory`: `missing`
- `modal-sparseconv-fixture-001` missing/weak `board_inventory`: `missing`

## Artifact Completeness

- `V770`: present `0`, missing `0`
- `V129`: present `0`, missing `0`
- `V260`: present `0`, missing `2`
- `V999`: present `0`, missing `0`
- `modal-sparseconv-fixture-001`: present `4`, missing `4`

## Visual Completeness

- `V770`: available `0`, missing `0`, proxy-only `1`
- `V129`: available `0`, missing `0`, proxy-only `1`
- `V260`: available `0`, missing `1`, proxy-only `0`
- `V999`: available `0`, missing `1`, proxy-only `0`
- `modal-sparseconv-fixture-001`: available `0`, missing `1`, proxy-only `0`

## Hard Gate Summary

- `V770`: passed `0`, failed `0`
- `V129`: passed `0`, failed `0`
- `V260`: passed `0`, failed `0`
- `V999`: passed `0`, failed `0`
- `modal-sparseconv-fixture-001`: passed `4`, failed `11`

## Failure Summary

- `MISSING_ASSETS`: `modal-sparseconv-fixture-001`
- `PACKAGE_INCOMPLETE`: `modal-sparseconv-fixture-001`
- `REAL_BACKEND_UNAVAILABLE`: `modal-sparseconv-fixture-001`
- `SPARSE_BACKEND_UNAVAILABLE`: `modal-sparseconv-fixture-001`
- `VISUAL_PROOF_INSUFFICIENT`: `modal-sparseconv-fixture-001`

## Claimed Improvements

- full human completion
- SparseConv3D promotion

## Unsupported Claims

- V770 cannot be claimed as full human completion.
- V260 is hard-blocked and should not be compared as success.
- V999 long-run does not equal promotion.
- SparseConv3D success requires real backend evidence.
- V999 has claims but status is not-enough-evidence.

## Next Actions

- V770: add advisor-ready board inventory.
- V129: add advisor-ready board inventory.
- V260: resolve hard blocker before comparison.
- V260: collect missing artifact metadata.
- V260: add advisor-ready board inventory.
- V999: add advisor-ready board inventory.
- modal-sparseconv-fixture-001: collect missing artifact metadata.
- modal-sparseconv-fixture-001: add advisor-ready board inventory.
- modal-sparseconv-fixture-001: collect real sparse backend evidence.

## Boundary

- Comparison is metadata/report level only.
- No Modal or VGGT execution was performed.
- Planned routes are not observed results.
- SparseConv3D success requires real backend evidence.
- Human review is required.
