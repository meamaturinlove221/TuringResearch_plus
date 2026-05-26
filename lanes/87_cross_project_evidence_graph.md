# Lane 87 - Cross-project Evidence Graph

Status: implemented minimal.

## Scope

Round 106 implements a local cross-project evidence graph for comparing multiple
research projects in a workspace.

## Added

- `src/turing_research_plus/cross_project/`
- `contracts/cross_project_evidence_graph.yaml`
- `docs/cross-project-evidence-graph.md`
- demo workspace graph JSON and Markdown summary
- unit and workflow tests

## Supported Output

- project nodes
- claim nodes
- artifact nodes
- method nodes
- failure nodes
- route nodes
- cross-project edges
- shared methods
- shared failures
- reusable template hints
- missing evidence claims

## Boundaries

- No graph database.
- No network access.
- No private project reads.
- No automatic evidence promotion.
- No evidence transfer between projects.
- Shared patterns are review hints only.
- Human review is required.
