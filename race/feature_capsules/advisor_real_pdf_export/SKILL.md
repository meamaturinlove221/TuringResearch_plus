# Advisor Real PDF Export Skill

Status: planning skill draft.

Use this skill for optional advisor PDF export planning. It keeps Markdown
source authoritative and does not fabricate figures or results.

## Inputs

- AdvisorMarkdownBundle
- export manifest
- figure list
- evidence refs
- limitations

## Outputs

- AdvisorPDFExportPlan
- AdvisorPDFArtifactManifest
- PDFExportSafetyReport

## Safety Rules

- Do not generate binary PDF by default.
- Do not call external converters by default.
- Do not invent figures, tables, or result values.
- Require human review.

## Related Contracts

- advisor_real_pdf_export.yaml
- advisor_export.yaml
