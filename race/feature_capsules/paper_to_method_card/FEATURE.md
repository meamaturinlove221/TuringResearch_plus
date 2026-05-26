# TuringResearch Plus Feature Capsule: paper_to_method_card

## Problem

VGGT dogfooding needs to understand NeuralBody, HumanRAM, HART, and related
methods without turning incomplete PDF or note inputs into unsupported method
claims.

## VGGT motivating example

The SMPL-X feature encoding route depends on knowing which prior methods use
canonical features, raster features, tri-planes, sparse voxels, or latent
representations. Those facts must come from provenance-backed paper inputs, not
memory or guesswork.

## User story

As a TuringResearch Plus maintainer, I need to extract a paper's method into a
structured Method Card with evidence refs, limitations, and missing-input
markers.

## Inputs

- Local paper metadata.
- PDF Phase B asset reports.
- Literature survey artifacts.
- EvidenceRefs.
- Failure Taxonomy labels.
- Hard Gate results.

## Outputs

- `PaperMethodCard`
- method component list
- architecture cue list
- evidence-backed limitations
- missing paper / missing figure report

## Data model

- `PaperMethodCard`
- `MethodComponent`
- `MethodEvidenceRef`
- `MethodLimitation`
- `MethodArchitectureCue`

## Proposed commands / tools

- command: `turing paper method-card`
- tool: `paper.method_card_extract`
- output: `PaperMethodCard`

This is a capsule-local proposal and is not a frozen public MCP API until a
contracts-first round updates root contracts and `docs/mcp-tools.md`.

## Related contracts

- `contracts/method_cards.yaml`
- `contracts/pdf_markdown.yaml`
- `contracts/paper_pipeline.yaml`
- `contracts/hard_gates.yaml`

## Related skills

- `turingresearch-paper-writing-pipeline`
- `turingresearch-pdf-markdown-core`
- `turingresearch-fusion-literature-survey`

## Required tests

- Method card validates with paper metadata and EvidenceRef fields.
- Missing real paper input returns `requires-real-paper`.
- Missing figure input returns `requires-human-review`.
- Method card does not fabricate method components.
- PDF Phase B asset report can be referenced without copying copyrighted PDF
  content.

## Risks

- Overstating paper claims.
- Treating extracted figures as interpreted architecture.
- Copying too much copyrighted text.
- Blocking on incomplete PDF extraction.

## Done criteria

- Method cards serialize to JSON and Markdown.
- Every major method claim has EvidenceRef.
- Missing inputs become explicit status outputs.
- Figure-to-Architecture can consume method cards.

## Release target

v0.2.0 Sprint 2.

## Upstream learning note

`docs/upstream-learning-report.md` is missing in the current checkout. This
capsule follows the local learning policy: reuse architecture and test ideas,
not incompatible source code or unsupported paper claims.

## Relation to Sprint 1 modules

- Uses PDF Phase B page maps, section trees, figures, and tables.
- Uses Evidence Ledger status language for provenance.
- Can feed Advisor Pack Builder with method summaries.
- Does not replace Literature Survey or Paper Draft Gate.
