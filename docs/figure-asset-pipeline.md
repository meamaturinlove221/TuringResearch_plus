# Figure Asset Pipeline

TuringResearch Plus keeps paper figures, extracted PDF assets, tables, and
captions in a local figure registry.

Round 41 adds a bridge from PDF Phase B asset reports into the existing paper
figure registry.

## Registry Rules

- No orphan figure.
- Every paper figure must have a caption.
- Every figure must link to at least one ArticleBlock.
- Generated diagrams use stable filenames.
- PDF extracted figures and tables must record `original_pdf_source`.

## PDF Phase B Integration

`PDFAssetExtractionReport` can be imported into the paper registry with
`register_pdf_assets`.

Supported imported asset kinds:

- `pdf_extracted_figure`
- `pdf_extracted_table`

This integration records provenance and registry readiness. It does not claim
that a real paper has been analyzed and does not fabricate captions beyond
metadata-based placeholder captions for registered local assets.
