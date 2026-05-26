# Cross-project Evidence Graph: demo_workspace



- Project nodes: `2`

- Claim nodes: `7`

- Artifact nodes: `8`

- Method nodes: `11`

- Failure nodes: `7`

- Route nodes: `5`

- Requires human review: `true`

- Evidence source: `false`



## Shared Methods



- `method:advisor_review`: advisor review (demo_medical_imaging, vggt_human_prior)

- `method:artifact_review`: artifact review (demo_medical_imaging, vggt_human_prior)

- `method:route_planning`: route planning (demo_medical_imaging, vggt_human_prior)

- `method:visual_review`: visual review (demo_medical_imaging, vggt_human_prior)



## Shared Failures



- `failure:experiment_not_run`: experiment not run (demo_medical_imaging, vggt_human_prior)

- `failure:not_enough_evidence`: not enough evidence (demo_medical_imaging, vggt_human_prior)



## Shared Artifact Patterns



- `artifact:summary_artifact`: summary artifact (demo_medical_imaging, vggt_human_prior)

- `artifact:visual_review_artifact`: visual review artifact (demo_medical_imaging, vggt_human_prior)



## Shared Route Patterns



- `route:planned_route`: planned route (demo_medical_imaging, vggt_human_prior)



## Reusable Templates



- `planned_route_review_template`: Planned route review template (demo_medical_imaging, vggt_human_prior)

  - Caveat: Template reuse requires project-specific review and evidence.

- `artifact_pattern_review_template`: Artifact pattern review template (demo_medical_imaging, vggt_human_prior)

  - Caveat: Template reuse requires project-specific review and evidence.

- `missing_evidence_review_template`: Missing evidence review template (demo_medical_imaging, vggt_human_prior)

  - Caveat: Template reuse requires project-specific review and evidence.



## Claims Missing Evidence



- `claim:vggt_human_prior:1`

- `claim:vggt_human_prior:2`

- `claim:vggt_human_prior:3`

- `claim:demo_medical_imaging:1`

- `claim:demo_medical_imaging:3`



## Safety Boundary



- This graph is a reusable-pattern index, not a source of evidence.

- It does not transfer proof between projects.

- All cross-project reuse requires human review.



## Limitations



- Cross-project graph is a pattern index, not an evidence source.

- Evidence from one project is never applied to another project automatically.

- All reusable patterns require project-specific human review.
