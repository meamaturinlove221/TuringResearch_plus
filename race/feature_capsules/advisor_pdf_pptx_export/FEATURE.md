# Advisor PDF / PPTX Export

Status: scope_locked.

## Problem

Advisor communication needs portable PDF/PPTX outputs, but formatted documents can hide evidence caveats.

## VGGT motivating example

VGGT advisor summaries need a clean PDF or deck while preserving V260 hard-blocked, visual readiness blocked, and SparseConv3D not proven.

## User story

As a TuringResearch operator, I want this capability to turn existing review artifacts into safer, clearer project workflows without weakening evidence boundaries.

## Inputs

- Existing Markdown and JSON review artifacts.
- v0.4 remote artifact, dashboard, paper digest, or advisor export outputs.
- Project manifests and source refs.
- Manual review notes when needed.

## Outputs

- AdvisorPdfExportPlan.
- AdvisorPptxExportPlan.
- AdvisorExportManifest.
- `advisor_pdf_export_plan.md`.
- `advisor_pptx_outline.md`.
- `export_manifest.yaml`.
- `slide_section_mapping.md`.
- JSON-serializable report.
- Markdown review summary.
- Required human-review flags.

## Data model

- status: planned / generated / blocked / requires-human-review.
- source refs and sha256 metadata where applicable.
- limitations, omitted items, and safety warnings.
- no verified result unless evidence explicitly supports it.

## Proposed commands / tools

- command: `turing advisor pdf-plan`
- command: `turing advisor pptx-plan`
- command: `turing advisor export-manifest`
- tool: `advisor.pdf_export_plan`
- tool: `advisor.pptx_export_plan`
- tool: `advisor.export_manifest_build`
- output: `AdvisorExportManifest`

## Related contracts

- contracts/advisor_export.yaml

## Related skills

- `turingresearch-master-orchestrator`

## Required tests

- Fake/default workflow test.
- JSON serialization test.
- Markdown export test.
- Evidence-boundary regression test.
- No secret/raw-data/SMPL-X model packaging test.

## Risks

Binary exports may look like final claims if limitations are not carried into every output.

## Done criteria

PDF/PPTX export path from Markdown bundle, limitation-preserving templates, no fabricated figures, fixture tests.

## Release target

v0.5

## Non-goals

- No complex SaaS.
- No user system.
- No cloud deployment.
- No automatic paper writing.
- No unauthorized data upload.
- No legacy project naming.
