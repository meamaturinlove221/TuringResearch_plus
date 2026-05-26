# TuringResearch Plus Feature Capsule: figure_to_architecture

## Problem

Architecture diagrams are useful for explaining paper methods and VGGT routes,
but diagram drafts can easily imply unsupported implementation details if they
are generated without method-card and figure provenance.

## VGGT motivating example

SMPL-X feature encoding needs diagrams that distinguish canonical features,
raster features, tri-planes, sparse voxels, and sparse latent routes. Those
diagrams should be labeled as drafts unless supported by Method Cards, extracted
figures, and route evidence.

## User story

As a TuringResearch Plus maintainer, I need to map method cards and extracted
figures into architecture diagram specs that preserve provenance and mark
unsupported edges.

## Inputs

- `PaperMethodCard`
- PDF Phase B figure/table extraction reports.
- Figure registry entries.
- Experiment Route DSL specs.
- Hard Gate validation reports.

## Outputs

- `ArchitectureDiagramSpec`
- Mermaid graph draft
- Graphviz export plan
- figure-to-component map
- unsupported-edge warnings

## Data model

- `ArchitectureDiagramSpec`
- `ArchitectureNode`
- `ArchitectureEdge`
- `FigureComponentMapping`
- `UnsupportedArchitectureClaim`

## Proposed commands / tools

- command: `turing figure arch`
- tool: `paper.figure_to_architecture`
- output: `ArchitectureDiagramSpec`

This is a capsule-local proposal and is not a frozen public MCP API until a
contracts-first round updates root contracts and `docs/mcp-tools.md`.

## Related contracts

- `contracts/figure_architecture.yaml`
- `contracts/method_cards.yaml`
- `contracts/paper_pipeline.yaml`
- `contracts/pdf_markdown.yaml`

## Related skills

- `turingresearch-paper-figure-asset-pipeline`
- `turingresearch-paper-sop-graph-generator`
- `turingresearch-paper-writing-pipeline`

## Required tests

- Architecture draft validates from a minimal Method Card fixture.
- Mermaid export contains nodes and edges.
- Unsupported edges are reported as warnings.
- Figure provenance is preserved.
- Output is labeled draft unless all required evidence is present.

## Risks

- Fabricating architecture edges.
- Treating source figures as interpreted method proof.
- Creating polished diagrams without sufficient evidence.

## Done criteria

- Diagram specs serialize to JSON and Markdown.
- Mermaid output is valid text.
- Unsupported edges remain explicit.
- Figure and Method Card provenance are preserved.

## Release target

v0.2.0 Sprint 2.

## Upstream learning note

`docs/upstream-learning-report.md` is missing in the current checkout. This
capsule follows the internal SOP graph discipline: generate traceable drafts,
not unsupported finished diagrams.

## Relation to Sprint 1 modules

- Uses PDF Phase B extracted figures and tables.
- Uses paper figure registry entries.
- Uses Advisor Pack summaries only as context, not evidence.
- Depends on Paper-to-Method Card for method semantics.
