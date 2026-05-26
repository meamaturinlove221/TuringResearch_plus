# Modal SparseConv3D Route Pack

Status: planned / requires-real-experiment / not executed by TuringResearch.

This route pack prepares a VGGT-side experiment plan for Modal Real SparseConv3D
with SMPL-X voxel feature encoding. It is meant to be reviewed and executed
inside the VGGT project later. It does not contain experiment results.

## North Star

Move from:

```text
SMPL-X direct replacement
```

to:

```text
SMPL-X feature encoding for VGGT
```

The route should encode SMPL-X-derived voxel features into a sparse latent field
that can condition VGGT token / point residual behavior without replacing VGGT's
core objective.

## Planned Route

1. Use Modal Linux GPU only in the future VGGT execution environment.
2. Probe real sparse backends: `spconv`, `MinkowskiEngine`, or `TorchSparse`.
3. Build SMPL-X voxel feature encoding.
4. Produce a SparseConv3D latent field.
5. Integrate with VGGT token / point residual path.
6. Evaluate with strict hard gates.
7. Do not promote the route unless every required hard gate passes.

## Pack Contents

- `route_spec.yaml`
- `hard_gates.md`
- `failure_taxonomy.md`
- `codex_controller_prompt.md`
- `artifact_requirements.md`
- `advisor_summary.md`
- `architecture.mmd`

## Safety Boundary

- Do not run Modal from this pack.
- Do not run VGGT from this pack.
- Do not claim SparseConv3D success from this pack.
- Do not treat planned route compile as observed experiment evidence.
- Do not modify VGGT project files while reviewing this pack.
