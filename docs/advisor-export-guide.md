# Advisor Export Guide

Status: v0.7 advisor export guide.

Advisor export starts from an `AdvisorMarkdownBundle`. Markdown is the primary
review source. PDF and PPTX export paths are optional and may skip gracefully if
the local backend is unavailable.

## Outputs

- Markdown bundle.
- PDF export plan and optional PDF.
- PPTX export plan and optional deck.
- Export quality report.

## Safety Boundary

- No fake figures.
- No fabricated result values.
- Planned work must stay planned.
- Limitations and human-review markers must remain visible.
- Optional backend failure must not fail default tests.

## Useful Docs

- [Advisor Export Plan](advisor-export-plan.md)
- [Advisor Markdown Bundle](advisor-markdown-bundle.md)
- [Advisor PDF/PPTX Export](advisor-pdf-pptx-export.md)
- [Real Advisor PDF Export](advisor-real-pdf-export.md)
- [Real Advisor PPTX Export](advisor-real-pptx-export.md)
- [Export Quality Gate](export-quality-gate.md)

## Validation

```powershell
python -m pytest tests/workflow/test_v0_7_dashboard_export_fake.py -q
```
