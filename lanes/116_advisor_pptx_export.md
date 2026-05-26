# Lane 116: Advisor PPTX Export

Round: 135

Status: implemented minimal / optional backend.

## Goal

Add a real Advisor PPTX export path from `AdvisorMarkdownBundle` while keeping
deck generation optional, review-only, and dependency-safe.

## Implemented

- `AdvisorRealPptxExportPlan`
- `AdvisorPptxSlide`
- `AdvisorPptxExportResult`
- optional `python-pptx` backend detection
- graceful skip when the backend is unavailable or intentionally skipped
- Markdown review source generation
- VGGT skipped fixture under `examples/vggt-human-prior-survey/advisor_export/pptx_export/`

## Deck Sections

1. Research North Star
2. Current Engineering State
3. Evidence Summary
4. Visual Readiness
5. Failure / Blockers
6. Related Work Position
7. Next Experiment Route
8. Advisor Ask / Decision Needed

## Boundaries

- No network access.
- No mandatory PPTX dependency.
- No fake charts, figures, screenshots, or visual evidence.
- No fabricated experiment values.
- No planned work written as observed evidence.
- Not-ready claims remain marked.
- No VGGT or Modal execution.
- No private VGGT path reads.
- Human review remains required.

## Validation

- `tests/unit/test_advisor_pptx_models.py`
- `tests/unit/test_advisor_pptx_export_plan.py`
- `tests/unit/test_advisor_pptx_template.py`
- `tests/workflow/test_advisor_pptx_export_optional.py`
