# TuringResearch Plus Citation Graph Expansion

Status: v0.2 beta minimal implementation.

Round 57 adds a citation graph package that can build fake/manual graphs by
default and use the optional Semantic Scholar live adapter only when explicitly
enabled.

## Scope

The beta graph supports:

- fake VGGT-related work graph;
- manual seed lists;
- optional live Semantic Scholar retrieval path;
- depth limit;
- max node limit;
- year and open-access filters;
- duplicate node and edge merging;
- frontier report;
- JSON and Markdown export.

## VGGT Seed Topics

- VGGT
- SMPL-X
- NeuralBody
- HumanRAM
- HART
- VGGT-HPE
- HGGT
- Fus3D
- SparseConv3D
- human prior

## Model

`CitationGraph` contains:

- `graph_id`
- `seed_papers`
- `nodes`
- `edges`
- `frontier_nodes`
- `expansion_depth`
- `filters`
- `source_adapter`
- `retrieval_status`
- `limitations`
- `requires_human_review`

## Edge Types

- `cites`
- `cited_by`
- `related`
- `same_author`
- `recommended`
- `manual_related`

## Live Boundary

Default execution does not call the network. Live mode requires the Semantic
Scholar live adapter conditions from `docs/semantic-scholar-live-adapter.md`:

- request context must allow live mode;
- dry-run must be false;
- `SEMANTIC_SCHOLAR_API_KEY` must exist;
- live tests must set `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.

Live retrieval is not human verification. It must not be used as a final
related-work conclusion without human review and EvidenceRef discipline.

## Limitations

- No full text is downloaded.
- Citation expansion is not complete related work.
- Fake graph output is only a deterministic test fixture.
- Live graph output is retrieval metadata only.
- Collision-risk conclusions are out of scope for this round.
