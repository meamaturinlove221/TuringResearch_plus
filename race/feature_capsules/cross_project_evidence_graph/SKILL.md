# Cross-project Evidence Graph Skill



Status: planning skill draft.



Use this skill when a task is about `cross_project_evidence_graph` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Cross-project Evidence Graph` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- workspace registry

- project evidence ledgers

- vault graphs

- failure taxonomies

- route summaries



## Outputs



- CrossProjectEvidenceGraph

- CrossProjectComparison

- Markdown graph summary



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- cross_project_evidence_graph.yaml

- vault_graph.yaml
