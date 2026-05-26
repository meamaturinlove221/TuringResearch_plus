# VGGT Related Work Graph

Status: fixture / requires human review.

## Nodes

- [[VGGT]]
- [[SMPL-X]]
- [[NeuralBody]]
- [[HumanRAM]]
- [[SparseConv3D]]
- [[tri-plane]]
- [[voxel feature]]
- [[hairline regression]]
- [[hand-object confusion]]
- [[hard gate]]
- [[failure taxonomy]]

## Edges

- [[NeuralBody]] -- `related_to` --> [[SparseConv3D]]
- [[HumanRAM]] -- `related_to` --> [[tri-plane]]
- [[SMPL-X]] -- `maps_to` --> [[feature adapter]]
- [[hard gate]] -- `blocks` --> [[promotion]]

All edges require source refs before final use.
