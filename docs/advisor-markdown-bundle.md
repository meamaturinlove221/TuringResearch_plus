# Advisor Markdown Bundle

Status: v0.4 minimal implementation.

The Advisor Markdown Bundle is a source package for future PDF, PPTX, DOCX, and
HTML exports. It is not itself a PDF or PPTX export.

## Inputs

- Existing VGGT advisor pack Markdown files.
- Existing VGGT research knowledge pack Markdown files.

Missing inputs should be recorded in source sections rather than causing a
binary export to be fabricated.

## Output Files

- `README.md`
- `advisor_report_source.md`
- `slides_outline.md`
- `figure_list.md`
- `table_list.md`
- `evidence_refs.md`
- `limitations.md`
- `next_actions.md`
- `manifest.yaml`

## Boundary

The bundle does not run VGGT, does not run Modal, does not generate figures,
does not generate tables, and does not convert Markdown into binary documents.
It exists so a later export phase can work from auditable source material.
