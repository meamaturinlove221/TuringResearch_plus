# Related Work Positioning Generator

Status: implemented minimal.

The Related Work Positioning Generator turns method cards, citation graph
context, and collision-risk outputs into a conservative planning report for a
future related-work section. It does not generate final paper prose and does
not claim novelty.

## Inputs

- `PaperMethodCard` or method-card-like dictionaries
- `CitationGraph` JSON
- `CollisionRiskReport`
- optional web summaries
- manual reviewer notes

## Output

`RelatedWorkPositioningReport` contains:

- `project_topic`
- `paper_groups`
- `method_clusters`
- `overlap_summary`
- `differentiation_points`
- `safe_claims`
- `unsafe_claims`
- `missing_evidence`
- `recommended_related_work_structure`
- `requires_human_review`

## VGGT Positioning Rules

- NeuralBody can be used as SMPL structured latent / sparse voxel inspiration,
  but the current fixture evidence does not make it a VGGT point-completion
  objective match.
- HumanRAM can be used as SMPL-X canonical / tri-plane / rasterized token
  inspiration, but the output target differs in current fixture evidence.
- HART may be closer to human reconstruction and needs focused review.
- VGGT-HPE may be lower risk if it is limited to head pose, but that must be
  confirmed.
- HGGT and Fus3D require real paper review before claims.

## Safety Boundary

- No default networking.
- No paper download.
- No final paper paragraph generation.
- No citation fabrication.
- No fake fixture output treated as complete review.
- No SparseConv3D success claim without evidence-ledger support.

## Recommended Use

Use this report to decide which papers to review next, which claims are safe to
make in an advisor update, and which claims must remain blocked until evidence
exists.
