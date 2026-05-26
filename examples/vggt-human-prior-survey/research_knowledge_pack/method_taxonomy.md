# Method Taxonomy

Status: fixture / requires human review.

## Key Concepts

- [[VGGT]]
- [[SMPL-X]]
- [[feature adapter]]
- [[SparseConv3D]]
- [[tri-plane]]
- [[voxel feature]]
- [[token injection]]
- [[point completion]]
- [[hairline regression]]
- [[hand-object confusion]]
- [[hard gate]]
- [[failure taxonomy]]

## Method Clusters

### Feed-forward Geometry

VGGT and related feed-forward geometry systems provide the base context for
point completion and geometry prediction.

### Human Prior Models

SMPL / SMPL-X-style priors provide structured human information, but must be
used as features or constraints rather than replacement outputs.

### Sparse Voxel / SparseConv Inspiration

NeuralBody-style sparse voxel reasoning motivates the planned SparseConv3D
route. Current evidence does not prove that route.

### Tri-plane / Rasterized Feature Inspiration

HumanRAM-style tri-plane and rasterized pose features motivate token-aligned
human priors for VGGT.

### Evaluation and Failure Control

Hard gates, failure taxonomy, visual boards, and artifact requirements define
when a route can be reviewed and when it must remain blocked.

## Missing Taxonomy Evidence

- Source refs for final paper claims.
- Real route outputs for SparseConv3D.
- Visual evidence nodes for full body, hairline, and hands.
- Dataset and evaluation target details for collision analysis.
