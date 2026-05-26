# PDF Phase B Figure/Table Extraction

Round 41 implements the lightweight PDF Phase B extraction path for
TuringResearch Plus.

This is a local fixture-safe implementation. It does not run OCR, does not use
MinerU or Marker, does not download real papers, and does not copy copyrighted
PDF content into the repository.

## Implemented Surface

- `src/turing_research/pdf/asset_report.py`
- `src/turing_research/pdf/extractors/figure_extractor.py`
- `src/turing_research/pdf/extractors/table_extractor.py`
- `src/turing_research/pdf/extractors/page_map.py`
- `src/turing_research/pdf/extractors/section_tree.py`
- `src/turing_research_plus/paper/pdf_asset_import.py`

## Output Model

`PDFAssetExtractionReport` includes:

- `extracted_figures`
- `extracted_tables`
- `page_map`
- `section_tree`
- `extraction_warnings`
- `quality_score`
- optional `paper_registry_entries`

Each extracted figure records source PDF, page number, optional bbox, optional
output path, optional caption, extraction status, and warnings.

Each extracted table records source PDF, page number, extraction format,
optional output path, optional Markdown table, extraction status, and warnings.

## Lightweight Extraction Rules

- Figures: PyMuPDF embedded image metadata and optional image bytes extraction.
- Tables: simple pipe-delimited or tab-delimited text tables.
- Page map: page size, text character count, and image count.
- Section tree: simple heading detection from extractable text.

If PyMuPDF is unavailable, extraction returns warnings rather than breaking
package import.

## Paper Registry Integration

`turing_research_plus.paper.pdf_asset_import.register_pdf_assets` converts
extracted figures and tables into `FigureAssetRegistry` entries:

- figures become `pdf_extracted_figure`
- tables become `pdf_extracted_table`
- each entry records `original_pdf_source`
- every generated entry links to at least one ArticleBlock

## Non-Goals

- No OCR.
- No complex layout model.
- No MinerU / Marker integration.
- No live network access.
- No real paper analysis claim.
- No fabricated captions or paper results.
