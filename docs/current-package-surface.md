# TuringResearch Plus Current Package Surface

## Canonical Packages

- `turing_research`
- `turing_research.pdf`
- `turing_research_plus`

## Round 38 Sprint 1 Packages

- `turing_research_plus.vggt`
- `turing_research_plus.artifact_audit`

## VGGT Evidence Modules

- `turing_research_plus.vggt.evidence_models`
- `turing_research_plus.vggt.evidence_ledger`
- `turing_research_plus.vggt.edge_audit`
- `turing_research_plus.vggt.markdown_export`
- `turing_research_plus.vggt.tools`

`edge_audit` and `markdown_export` are minimal post-rename surface modules.
They operate only on existing evidence-ledger data and do not read VGGT local
paths.

## Artifact Audit Modules

- `turing_research_plus.artifact_audit.models`
- `turing_research_plus.artifact_audit.auditor`
- `turing_research_plus.artifact_audit.npz_summary`
- `turing_research_plus.artifact_audit.manifest`
- `turing_research_plus.artifact_audit.tools`

The Artifact Auditor remains a local manifest/index auditor. It does not
implement Visual Evidence Auditor or Advisor Pack Builder behavior.

## Round 40 Advisor Modules

- `turing_research_plus.advisor`
- `turing_research_plus.advisor.models`
- `turing_research_plus.advisor.pack_builder`
- `turing_research_plus.advisor.sections`
- `turing_research_plus.advisor.templates`
- `turing_research_plus.advisor.tools`

Advisor Pack Builder writes Markdown-only VGGT / SMPL-X status packs and does
not generate PPTX or PDF.

## Round 41 PDF Phase B Modules

- `turing_research.pdf.asset_report`
- `turing_research.pdf.extractors.figure_extractor`
- `turing_research.pdf.extractors.table_extractor`
- `turing_research.pdf.extractors.page_map`
- `turing_research.pdf.extractors.section_tree`
- `turing_research_plus.paper.pdf_asset_import`

PDF Phase B extends the existing Core PDF package at `src/turing_research/pdf/`.
It does not create a separate Plus PDF package and does not implement OCR,
MinerU, Marker, or complex layout parsing.
