# Vault Edge Audit

Status: implemented minimal.

Round: 244.

The v1.2 vault edge audit layer reports graph quality issues that make wiki
navigation safer to inspect.

## Checks

- Dangling links: edges whose source or target node is missing.
- Missing edges: evidence-bearing edges without `source_refs`.
- Weak edges: edges below the confidence threshold.
- Requires-review nodes: nodes still marked for human review.
- Graph summary: node, edge, node type, and edge type counts.

## Release Boundary

Dangling links and missing evidence-bearing edges are release blockers for a
public claim graph. They are not automatically fixed because that would risk
inventing relationships.

Weak edges are not proof of failure. They are prompts for review.

## Non-goals

- No graph database.
- No automatic inference.
- No default network sync.
- No private vault ingestion.
- No automatic evidence ledger update.

## Example Use

```python
from turing_research_plus.vault_graph.edge_quality import evaluate_edge_quality

report = evaluate_edge_quality(graph)
assert report.requires_human_review
```
