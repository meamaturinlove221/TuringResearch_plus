---
name: tulingresearch-pdf-phase-b-figure-table-extraction
description: Use when planning or implementing the PDF Phase B figure/table extraction capsule.
---

# TulingResearch Plus Skill: pdf_phase_b_figure_table_extraction

## Role

Maintain the Sprint 1 PDF Phase B figure/table extraction capsule.

## When to use

Use when a task touches `pdf.extract_figures`, `pdf.extract_tables`, PDF asset
provenance, table metadata, or paper figure registry alignment.

## Inputs

- Local fixture PDFs
- PDF Markdown Phase A outputs
- PDF Phase B contracts
- Paper figure registry expectations

## Outputs

- `PDFAssetExtractionReport`
- Figure/table metadata
- Warning list

## Required files

- `race/feature_capsules/pdf_phase_b_figure_table_extraction/FEATURE.md`
- `race/feature_capsules/pdf_phase_b_figure_table_extraction/contract.yaml`
- `race/feature_capsules/pdf_phase_b_figure_table_extraction/sop.mmd`
- `race/feature_capsules/pdf_phase_b_figure_table_extraction/test_plan.md`

## Related contracts

- `contracts/pdf_markdown.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/03_pdf_markdown.md`
- `lanes/14_v0.2_sprint_1.md`
- `lanes/16_vggt_feature_capsules.md`

## Required tests

- Fixture PDF figure extraction.
- Fixture PDF table extraction.
- Provenance and warning serialization.

## Rules / constraints

- Do not implement OCR in this sprint.
- Do not call external services.
- Do not fabricate captions or paper claims.
- Do not implement Future Sync Adapters in Sprint 1.

## Done criteria

- Figure/table outputs have page provenance.
- Empty or unsupported extraction emits warnings.
- Existing PDF Markdown Phase A behavior remains compatible.

