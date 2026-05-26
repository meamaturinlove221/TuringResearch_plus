# Cross-project Evidence Graph



Status: feature capsule draft.



Release target: v0.6 Sprint 1.



## 1. Problem



Researchers need to see reusable patterns across projects without transferring proof from one project to another.



## 2. VGGT / Research Motivating Example



VGGT and another geometry project may share failure types or route structures, but VGGT evidence must not become evidence for the other project.



## 3. Upstream / Internal Inspiration



Vault Graph Enhancement and Round 102 multi-project planning.



## 4. User Story



As a researcher, I want a graph that highlights shared methods, failures, artifacts, and reusable templates across projects.



## 5. Inputs



- workspace registry

- project evidence ledgers

- vault graphs

- failure taxonomies

- route summaries



## 6. Outputs



- CrossProjectEvidenceGraph

- CrossProjectComparison

- Markdown graph summary



## 7. Data Model



CrossProjectEvidenceGraph, CrossProjectNode, CrossProjectEdge



## 8. Proposed Commands / Tools



- command: `turing workspace graph`; tool: `workspace.cross_project_graph`; output: `CrossProjectEvidenceGraph`



## 9. Related Contracts



- cross_project_evidence_graph.yaml

- vault_graph.yaml



## 10. Related Skills



- turingresearch-fusion-wiki-vault

- turingresearch-master-orchestrator



## 11. Required Tests



- cross-project graph tests

- comparator tests

- Markdown export tests

- fake workspace workflow



## 12. Risks



- proof transfer

- private project leakage

- low-confidence graph treated as final truth



## 13. Done Criteria



- graph exports JSON and Markdown

- shared patterns are review-required

- unsupported claims are listed



## 14. Release Target



v0.6 Sprint 1



## 15. Non-goals



- no graph database

- no automatic evidence promotion

- no private project scan
