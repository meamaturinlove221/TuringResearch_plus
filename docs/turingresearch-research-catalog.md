# TuringResearch Research Catalog

Status: v1.2 integration.

Round: 248.

The TuringResearch Research Catalog is the integration view over the local-first
research workflow. It connects campaigns, skills, capabilities, vault graph,
ontology SOPs, stress tests, experiment runbooks, advisor packaging, and public
release gates.

It is a navigation and review catalog. It does not execute agents, run
experiments, call live services, or publish releases.

## Integrated Surfaces

| Surface | Role | Primary docs |
| --- | --- | --- |
| Campaigns | Choose the research workflow lane. | `docs/turingresearch-campaign-catalog.md` |
| Skills | Route work to human-reviewed SOPs. | `.agents/ENTRY.md` |
| Capabilities | Explain available local APIs and modules. | `docs/v1.1.0-feature-list.md` |
| Vault graph | Organize concept, claim, method, and artifact links. | `docs/yogsoth-vault-parity.md` |
| Ontology SOPs | Review aliases, gaps, hierarchy, and export steps. | `docs/yogsoth-ontology-parity.md` |
| Stress tests | Challenge claims, routes, plugins, privacy, and advisor output. | `docs/yogsoth-stress-test-parity.md` |
| Experiment runbooks | Prepare human-run experiment checklists and ingest contracts. | `docs/yogsoth-experiment-execution-parity.md` |
| Advisor pack | Package review material without final-paper claims. | `docs/advisor-pack-builder.md` |
| Public release | Gate README, demo, privacy, and release posture. | `docs/v1.0.0-public-launch-rc-report.md` |

## Catalog Flow

1. Start with `north_star` to define the review target.
2. Use `knowledge_acquisition` and `deep_insight` to gather source context.
3. Use vault graph and ontology SOPs to organize local knowledge.
4. Use `hypothesis_formation` and `experiment_planning` to draft route plans.
5. Use experiment execution runbooks to define artifact requirements.
6. Use stress tests before convergence or public release.
7. Use advisor pack and public release gates for human-facing output.

## Safety Boundary

- No automatic experiment execution.
- No multi-agent runtime.
- No default networking.
- No unknown plugin execution.
- No private data upload.
- No final paper automation.
- No fake/demo result promotion.
- No public release without human review.

## v1.2 Interpretation

This catalog completes conceptual integration for yogsoth-ai parity. It is not
a new runtime. It is a map for deciding which local review surface to use next.
