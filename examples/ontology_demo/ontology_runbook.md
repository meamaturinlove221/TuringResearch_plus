# Ontology SOP Runbook Demo

Status: public-safe fake demo.

Graph id: `ontology-demo`.

## Runbook Status

- Status: `requires-human-review`
- Requires human review: `true`
- Final knowledge graph generated: `false`
- Network required: `false`

## SOP Steps

- `alias-resolution` -> review aliases and candidate merges
- `gap-detection` -> report missing source refs, low confidence, dangling edges
- `concept-page-creation` -> draft concept pages
- `edge-batch-creation` -> propose edges for review
- `ontology-export` -> export review artifact only

## Alias Resolution

| Alias | Candidate | Status |
| --- | --- | --- |
| `north star question` | `north-star` | candidate; requires human review |
| `research workflow catalog` | `research-catalog` | candidate; requires human review |
| `unknown term` | none | unresolved |

## Concept Pages

- `concepts/North Star.md`
- `concepts/Hypothesis.md`
- `concepts/Research Catalog.md`

## Edge Suggestions

- `north-star` belongs_to `research-catalog`
- `hypothesis` belongs_to `research-catalog`
- `research-catalog` requires `stress-test`

## Safety Boundary

- fake/demo only;
- review-only ontology output;
- no automatic alias merge;
- no Evidence Ledger mutation;
- no final knowledge graph.
