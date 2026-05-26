# TuringResearch Campaign Catalog

Status: implemented minimal.

Round: 176 upstream adjustment.

The Campaign Catalog is a static, review-only strategy book for routing common
research-workflow tasks to TuringResearch campaigns and skills. It is inspired
by upstream campaign routing and precondition patterns, but it does not copy
upstream code.

## Boundary

- It does not execute skills.
- It does not call an LLM.
- It does not start an MCP server.
- It does not use the network.
- It does not replace `turingresearch-master-orchestrator`.
- It does not convert planned work into observed evidence.

## Campaigns

| Campaign | Purpose | Primary skill |
| --- | --- | --- |
| `north_star` | Clarify research goal, scope, and non-goals. | `turingresearch-fusion-north-star` |
| `knowledge_acquisition` | Collect papers, source material, and context with source hygiene. | `turingresearch-fusion-literature-survey` |
| `deep_insight` | Produce reviewable gap and uncertainty notes. | `turingresearch-fusion-deep-insight` |
| `hypothesis_formation` | Shape hypotheses and falsifiability checks. | `turingresearch-fusion-hypothesis-formation` |
| `creative_ideation` | Generate bounded candidate ideas. | `turingresearch-fusion-creative-ideation` |
| `convergence` | Rank options and converge on feasible decisions. | `turingresearch-fusion-convergence` |
| `stress_test` | Stress-test claims, plans, and release posture. | `turingresearch-fusion-stress-test` |
| `experiment_planning` | Plan routes, hard gates, and metrics. | `turingresearch-fusion-experiment-execution` |
| `artifact_audit` | Audit artifacts and export readiness. | `turingresearch-cache-and-ledger` |
| `advisor_pack` | Package advisor review material. | `turingresearch-paper-writing-pipeline` |
| `public_release` | Prepare public release gates and go/no-go reports. | `turingresearch-qa-release` |

## Local API

- `list_campaigns()`
- `get_campaign(campaign_id)`
- `route_campaign(task_description)`
- `render_campaign_catalog_markdown()`

These are local Python surfaces, not public MCP tools.

## Upstream Inspiration

The catalog absorbs the idea of campaign routing, preconditions, and strategy
book structure. It intentionally keeps execution outside the catalog.

## Release Use

For v1.0, the catalog is useful for documentation, interview explanation,
skill routing, and public release clarity. It is not a complex agent runtime.
