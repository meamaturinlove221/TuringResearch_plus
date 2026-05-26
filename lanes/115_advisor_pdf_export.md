# Lane 115: Advisor PDF Export

Round: 134

Status: implemented minimal / optional backend.

## Goal

Add a real Advisor PDF export path from `AdvisorMarkdownBundle` while keeping
PDF generation optional and review-only.

## Implemented

- `AdvisorRealPdfExportPlan`
- `AdvisorPdfExportResult`
- optional `reportlab` backend detection
- graceful skip when the backend is unavailable or intentionally skipped
- Markdown review source generation
- VGGT skipped fixture under `examples/vggt-human-prior-survey/advisor_export/pdf_export/`

## Boundaries

- No network access.
- No mandatory PDF dependency.
- No fake charts, figures, or visual evidence.
- No planned work written as observed evidence.
- No VGGT or Modal execution.
- No private VGGT path reads.
- Human review remains required.

## Validation

- `tests/unit/test_advisor_pdf_models.py`
- `tests/unit/test_advisor_pdf_export_plan.py`
- `tests/unit/test_advisor_pdf_template.py`
- `tests/workflow/test_advisor_pdf_export_optional.py`
