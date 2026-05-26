# TuringResearch Plus Paper-to-Method Card

Status: implemented minimal for v0.2 Sprint 2.

Paper-to-Method Card converts local notes, PDF markdown, or HTML summaries into
structured method cards. It is a local, conservative extraction layer. It does
not download papers, call live APIs, run OCR, copy long paper text, fabricate
citations, or claim that related work has been completed.

## Core Models

- `PaperMethodCard`
- `PaperMethodCardInput`
- `VGGTMethodMapping`

## Method Card Fields

- `paper_id`
- `title`
- `source_type`
- `task`
- `inputs`
- `outputs`
- `representation`
- `core_method`
- `architecture_components`
- `training_objective`
- `inference_pipeline`
- `key_figures`
- `key_tables`
- `what_to_borrow`
- `what_not_to_copy`
- `collision_risk`
- `mapping_to_vggt`
- `evidence_refs`
- `limitations`
- `requires_human_review`

## VGGT Mapping

The VGGT mapping records:

- SMPL / SMPL-X role
- voxel / sparseconv relevance
- tri-plane relevance
- token alignment relevance
- geometry output relevance
- difference from VGGT objective
- potential collision risk

## Fixtures

- `examples/vggt-human-prior-survey/paper_method_cards/neuralbody.fixture.md`
- `examples/vggt-human-prior-survey/paper_method_cards/humanram.fixture.md`

Both fixtures are explicitly `fake-or-manual-note` and
`requires-real-paper-review`. They are test samples only and do not claim
complete paper reading.

## Tool Boundary

Proposed capsule-local tool:

- command: `turing paper method-card`
- tool: `paper.method_card_extract`
- output: `PaperMethodCard`

This is not a frozen public MCP API until root contracts and `docs/mcp-tools.md`
accept it.
