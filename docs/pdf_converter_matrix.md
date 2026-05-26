# TuringResearch Plus PDF Converter Matrix

This matrix compares candidate converter routes for PDF Markdown Phase B.
Round 41 implements only the lightweight PyMuPDF route for figures, simple text
tables, page maps, and section trees.

## Converter Summary

| Converter | Use case | Dependency weight | Phase B role |
| --- | --- | --- | --- |
| PyMuPDF | Existing local text extraction and basic asset access | light | implemented lightweight Phase B route |
| pdfplumber | Tables and layout hints for digital PDFs | medium | optional table/layout route |
| Marker optional | Higher quality document-to-markdown route | heavy | optional future route |
| MinerU optional | Rich paper layout understanding | heavy | optional future route |
| OCR future | Scanned PDFs and image-only pages | heavy | future only |

## PyMuPDF

- Use case: local PDF inspection, text extraction, page iteration, simple asset extraction.
- Strengths: already used in Phase A, fast, local, suitable for small fixtures.
- Limitations: limited table semantics, limited high-level section structure, scanned PDFs need OCR.
- Dependency weight: light optional `pdf` extra.
- Test strategy: tiny generated fixture PDFs, invalid PDF tests, empty PDF warnings, cache-hit tests.
- Fallback behavior: if unavailable, return typed `converter_unavailable` error without breaking package import.
- Round 41 status: implemented for embedded figures, simple text tables, page
  map, and heading-based section tree.

## pdfplumber

- Use case: table extraction, layout hints, bounding boxes for digital PDFs.
- Strengths: useful for table structure and page layout in text-based PDFs.
- Limitations: not reliable for scanned PDFs, may be slower, adds another optional dependency.
- Dependency weight: medium optional future extra.
- Test strategy: tiny fixture with a simple table, no network, skipped if optional dependency absent unless fake adapter is used.
- Fallback behavior: fall back to PyMuPDF text route and emit table extraction warning.

## Marker Optional

- Use case: richer document-to-markdown conversion when users opt in.
- Strengths: potentially better markdown structure for papers.
- Limitations: heavier dependency footprint, may be model/resource sensitive, not appropriate for default path.
- Dependency weight: heavy optional route.
- Test strategy: protocol/fake adapter tests by default; manual tests only when installed.
- Fallback behavior: fall back to PyMuPDF route and record converter route warning.

## MinerU Optional

- Use case: richer scientific paper layout parsing and asset detection when users opt in.
- Strengths: potentially strong for paper-style layouts and figures/tables.
- Limitations: heavy dependency and environment requirements; may not be suitable for CI defaults.
- Dependency weight: heavy optional route.
- Test strategy: fake adapter and contract tests by default; manual tests for installed environments.
- Fallback behavior: fall back to PyMuPDF or pdfplumber routes and record unsupported route warning.

## OCR Future

- Use case: scanned PDFs and image-only pages.
- Strengths: required for documents with no extractable text.
- Limitations: high dependency cost, accuracy variability, language and layout complexity.
- Dependency weight: heavy future route.
- Test strategy: future manual/fixture tests; not part of Phase B implementation.
- Fallback behavior: emit explicit OCR-not-enabled warning and keep text route output if available.

## Selection Rule

Default route remains local and lightweight. Heavier converters must be optional, explicitly configured, and covered by fake or manual tests before use in workflows.
