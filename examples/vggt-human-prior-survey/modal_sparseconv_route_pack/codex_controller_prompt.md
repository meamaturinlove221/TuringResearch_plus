# Codex Controller Prompt: Modal Real SparseConv3D Route

You are working inside the VGGT project, not inside TuringResearch Plus.

Goal: run or prepare the Modal Real SparseConv3D + SMPL-X voxel feature
encoding route for VGGT, producing evidence-backed artifacts. Do not treat this
prompt as proof that the route has already run.

## Non-Negotiable Rules

- Do not fast-return.
- Do not produce report-only output.
- Do not promote planned work to observed evidence.
- Do not claim SparseConv3D success without real backend evidence.
- Do not use fallback-only output as SparseConv3D success.
- Do not use identity copy output as candidate success.
- Do not modify unrelated VGGT project files.
- Do not hide missing assets.
- If the route fails, produce failure analysis with taxonomy labels.

## Required Backend Probe

1. Confirm Modal Linux GPU runtime.
2. Probe real sparse backend availability:
   - `spconv`
   - `MinkowskiEngine`
   - `TorchSparse`
3. Save backend probe logs.
4. If no real backend is available, stop promotion and classify the route as
   `REAL_BACKEND_UNAVAILABLE` or `SPARSE_BACKEND_UNAVAILABLE`.

## Required Route Steps

1. Build or load SMPL-X voxel feature encoding.
2. Pass voxel features through real SparseConv3D only if a real backend is
   available.
3. Integrate sparse latent field into VGGT token / point residual path.
4. Produce candidate predictions.
5. Produce visual boards:
   - full body
   - hairline / head boundary
   - hand / object close-up
6. Produce NPZ diff or a thin summary comparing baseline vs candidate.
7. Produce `final_status.json`, `ranked_candidates.csv`, `sha256` manifest,
   cleanup report, advisor summary, and failure report.

## Required Final Output

If successful, output evidence-backed artifacts only. If blocked or failed,
output:

- failure category;
- evidence refs;
- missing assets;
- retry policy;
- concrete next action;
- human review requirement if applicable.

Never write that the route is successful unless the real artifacts prove it.
