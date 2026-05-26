# Advisor Real PDF Export

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Advisor export currently produces Markdown/source plans. v0.7 may add an
optional PDF adapter while preserving source-bundle and evidence boundaries.

## 2. Research Motivating Example

A researcher may need a PDF advisor brief from a reviewed Markdown bundle, but
the PDF must not invent figures, tables, or claims.

## 3. Inputs

- AdvisorMarkdownBundle
- export manifest
- figure list
- evidence refs
- limitations

## 4. Outputs

- AdvisorPDFExportPlan
- AdvisorPDFArtifactManifest
- PDFExportSafetyReport

## 5. Proposed Commands / Tools

- command: `turing advisor export-pdf`
- tool: `advisor.export_pdf_optional`
- output: `AdvisorPDFArtifactManifest`

## 6. Related Contracts

- advisor_real_pdf_export.yaml
- advisor_export.yaml

## 7. Related Skills

- turingresearch-paper-writing-pipeline
- turingresearch-qa-release

## 8. Required Tests

- optional adapter tests
- no external converter by default tests
- artifact manifest tests

## 9. Risks

- binary export implies finality
- external converter dependency risk
- fabricated figures or tables

## 10. Done Criteria

- PDF export is optional
- source Markdown remains authoritative
- no fake chart/result generation

## 11. Non-goals

- no default binary generation
- no office/cloud converter call by default
- no final paper generation
