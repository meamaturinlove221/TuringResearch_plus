# Ontology SOP Runbook

Status: implemented minimal.

Round: 245.

The ontology SOP runbook packages supported ontology SOP steps into a local,
deterministic review plan. It is meant for handoff and inspection, not for
automatic knowledge graph publication.

## Inputs

- A `VaultGraph`.
- Optional SOP names.
- Optional aliases to resolve.

## Outputs

- SOP step results.
- Proposed review outputs.
- Alias resolution report.
- Ontology gap report.
- Human-review flags.

## Default SOP Flow

When no subset is provided, the runner uses the existing ontology SOP list:

1. seed-concept-search
2. source-gathering
3. concept-page-creation
4. alias-resolution
5. edge-batch-creation
6. hierarchy-visualization
7. gap-detection
8. merge-candidates
9. confidence-update
10. ontology-export

## Review Rules

- Missing source references are blockers until reviewed.
- Dangling edges must be corrected or explicitly deferred.
- Aliases are candidates, not automatic merges.
- Low-confidence nodes remain visible.
- Ontology export is a review artifact, not final truth.

## Example

```python
from turing_research_plus.vault_graph.ontology_sop_runner import run_ontology_sop_plan

plan = run_ontology_sop_plan(graph, aliases=["north star question"])
assert plan.requires_human_review
assert not plan.final_knowledge_graph_generated
```
