# Experiment Routes

## Modal SparseConv3D Route

Status: planned / requires-real-experiment / not executed by TuringResearch.

Planned route:

1. Prepare Modal Linux GPU environment.
2. Probe real sparse backends: `spconv`, `MinkowskiEngine`, or `TorchSparse`.
3. Build SMPL-X voxel feature encoding.
4. Test SparseConv3D latent field.
5. Integrate with VGGT token / point residual route.
6. Run strict evaluation with hard gates.
7. Produce advisor and failure reports without automatic promotion.

## Hard Gates

- Real sparse backend required.
- Not report-only.
- Not fast-return.
- Not fallback-only.
- Not identity copy.
- No promotion without evidence.
- Candidate predictions included.
- Visual boards included.
- NPZ diff or thin summary included.
- Sha256 manifest included.
- Zip test clean.
- Cleanup report included.
- Hairline, hand/object, and full-body checks included.

## Artifact Requirements

- `final_status.json`
- `ranked_candidates.csv`
- `predictions.npz` or thin summary
- board inventory
- advisor summary
- failure report
- sha256 manifest
- cleanup report

## Fallback Rules

Fallbacks may be used for failure handling, but fallback-only output must not be
promoted as SparseConv3D evidence. Route compile is planning, not execution.
