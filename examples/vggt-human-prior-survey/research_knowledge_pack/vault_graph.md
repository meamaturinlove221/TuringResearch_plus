# Vault Graph

Status: review graph / requires human review.

## Graph Notes

The current vault graph is a lightweight review artifact. It uses nodes and
edges to connect papers, methods, claims, failures, routes, artifacts, and
concepts, but it is not a final knowledge graph.

## Example Edges

- [[NeuralBody]] -- `related_to` --> [[SparseConv3D]]
- [[HumanRAM]] -- `related_to` --> [[tri-plane]]
- [[SMPL-X]] -- `maps_to` --> [[feature adapter]]
- [[hard gate]] -- `blocks` --> [[promotion]]

## Missing Edges

- Evidence-backed edge from SparseConv3D route to observed success.
- Evidence-backed visual edge for full body, hairline, and hand close-ups.
- Citation-grade source refs for final related-work claims.
- Dataset and evaluation target edges for collision analysis.

## Wikilink Export

Inline `[[wikilink]]` labels are navigation aids. They are not evidence by
themselves and must not be treated as proof.

## Edge Audit Boundary

Evidence-bearing edges without source refs remain blocked. Low-confidence nodes
and requires-human-review nodes must stay visible in review outputs.
