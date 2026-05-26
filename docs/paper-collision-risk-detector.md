# TuringResearch Plus Paper Collision Risk Detector

Status: v0.2 beta minimal implementation.

Round 58 adds a conservative local rule engine for comparing the current
VGGT/SMPL-X feature adapter direction against paper method cards and citation
graph context. It does not prove novelty and does not replace human paper
review.

## Inputs

- local `PaperMethodCard` fixture data;
- fake/manual citation graph data;
- VGGT dogfooding context.

## Output

`CollisionRiskReport` contains:

- `target_project`
- `compared_papers`
- `overlap_matrix`
- `risk_scores`
- `safe_claims`
- `unsafe_claims`
- `positioning_notes`
- `missing_evidence`
- `requires_human_review`

## Overlap Dimensions

- task
- input
- output
- representation
- model component
- human prior usage
- SMPL / SMPL-X encoding
- VGGT token integration
- evaluation target
- dataset
- claimed contribution

## VGGT Positioning Rules

- NeuralBody is related through SMPL structured latent / sparseconv ideas, but
  current fixtures do not make it the same target as VGGT point completion.
- HumanRAM is related through SMPL-X tri-plane / rasterized pose features, but
  current fixtures mark target and output as different.
- HART may be closer to human reconstruction and requires focused review.
- VGGT-HPE may be lower risk if limited to head pose, but details require
  review.
- HGGT and Fus3D are `requires-real-paper-review`; no conclusion should be
  made from placeholders.

## Safe Boundary

The detector can say:

- likely overlap;
- possible risk;
- requires review;
- conservative positioning notes.

The detector must not say:

- definitive no collision;
- complete related work review;
- SparseConv3D success;
- final novelty claim.

## Default Execution

The detector is offline and deterministic. It does not call live citation graph
or Semantic Scholar unless a future workflow explicitly opts into live mode.
