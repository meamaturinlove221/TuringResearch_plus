# Experiment Section Builder

Status: implemented minimal.

The Experiment Section Builder turns route DSL, run ingest reports, dashboard
summaries, and failure taxonomy outputs into a review-only experiment section
skeleton. It does not write result values or generate quantitative tables.

## Inputs

- `examples/vggt-human-prior-survey/run_ingest_report.md`
- `examples/vggt-human-prior-survey/dashboard/`
- `examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml`

## Outputs

- `experiment_section_skeleton.md`
- `result_table_missing_items.md`

## Skeleton Sections

- Dataset / setup placeholder
- Baselines
- Ablations
- Metrics
- Route status
- Run status
- Missing result tables
- Failure cases
- Planned experiments
- Not-ready claims

## Result Table Guard

The result table guard blocks result tables when predictions, visual boards,
sha256 manifests, cleanup reports, or backend evidence are missing. Dashboard
status is treated as review material only, not paper result evidence.

## Safety Boundary

- No result values are generated.
- Planned experiments are not treated as executed experiments.
- Dashboard summaries are not paper results.
- Failure analysis can be listed as internal analysis.
- No figure or table is fabricated.
- SparseConv3D success is not claimed without evidence.

## Tests

- `tests/unit/test_experiment_section_builder.py`
- `tests/unit/test_result_table_guard.py`
- `tests/workflow/test_vggt_experiment_section_skeleton.py`
