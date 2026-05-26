# Advisor Export Plan

Status: v0.4 planning + Markdown bundle minimal implementation.

Round 88 prepares future Advisor Pack export formats without generating binary
files. The current implementation produces Markdown source material and an
export plan only.

## Future Formats

- PDF export
- PPTX export
- DOCX export
- HTML export

## Current Implementation

The current implementation builds an `AdvisorMarkdownBundle` containing:

- `advisor_report_source.md`
- `slides_outline.md`
- `figure_list.md`
- `table_list.md`
- `evidence_refs.md`
- `limitations.md`
- `next_actions.md`
- `manifest.yaml`

## Safety Requirements

- No real PPTX generation.
- No real PDF generation.
- No external converter calls.
- No fabricated figures or tables.
- Planned work must remain planned.
- SparseConv3D success must remain unclaimed without evidence ledger support.
- Every export target must preserve limitations and human-review markers.

## Non-Goals

- No binary export in Round 88.
- No chart generation.
- No image generation.
- No final paper prose.
- No advisor claim beyond existing evidence.
