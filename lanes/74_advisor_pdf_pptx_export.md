# Lane 74 - Advisor PDF / PPTX Export

Status: implemented minimal.

Round: 93.

## Scope

Implemented a plan-only Advisor PDF / PPTX export layer on top of the existing
Advisor Markdown Bundle.

## Added

- `src/turing_research_plus/advisor_export/pdf_plan.py`
- `src/turing_research_plus/advisor_export/pptx_plan.py`
- `src/turing_research_plus/advisor_export/export_manifest.py`
- `src/turing_research_plus/advisor_export/templates/`
- `docs/advisor-pdf-pptx-export.md`
- `examples/vggt-human-prior-survey/advisor_export/export_plan/`
- Advisor PDF / PPTX plan unit and workflow tests

## Outputs

- `advisor_pdf_export_plan.md`
- `advisor_pptx_outline.md`
- `export_manifest.yaml`
- `slide_section_mapping.md`

## Boundaries

- No real PDF generation.
- No real PPTX generation.
- No external office tool calls.
- No fabricated figures, tables, charts, or result slides.
- No planned-as-observed promotion.
- No private VGGT path read.
- No network access.
- Human review required before advisor delivery.
