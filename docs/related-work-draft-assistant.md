# Related Work Draft Assistant

Status: implemented minimal.

The Related Work Draft Assistant turns related-work positioning notes,
collision-risk reports, and paper digest fixtures into a related-work skeleton.
It is a review aid, not final paper prose.

## Inputs

- `examples/vggt-human-prior-survey/related_work/`
- `examples/vggt-human-prior-survey/collision_risk/`
- `examples/vggt-human-prior-survey/paper_digest/`

## Outputs

- `related_work_skeleton.md`
- `citation_safety_report.md`

## Skeleton Sections

- Feed-forward geometry
- Human prior / SMPL-X
- Neural body / sparse voxel
- Tri-plane / rasterized pose feature
- VGGT human extensions
- Difference from our route
- Requires review list
- Unsafe claims list

## Citation Safety

Every citation candidate records:

- `citation_id`
- `title`
- `source_status`
- `evidence_refs`
- `requires_human_review`
- `citation_grade`

Fixture digests such as NeuralBody and HumanRAM remain
`fake-or-manual-note`, not citation-grade evidence. HART, VGGT-HPE, HGGT, and
Fus3D remain `requires-real-paper-review`.

## Safety Boundary

- No final related-work paragraph is generated.
- No citation is fabricated.
- No claim of completed human review is made.
- Fake fixtures are not treated as real citations.
- Missing human review is listed explicitly.
- Human review is required before camera-ready paper text.

## Tests

- `tests/unit/test_related_work_builder.py`
- `tests/unit/test_citation_safety.py`
- `tests/workflow/test_vggt_related_work_draft_skeleton.py`
