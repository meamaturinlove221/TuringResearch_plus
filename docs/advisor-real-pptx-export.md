# Advisor Real PPTX Export

Status: v0.7 minimal optional implementation.

Round 135 adds a real Advisor PPTX export path for `AdvisorMarkdownBundle`.
The path is optional: if the local PPTX backend is unavailable, it returns a
skipped result with a reason and writes an auditable Markdown review source.
Default tests do not require PPTX dependencies.

## Inputs

- `AdvisorMarkdownBundle`
- `slides_outline.md`
- `advisor_report_source.md`
- `evidence_refs.md`
- `figure_list.md`
- `limitations.md`
- `next_actions.md`

## Outputs

- `AdvisorRealPptxExportPlan`
- `AdvisorPptxExportResult`
- `advisor_pptx_review_source.md`
- optional `advisor_deck.pptx` when the backend is installed

The committed VGGT fixture intentionally uses the skipped path:

- `examples/vggt-human-prior-survey/advisor_export/pptx_export/pptx_export_plan.yaml`
- `examples/vggt-human-prior-survey/advisor_export/pptx_export/pptx_export_report.md`
- `examples/vggt-human-prior-survey/advisor_export/pptx_export/advisor_pptx_review_source.md`

## Deck Sections

1. Research North Star
2. Current Engineering State
3. Evidence Summary
4. Visual Readiness
5. Failure / Blockers
6. Related Work Position
7. Next Experiment Route
8. Advisor Ask / Decision Needed

## Backend Policy

The current optional backend is `python-pptx`. It is not a default dependency.
When unavailable, `export_advisor_pptx_optional` returns `status=skipped` and
does not fail default tests.

## Safety Boundary

- No network access.
- No fake charts, figures, screenshots, or visual evidence.
- No synthetic experiment values.
- Not-ready claims remain explicitly marked.
- Planned experiments remain planned.
- No VGGT or Modal execution.
- No private VGGT path reads.
- Human review remains required before advisor delivery.

## Non-goals

- No mandatory heavy PPTX dependency.
- No cloud converter.
- No office automation.
- No final presentation claims.
- No advisor claim beyond existing evidence.
