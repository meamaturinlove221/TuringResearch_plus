# Lane 67 - Experiment Board Index + Run Comparison

Status: implemented minimal.

Round: 86.

## Scope

Implemented a metadata/report-level run comparison layer for VGGT / SMPL-X
experiments. The layer compares board availability, artifact completeness, hard
gate summaries, failure categories, claimed improvements, unsupported claims,
and next actions.

## Added

- `src/turing_research_plus/run_compare/`
- `contracts/run_comparison.yaml`
- `docs/experiment-board-index.md`
- `docs/run-comparison.md`
- `examples/vggt-human-prior-survey/run_comparison/vggt_run_comparison.md`
- run comparison unit and workflow tests

## Boundaries

- No Modal execution.
- No VGGT execution.
- No network access.
- No private VGGT path reads.
- No image understanding.
- No planned-as-observed promotion.
- No SparseConv3D success claim without real backend evidence.

## VGGT Rules Preserved

- V770 is not full human completion.
- V129 local positive keeps regression warning.
- V260 hard-blocked is not success.
- V999 long-run is not promotion.
- SparseConv3D success requires backend evidence.
