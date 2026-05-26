# Method Section Skeleton: VGGT / SMPL-X Human Prior



This is an evidence-linked skeleton, not a final method section.



## Problem Setting



- Describe a human-prior route for VGGT without claiming completion.

- Treat method-card fixtures as comparison vocabulary and review inputs.



## Overview



- Organize the method around SMPL-X feature encoding, VGGT integration, and route-gated validation.

- Use NeuralBody / HumanRAM fixture notes as inspiration only, not copied method claims.



## SMPL-X Feature Encoding



- Represent SMPL-X as feature encodings rather than direct mesh output replacement.

- Candidate encodings include voxel, tri-plane, and token-aligned features; all remain evidence-gated.

- Borrowable comparison terms: feature encoding comparison point for VGGT dogfooding

- Borrowable comparison terms: human-specific method card vocabulary

- Borrowable comparison terms: body-prior-conditioned representation as a comparison lens

- Borrowable comparison terms: separation of geometry representation from VGGT general objective



## VGGT Integration



- Place human-prior features at the VGGT token or point-residual interface as a planned architecture section.

- Separate adapter design from verified experiment outputs.



## Route Variants



- `modal_sparseconv_v0`: `requires-real-experiment`; final states remain planned, requires-real-experiment, not executed by TuringResearch.



## Hard Gates



- `no_promotion` must pass before method/result promotion.

- `real_backend_required` must pass before method/result promotion.

- `sparse_backend_probe_required` must pass before method/result promotion.

- `candidate_predictions_required` must pass before method/result promotion.

- `visual_board_required` must pass before method/result promotion.

- `cleanup_required` must pass before method/result promotion.



## Implementation Notes



- Implementation notes are derived from route DSL and architecture diagrams.

- No Modal or VGGT execution is represented by this section skeleton.

- Do not copy: implementation details

- Do not copy: paper text

- Do not copy: evaluation claims without real paper evidence

- Do not copy: implementation details

- Do not copy: paper text

- Do not copy: claims without real paper evidence



## Limitations



- Architecture diagrams are derived from fixtures and require human review.

- Method cards require real paper review before citation-grade use.

- SparseConv3D backend success is not established by this skeleton.

- Experiment evidence is missing, so results wording must remain blocked.



## Figure Placeholders



- `humanram_mapping` - Humanram Mapping

- `modal_sparseconv_route` - Modal Sparseconv Route

- `neuralbody_mapping` - Neuralbody Mapping



## Evidence Refs



- `examples/vggt-human-prior-survey/paper_method_cards/humanram.fixture.md`

- `examples/vggt-human-prior-survey/paper_method_cards/neuralbody.fixture.md`

- `examples/vggt-human-prior-survey/architecture_diagrams/humanram_mapping.mmd`

- `examples/vggt-human-prior-survey/architecture_diagrams/modal_sparseconv_route.mmd`

- `examples/vggt-human-prior-survey/architecture_diagrams/neuralbody_mapping.mmd`

- `examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml`



## Unsafe Claims



- Do not claim the method is fully experimentally verified.

- Do not claim SparseConv3D success.

- Do not claim final contribution over related work.

- Do not fabricate figures, tables, metrics, or ablation results.



## Safety Boundary



- No final contribution claims are generated.

- No method verification is claimed.

- No experiment, figure, table, metric, or ablation result is fabricated.

- Human review is required before drafting paper prose.
