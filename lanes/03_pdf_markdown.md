# Lane 03: PDF Markdown

## Scope

Define PDF input to Markdown models and contract for a minimal local PyMuPDF route.

## Outputs

- `contracts/pdf_markdown.yaml`
- `docs/pdf_markdown.md`
- `src/turing_research/pdf/models.py`
- `tests/unit/test_pdf_markdown_models.py`

## Status

Phase 1 complete. Heavy OCR is out of scope.

## Round 2 Update

2026-05-19: Implemented Phase A local PDF to Markdown path:

- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.cache_lookup`
- `pdf.markdown_content`

The implementation supports local PDF paths, a replaceable PyMuPDF converter adapter, Markdown file output, simple section heading detection, page map output, and CacheManager entries in the `pdf/markdown` namespace.

Out of scope remains heavy OCR, complex layout understanding, real external APIs, paper fetching, paper searching, and fusion workflows.

Validation passed:

- `python -m pytest`
- `python -m ruff check .`
- `python -m mypy src`

## Round 33 Phase B Planning

2026-05-20: Planned PDF Markdown Phase B without implementing heavy features.

Created or updated:

- `docs/pdf_phase_b_plan.md`
- `docs/pdf_converter_matrix.md`
- `contracts/pdf_markdown.yaml`
- `tests/fixtures/pdf/README.md`

Phase B planning covers:

- `pdf.extract_figures`
- `pdf.extract_tables`
- `pdf.sectionize`
- page map compatibility
- section tree
- quality score v2
- PDF assets registration
- integration with `paper.figure_register`
- integration with `vault.ingest_source`

Converter matrix covers PyMuPDF, pdfplumber, Marker optional, MinerU optional, and OCR future routes.

Restrictions preserved:

- No OCR implementation.
- No heavy default dependency.
- No real external service call.
- No implementation-status promotion for contract-only Phase B tools.

Validation:

- `python -m pytest tests/contract/test_contract_schema_integrity.py tests/contract/test_tool_namespace_integrity.py tests/contract/test_name_integrity.py` passes with 10 tests.
- `python -m pytest tests/unit/test_pdf_markdown_models.py tests/unit/test_pdf_markdown_pipeline.py tests/workflow/test_example_pdf_to_markdown.py` passes with 9 tests.
- `python -m ruff check .` passes.
- `python -m pytest tests/contract` passes with 72 tests.
- `python -m mypy src` passes.
- Forbidden naming scan has no hits.
