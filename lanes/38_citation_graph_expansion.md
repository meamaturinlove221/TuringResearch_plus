# Lane 38: Citation Graph Expansion

Status: beta minimal implementation.

## Scope

Round 57 implements citation graph expansion with fake/manual defaults and an
optional live Semantic Scholar path.

## Implemented

- `src/turing_research_plus/citation_graph/`
- `contracts/citation_graph.yaml`
- `docs/citation-graph-expansion.md`
- VGGT fake related-work graph example
- frontier report example
- default-skipped live test

## Boundaries

- Default execution is offline.
- Live mode requires explicit opt-in.
- No full-text download.
- No collision conclusion.
- No claim that citation graph is complete related work.
- Live results are retrieved, not human-verified.

## Validation

- Citation graph focused unit and workflow tests: passed.
- Optional live citation graph test: skipped without explicit opt-in.
- Contract tests: passed.
- Package import / public import / name integrity checks: passed.
- Full pytest: passed with live tests deselected by default.
- `python -m mypy src`: passed.
- Focused ruff check: passed.
