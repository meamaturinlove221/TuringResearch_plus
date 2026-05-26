# TuringResearch Plus PDF Markdown Phase B Plan

Round 33 plans PDF Markdown Phase B. This is design and backlog work only; it does not implement OCR, add heavy dependencies, or call external services.

## Goals

- Plan `pdf.extract_figures`.
- Plan `pdf.extract_tables`.
- Plan `pdf.sectionize`.
- Improve page map and section tree contracts.
- Define quality score v2.
- Define PDF asset registration expectations.
- Define integration with `paper.figure_register`.
- Define integration with `vault.ingest_source`.

## Non-Goals

- No OCR implementation.
- No heavy dependency added by default.
- No real external service calls.
- No default live network behavior.
- No public API implementation status change from `contract_only` to done.

## Phase B Tool Surface

| Tool | Phase B target | v0.2.0 status |
| --- | --- | --- |
| `pdf.extract_figures` | Extract local figure assets and provenance metadata | planned contract-only until implemented |
| `pdf.extract_tables` | Extract local tables and serialize to markdown/csv-compatible records | planned contract-only until implemented |
| `pdf.sectionize` | Produce section tree and page-linked headings | planned contract-only until implemented |
| `pdf.to_markdown` | Carry quality v2 and page map compatibility | existing minimal implementation plus planned contract additions |

## Page Map v2

Phase B page map should preserve:

- page number
- markdown line start
- markdown line end
- source bounding boxes when available
- extraction confidence
- section id when available

The Phase A page map remains compatible. New fields should be optional until implementation is complete.

## Section Tree

Section tree should include:

- `section_id`
- title
- level
- page start
- page end
- parent section id
- child section ids
- evidence locator
- confidence

The section tree must not invent hierarchy when headings are uncertain. Low confidence headings should produce warnings.

## Figure Extraction Plan

Figure extraction should produce PDF assets with:

- stable asset id
- source PDF path hash
- page number
- output path
- bounding box when available
- caption text when available
- confidence
- warnings

Integration:

- `paper.figure_register` can register extracted figure assets.
- `vault.ingest_source` can ingest figure metadata as evidence/source pages.

## Table Extraction Plan

Table extraction should produce:

- stable table id
- source PDF path hash
- page number
- markdown table or structured rows
- optional CSV output path
- confidence
- warnings

Tables should be evidence-linked when used in survey, experiment, or paper workflows.

## Quality Score v2

Quality score v2 should separate:

- text extraction coverage
- section confidence
- page map completeness
- figure extraction confidence
- table extraction confidence
- warning severity
- empty page ratio
- cache status

The score should be transparent. Warnings should explain why confidence is low.

## Integration With Paper Pipeline

Planned path:

1. `pdf.extract_figures` creates figure asset metadata.
2. `paper.figure_register` validates figure id, caption status, source file, output files, and ArticleBlock links.
3. `paper.caption_generate` may draft captions only from available metadata and evidence.
4. `paper.docflow_status` blocks sections missing required figures.

## Integration With Vault

Planned path:

1. `pdf.to_markdown` or `pdf.sectionize` produces evidence locators.
2. `vault.ingest_source` creates source, evidence, claim, or topic pages as appropriate.
3. `vault.add_edge` connects claims to evidence with `supported_by` edges.

## Test Strategy

- Fixture PDFs must be tiny and local.
- Tests must not require real network access.
- Tests must not require private papers or restricted datasets.
- OCR tests remain future/manual.
- Converter-specific tests should use fake or minimal fixtures.
- Outputs must serialize to markdown and json-compatible data.

## Backlog Mapping

- BL-05: PDF figure extraction.
- BL-06: PDF table extraction.
- BL-07: PDF section tree and page map upgrade.
- BL-08: PDF quality report Phase B.

## Release Blockers For Phase B

- Extracted assets without provenance.
- Page map changes that break Phase A compatibility.
- Figure/table output that cannot serialize.
- Quality score that hides warnings.
- Any test requiring network or real API keys.
- Any OCR dependency added to the default path.
