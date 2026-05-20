# Test Plan: pdf_phase_b_figure_table_extraction

## Unit tests

- `test_fixture_pdf_figure_extraction_metadata`
- `test_fixture_pdf_table_extraction_metadata`
- `test_page_provenance_recorded`
- `test_empty_extraction_emits_warning`
- `test_asset_report_serializes_to_markdown_and_json`

## Contract tests

- `test_pdf_extract_figures_contract_fields`
- `test_pdf_extract_tables_contract_fields`
- `test_pdf_assets_align_with_figure_registry`

## Workflow tests

- Dry run with tiny fixture PDF.
- Dry run with unsupported scanned-like fixture.

## Fixtures

- Tiny PDF with a simple drawn figure.
- Tiny PDF with a simple table.
- Empty PDF fixture.

## Non-goals

- No OCR.
- No heavy layout parsing.
- No external services.
- No cross-machine sync.

