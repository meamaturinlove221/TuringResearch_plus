# Ontology SOPs

Status: implemented minimal.

Ontology SOPs are repeatable review steps for maintaining concept pages,
aliases, graph edges, confidence labels, and ontology exports. They are not
automatic truth inference.

## Supported SOPs

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

## Rules

- Every SOP output requires human review.
- Evidence-free edges must not be promoted.
- Alias resolution must keep source refs and confidence.
- Ontology export is a review artifact, not a final knowledge graph.
