# Advisor Real PDF Export

Status: v0.7 minimal optional implementation.

Round 134 adds a real Advisor PDF export path for `AdvisorMarkdownBundle`.
The path is optional: if the local PDF backend is unavailable, it returns a
skipped result with a reason and writes an auditable Markdown review source.
Default tests do not require PDF dependencies.

## Inputs

- `AdvisorMarkdownBundle`
- Existing Markdown bundle files:
  - `advisor_report_source.md`
  - `evidence_refs.md`
  - `figure_list.md`
  - `table_list.md`
  - `limitations.md`
  - `next_actions.md`
  - `manifest.yaml`

## Outputs

- `AdvisorRealPdfExportPlan`
- `AdvisorPdfExportResult`
- `advisor_pdf_review_source.md`
- optional `advisor_report.pdf` when the backend is installed

The committed VGGT fixture intentionally uses the skipped path:

- `examples/vggt-human-prior-survey/advisor_export/pdf_export/pdf_export_plan.yaml`
- `examples/vggt-human-prior-survey/advisor_export/pdf_export/pdf_export_report.md`
- `examples/vggt-human-prior-survey/advisor_export/pdf_export/advisor_pdf_review_source.md`

## Required PDF Sections

- title
- current status
- evidence summary
- artifact readiness
- visual readiness
- failure summary
- next actions
- limitations
- requires human review

## Backend Policy

The current optional backend is `reportlab`. It is not a default dependency.
When unavailable, `export_advisor_pdf_optional` returns `status=skipped` and
does not fail default tests.

## Safety Boundary

- No network access.
- No automatic file opening.
- No fake figures or visual evidence.
- No synthetic result tables.
- No planned work written as observed evidence.
- No VGGT or Modal execution.
- No private VGGT path reads.
- Human review remains required before advisor delivery.

## Non-goals

- No mandatory heavy PDF dependency.
- No cloud converter.
- No office automation.
- No final paper writing.
- No advisor claim beyond existing evidence.
