# North Star

The VGGT / SMPL-X Human Prior line has shifted from:

`SMPL-X direct replacement -> SMPL-X feature encoding for VGGT`

## Rationale

Directly replacing VGGT output with SMPL-X is too brittle and risks turning the
system into a fallback or identity-copy path. The safer research direction is to
use SMPL-X as a structured human prior that can be encoded as features and then
tested against VGGT outputs through explicit hard gates.

## Working Hypothesis

SMPL-X feature encoding may help human-region geometry refinement if it is
introduced as evidence-backed features, not as a replacement result. Candidate
routes include voxel features, sparse latent fields, tri-plane or rasterized
features, and token / point residual integration.

## Non-Claims

- This pack does not claim the feature adapter improves VGGT.
- This pack does not claim SparseConv3D has succeeded.
- This pack does not claim the related work position is final.
- This pack does not claim visual proof is advisor-ready.
