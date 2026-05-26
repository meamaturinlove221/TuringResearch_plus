# Paper Draft Assembly Beta

Status: implemented beta.

Round: 222.

The Paper Draft Assembly Beta turns existing paper scaffold and section
skeleton files into an evidence-linked draft package. It is a review package,
not a final paper writer.

## Inputs

The beta assembler reads existing local scaffold files:

- `paper_outline.md`
- `related_work_skeleton.md`
- `method_section_skeleton.md`
- `experiment_section_skeleton.md`
- `result_table_missing_items.md`
- `evidence_gap_report.md`
- `citation_safety_report.md`

## Outputs

The draft package includes:

- title candidates;
- abstract placeholder;
- introduction skeleton;
- related work skeleton;
- method skeleton;
- experiment skeleton;
- results blocked section;
- limitations;
- missing evidence report;
- unsafe claim report;
- citation status report.

Committed VGGT fake/demo output lives under:

- `examples/vggt-human-prior-survey/paper_scaffold/draft_beta/`

## Safety Boundary

- No final paper is generated.
- No final abstract is generated.
- No final result section is generated.
- No result value, metric, table, figure, or ablation is fabricated.
- Citation fixtures remain non-final until human review.
- Unsafe claims remain visible and blocked.
- SparseConv3D success is not claimed.
- Human review is required before any prose promotion.

## API

- `assemble_paper_draft_beta(scaffold_dir)`
- `export_paper_draft_package(package, output_dir)`
- `evaluate_paper_claims(text_by_section)`
- `parse_citation_status_report(markdown)`

## Tests

- `tests/unit/test_paper_draft_assembly.py`
- `tests/unit/test_paper_claim_guard.py`
- `tests/unit/test_citation_status_guard.py`
- `tests/workflow/test_vggt_paper_draft_beta_fake.py`
