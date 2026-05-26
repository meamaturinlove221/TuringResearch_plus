# Paper Draft Beta Package: VGGT / SMPL-X Human Prior



- Package ID: `vggt_paper_draft_beta`

- Requires human review: `true`

- Status: `review-only-beta`



## Title Candidates



- SMPL-X Feature Encoding for VGGT Human Geometry Completion

- Human-Prior Feature Injection for Feed-forward 3D Geometry



## Abstract Placeholder



Abstract placeholder only. Real abstract prose is blocked until evidence, citations, results, and human review are complete.



## Introduction Skeleton



### Introduction



- Status: `needs-human-review`



- Frame the north star as SMPL-X feature encoding for VGGT.

- State the current work as research planning and evidence-gated development.



## Related Work Skeleton



# Related Work Skeleton: VGGT / SMPL-X feature encoding



This is a draft skeleton, not camera-ready related-work text.



## Feed-forward Geometry



- Start with feed-forward 3D geometry and VGGT context as background.

- Do not claim final novelty or absence of collision from fixture data.



## Human Prior / SMPL-X



- Frame the project as SMPL-X feature encoding for VGGT.

- Avoid presenting the route as direct SMPL-X replacement.



## Neural Body / Sparse Voxel



- Use NeuralBody as sparse voxel / structured latent inspiration only.

- Keep NeuralBody citation and collision status pending real paper review.



## Tri-plane / Rasterized Pose Feature



- Use HumanRAM as SMPL-X canonical / tri-plane / rasterized feature inspiration only.

- Keep HumanRAM citation and collision status pending real paper review.



## VGGT Human Extensions



- Treat HART as potentially closer and requiring focused review.

- Treat VGGT-HPE, HGGT, and Fus3D as requires-real-paper-review items.



## Difference From Our Route



- Current route is SMPL-X feature encoding for VGGT.

- SparseConv3D remains planned / requires-real-experiment.

- This skeleton does not establish final related-work positioning.



## Citation Candidates



- `humanram-fixture` source_status=`fake-or-manual-note`

- `neuralbody-fixture` source_status=`fake-or-manual-note`

- `hart-review-needed` source_status=`requires-real-paper-review`

- `vggt-hpe-review-needed` source_status=`requires-real-paper-review`

- `hggt-review-needed` source_status=`requires-real-paper-review`

- `fus3d-review-needed` source_status=`requires-real-paper-review`



## Requires Review



- HART: may be closer to human reconstruction and needs focused review.

- VGGT-HPE: collision risk depends on whether it is mainly head pose or broader human geometry.

- HGGT: requires real paper review before positioning.

- Fus3D: requires real paper review before positioning.

- NeuralBody and HumanRAM: fixture method cards must be replaced or supported by citation-grade evidence before final paper text.



## Unsafe Claims



- There is definitively no collision with existing papers. Reason: Fake/manual method cards and fake citation graph are not sufficient evidence.

- The related work has been completely reviewed. Reason: Fixtures explicitly require real paper review.

- SparseConv3D integration is already successful. Reason: That requires real experiment evidence from the evidence ledger.

- Humanram is safe to ignore. Reason: Humanram has unknown collision risk and needs review.

- Neuralbody is safe to ignore. Reason: Neuralbody has unknown collision risk and needs review.

- HART requires-real-paper-review is safe to ignore. Reason: HART requires-real-paper-review has unknown collision risk and needs review.

- VGGT-HPE requires-real-paper-review is safe to ignore. Reason: VGGT-HPE requires-real-paper-review has unknown collision risk and needs review.

- HGGT requires-real-paper-review is safe to ignore. Reason: HGGT requires-real-paper-review has unknown collision risk and needs review.

- Fus3D requires-real-paper-review is safe to ignore. Reason: Fus3D requires-real-paper-review has unknown collision risk and needs review.



## Evidence Refs



- `examples/vggt-human-prior-survey/related_work/related_work_positioning.md`

- `examples/vggt-human-prior-survey/related_work/safe_related_work_claims.md`

- `examples/vggt-human-prior-survey/related_work/requires_review.md`

- `examples/vggt-human-prior-survey/collision_risk/collision_risk_report.md`

- `examples/vggt-human-prior-survey/collision_risk/unsafe_claims.md`

- `examples/vggt-human-prior-survey/paper_digest/humanram_digest.fixture.md`

- `examples/vggt-human-prior-survey/paper_digest/neuralbody_digest.fixture.md`

- `examples/vggt-human-prior-survey/related_work/requires_review.md`

- `examples/vggt-human-prior-survey/related_work/requires_review.md`

- `examples/vggt-human-prior-survey/related_work/requires_review.md`

- `examples/vggt-human-prior-survey/related_work/requires_review.md`



## Boundary



- No final related-work paragraph is generated.

- No citation is fabricated.

- Fixture digests are not citation-grade evidence.

- Human review is required before paper claims.



## Method Skeleton



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



## Experiment Skeleton



# Experiment Section Skeleton: VGGT / SMPL-X Human Prior



This is an evidence-linked skeleton, not a paper results section.



## Dataset / Setup Placeholder



- Dataset/setup details remain placeholders until real experiment logs exist.

- Do not infer dataset results from route or dashboard fixtures.



## Baselines



- VGGT baseline placeholder requires real run evidence.

- Human-prior route comparison requires real run evidence.



## Ablations



- SMPL-X feature encoding ablation placeholder.

- SparseConv3D backend ablation placeholder.

- Visual proof ablation placeholder.



## Metrics



- Metric names may be planned, but result values are blocked.

- Quantitative tables require real predictions and manifest evidence.



## Route Status



- Route status: `requires-real-experiment`

- Run status: `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`

- Backend status: `real_backend_missing`



## Missing Result Tables



- main_quantitative_results

- ablation_results

- failure_case_visual_table



## Failure Cases



- REAL_BACKEND_UNAVAILABLE

- SPARSE_BACKEND_UNAVAILABLE

- MISSING_ASSETS

- VISUAL_PROOF_INSUFFICIENT

- PACKAGE_INCOMPLETE



## Planned Experiments



- Run real SparseConv3D backend probe before result writing.

- Collect predictions, visual board, sha256 manifest, and cleanup report.

- Re-run visual readiness checks before advisor or paper promotion.



## Not-ready Claims



- Planned route is not an executed experiment.

- Dashboard is not a paper result.

- SparseConv3D success is not established.

- Quantitative result tables are missing.

- Hard gate pending: `no_promotion`

- Hard gate pending: `real_backend_required`

- Hard gate pending: `sparse_backend_probe_required`

- Hard gate pending: `candidate_predictions_required`

- Hard gate pending: `visual_board_required`

- Hard gate pending: `cleanup_required`



## Evidence Refs



- `examples/vggt-human-prior-survey/run_ingest_report.md`

- `examples/vggt-human-prior-survey/dashboard/run_dashboard.md`

- `examples/vggt-human-prior-survey/dashboard/status_board.md`

- `examples/vggt-human-prior-survey/dashboard/failure_board.md`

- `examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml`



## Boundary



- No result value is generated.

- Planned is not executed.

- Dashboard is not a paper result.

- Failure analysis is internal analysis until paper evidence exists.

- No figure or table is fabricated.



## Results Blocked Section



# Result Table Missing Items



- Result tables allowed: `false`

- Planned is not executed: `true`

- Dashboard is not result: `true`

- Requires human review: `true`



## Missing Result Tables



- main_quantitative_results

- ablation_results

- failure_case_visual_table



## Missing Artifacts



- `predictions.npz`

- `board_inventory.md`

- `sha256_manifest.txt`

- `cleanup_report.md`



## Blocked Claims



- Do not report quantitative result values without real run evidence.

- Do not claim planned route execution as completed.

- Do not treat dashboard status as a paper result.

- Do not claim SparseConv3D success without backend evidence.

- Run status `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS` is not ready for result tables.

- Route status `requires-real-experiment` is not executed.



## Boundary



- No result value is generated.

- No figure or table is fabricated.

- Missing tables stay missing until real evidence exists.



## Limitations



### Limitations



- Status: `needs-human-review`



- State that current evidence is not enough for final experiment claims.

- State that visual readiness and artifact completeness remain blockers.



Unsafe claims:

- Do not claim SparseConv3D success.

- Do not claim full human completion.

- Do not claim final novelty against HART / HGGT / Fus3D without review.

- Do not report quantitative experiment numbers without real evidence.



## Safety Boundary



- This is a scaffold, not final paper prose.

- No final abstract is generated.

- No final results are generated.

- Planned experiments stay in the experiment plan.



## Safety Boundary



- This is not a final paper.

- No final abstract is generated.

- No final result section is generated.

- No result value, table, figure, metric, or ablation is fabricated.

- Human review is required before any paper prose can be promoted.
