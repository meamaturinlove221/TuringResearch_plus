# Research Catalog Dashboard

Status: v1.3 public-safe dashboard.

Round: 278.

This dashboard shows how the TuringResearch Research Catalog connects
campaigns, skills, vault graph, stress tests, experiment runbooks, advisor
review, and public release gates.

Data source:

- `examples/research_catalog/dashboard.json`

## Dashboard Groups

| Group | Role | Primary docs |
| --- | --- | --- |
| Campaigns | Route the next research workflow decision. | `docs/turingresearch-campaign-catalog.md` |
| Skills | Provide SOP handoff targets for each route. | `docs/research-catalog-skill-map.md` |
| Vault / Ontology | Organize concepts, aliases, edges, gaps, and wiki views. | `docs/yogsoth-vault-parity.md`, `docs/yogsoth-ontology-parity.md` |
| Stress | Challenge claims, routes, plugin posture, privacy, and advisor output. | `docs/yogsoth-stress-test-parity.md` |
| Experiment Runbooks | Prepare human-run experiment plans and artifact requirements. | `docs/yogsoth-experiment-execution-parity.md` |
| Advisor / Release | Package review material and gate public release posture. | `docs/advisor-pack-builder.md`, `docs/v1.0.0-public-launch-rc-report.md` |

## Relationship Map

1. Campaign routing chooses a review path.
2. Skill map identifies the human-reviewed SOP.
3. Vault and ontology organize knowledge before claims harden.
4. Stress tests challenge weak routes and unsupported claims.
5. Experiment runbooks prepare artifact requirements without running the
   experiment.
6. Advisor and release gates package output for human review.

## Safety Boundary

- dashboard only;
- no agent runtime;
- no automatic tool execution;
- no default network;
- no experiment execution;
- no Evidence Ledger mutation;
- no fake/demo result promotion;
- human review required.

## Interpretation

This dashboard is a navigation surface. It makes the Research Catalog easier to
show and test, but it does not execute the catalog.
