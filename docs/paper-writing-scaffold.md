# Paper Writing Scaffold

Status: implemented minimal.

The Paper Writing Scaffold organizes existing research material into a safe
paper-writing structure. It uses evidence summaries, method notes, related-work
positioning, and experiment route plans to produce review material, not final
paper prose.

## Outputs

- `paper_outline.md`
- `section_status.md`
- `evidence_gap_report.md`

## Data Model

`PaperScaffold` records:

- `title_candidates`
- `abstract_status`
- `introduction_plan`
- `related_work_plan`
- `method_plan`
- `experiment_plan`
- `results_status`
- `limitation_plan`
- `evidence_requirements`
- `missing_experiments`
- `unsafe_claims`
- `requires_human_review`

Each section is a plan-only structure with status, bullets, evidence refs,
missing evidence, unsafe claims, and human review notes.

## VGGT Usage

The VGGT scaffold is built from the research knowledge pack under
`examples/vggt-human-prior-survey/research_knowledge_pack/`.

It keeps the current project state conservative:

- SparseConv3D success is not claimed.
- Planned Modal routes stay in the experiment plan.
- Missing board-level visual evidence is listed.
- HART / HGGT / Fus3D / VGGT-HPE remain requires-real-paper-review.
- Quantitative experiment values are blocked unless real evidence exists.

## Safety Rules

- Do not write final results.
- Do not generate a final abstract.
- Do not fabricate experiment numbers.
- Keep planned experiments in `experiment_plan`.
- Always list missing evidence.
- Always list unsafe claims.
- Keep `requires_human_review=true`.

## Non-goals

- No automatic paper writing.
- No automatic citation generation.
- No final claim generation.
- No PDF/PPTX export.
- No network access.
- No private VGGT path access.

## Tests

- `tests/unit/test_paper_write_models.py`
- `tests/unit/test_paper_scaffold.py`
- `tests/unit/test_paper_section_status.py`
- `tests/unit/test_paper_evidence_linker.py`
- `tests/workflow/test_vggt_paper_scaffold_fake.py`
