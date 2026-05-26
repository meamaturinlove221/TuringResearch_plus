# TuringResearch Plus Feature Capsule: pdf_phase_b_figure_table_extraction

## Problem

PDF Markdown Phase A converts local PDFs to Markdown, but Sprint 1 needs a
planned Phase B slice for figure and table extraction with provenance so method
cards and advisor packs can reference paper assets safely.

## VGGT motivating example

The VGGT/SMPL-X dogfooding plan needs NeuralBody and HumanRAM method
understanding. Figure/table extraction can help build method-card inputs, but it
must not fabricate citations, captions, or paper claims.

## User story

As a TuringResearch Plus maintainer, I need local fixture-driven PDF figure and
table extraction that records page provenance and warnings for later paper and
vault ingestion.

## Inputs

- Local fixture PDFs.
- Existing PDF Markdown Phase A outputs.
- Optional extracted figure/table metadata.
- Paper figure registry expectations.

## Outputs

- `PDFAssetExtractionReport`
- Figure metadata list
- Table metadata list
- Page provenance map
- Warning list

## Data model

- `PDFAssetExtractionReport`
- `PDFFigureAsset`
- `PDFTableAsset`
- `PDFAssetProvenance`
- `PDFExtractionWarning`

## Proposed commands / tools

- command: `tuling pdf extract-assets`
- tools: `pdf.extract_figures`, `pdf.extract_tables`
- output: `PDFAssetExtractionReport`

The tool names already exist as contract-only PDF namespace entries. This
capsule plans the Sprint 1 implementation slice without changing public API.

## Related contracts

- `contracts/pdf_markdown.yaml`
- `contracts/paper_pipeline.yaml`
- `contracts/artifact_schema.yaml`

## Related skills

- `turingresearch-pdf-markdown-core`
- `turingresearch-paper-figure-asset-pipeline`
- `turingresearch-race-feature-capsule-factory`

## Required tests

- Local fixture PDF figure extraction.
- Local fixture PDF table extraction.
- Page provenance.
- Warning serialization.
- Method-card draft from figure/caption metadata without fabricated claims.

## Risks

- Misleading figure/table metadata.
- Unsupported scanned PDFs being treated as extracted.
- Captions fabricated from incomplete data.
- Breaking existing PDF Phase A outputs.

## Done criteria

- Extraction is local-only and fixture-driven by default.
- Each figure/table has source PDF and page provenance.
- Empty extraction emits warnings.
- Outputs align with paper figure registry and vault ingestion needs.

## Release target

v0.2.0 Sprint 1, fifth implementation slice.

Future Sync Adapters remain out of scope for this sprint. Handoff, NAS/SMB,
SSH/SFTP, GitHub sync, and cloud object storage must wait for later adapter
planning.
