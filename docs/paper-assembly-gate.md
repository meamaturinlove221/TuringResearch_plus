# Paper Assembly Gate

Status: implemented minimal.

The Paper Assembly Gate integrates the review-only paper scaffold, method
section skeleton, related-work draft skeleton, and experiment section skeleton.
It reports which sections are ready, partial, blocked, or
requires-human-review.

It does not generate a final paper.

## Inputs

- `paper_outline.md`
- `section_status.md`
- `evidence_gap_report.md`
- `method_section_skeleton.md`
- `method_figure_links.md`
- `related_work_skeleton.md`
- `citation_safety_report.md`
- `experiment_section_skeleton.md`
- `result_table_missing_items.md`

## Gate Checks

- Related work lacks real citation-grade references.
- Method section uses fixture-derived diagrams and requires review.
- Experiment section lacks real results.
- Result tables are missing.
- Unsafe claims remain blocked.
- Abstract must not be generated as a final version.
- Conclusion is blocked until results and claims are evidence-backed.

## Status Labels

- `ready`
- `partial`
- `blocked`
- `requires-human-review`

## Boundary

- No final paper is generated.
- No final abstract is generated.
- No final conclusion is generated.
- No result value is generated.
- No citation is fabricated.
- No SparseConv3D success claim is allowed.
