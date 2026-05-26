# Advisor PDF / PPTX Export

Status: v0.5 minimal plan-only implementation.

Round 93 adds the Advisor PDF / PPTX export planning layer. It does not create
real PDF or PPTX files. It produces auditable Markdown plans and a manifest that
future optional adapters can consume.

## Outputs

- `advisor_pdf_export_plan.md`
- `advisor_pptx_outline.md`
- `export_manifest.yaml`
- `slide_section_mapping.md`

## Current Implementation

The implementation builds:

- `AdvisorPdfExportPlan`
- `AdvisorPptxExportPlan`
- `AdvisorPptxSlidePlan`
- `AdvisorExportManifest`

The export manifest always records:

- `generated_binary_exports: false`
- `external_converter_called: false`
- `requires_human_review: true`

## Template Policy

Templates live under `src/turing_research_plus/advisor_export/templates/`.
They are text scaffolds only. They do not call office tools, browser engines,
PDF renderers, or slide generators.

## Safety Requirements

- Do not generate real PPTX by default.
- Do not generate real PDF by default.
- Do not call external office tools.
- Do not fabricate figures, tables, charts, or result slides.
- Do not write planned work as observed evidence.
- Do not claim SparseConv3D success without evidence ledger support.
- Preserve limitations and human-review markers in every planned output.

## VGGT Boundary

The VGGT fixture under `examples/vggt-human-prior-survey/advisor_export/export_plan/`
is an export plan only. It keeps Modal / VGGT execution, SparseConv3D success,
and paper conclusions outside the export layer.

## Future Optional Adapters

Future adapters may generate PDF or PPTX files, but they must be opt-in,
tested separately, and preserve this manifest boundary. Default tests must not
require those adapters.
