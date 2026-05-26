# Public Showcase

Status: v1.1 showcase draft.

Round: 220.

TuringResearch is a local-first Research OS for evidence-led research
workflows. It helps a reviewer inspect project intent, evidence state,
artifact status, paper scaffolds, route plans, dashboards, advisor packs, and
plugin boundaries without turning planned work into observed results.

## Project Pitch

Research projects often spread across notes, scripts, artifacts, papers,
dashboards, and informal claims. TuringResearch gives those surfaces a local,
review-first structure:

- evidence ledgers separate planned, fake/demo, missing, and reviewed states;
- artifact audits keep selected, missing, omitted, and unsafe files visible;
- paper workflow tools keep method notes and related-work claims reviewable;
- route plans stay separate from executed experiments;
- dashboards and advisor packs summarize state for humans;
- plugin and live adapter surfaces stay gated by safety policy.

## Architecture

The public showcase is organized around the main repository:

1. `README.md` explains the flagship project.
2. `docs/` holds source-of-truth documentation.
3. `examples/public_demo/` holds demo-only public fixtures.
4. `docs-site/` provides a local static documentation skeleton.
5. `src/turing_research_plus/dashboard_api/` exposes read-only dashboard data.
6. `src/turing_research_plus/local_server/` serves localhost-only summaries.
7. `split_ready/` holds export-ready bundles that are not published repos.

No cloud service is required for the showcase path.

## Public Demo

Start with:

- `docs/v1.0.0-public-demo-walkthrough.md`
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/SHOWCASE.md`
- `examples/public_demo/EXPECTED_OUTPUTS.md`

The demo is fake/demo only. It does not require API keys, VGGT data, restricted
model files, network access, or private local paths.

## VGGT Case Study

The VGGT case study is dogfooding material for the TuringResearch workflow. It
is not a VGGT experiment source repository and it does not claim SparseConv3D
success.

Relevant entry points:

- `docs/vggt-case-study-public.md`
- `split_ready/turingresearch-vggt-case/README.md`
- `split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md`

## Dashboard

The dashboard showcase has three local surfaces:

- static public demo dashboard files under `examples/public_demo/`;
- read-only Dashboard Data API summaries;
- localhost-only local server routes.

Useful docs:

- `docs/dashboard-data-api.md`
- `docs/local-server-dashboard.md`
- `docs/v1.1.0-docs-dashboard-integration-report.md`

## Paper Workflow

The paper workflow is designed for review, not automatic final paper writing.
It can expose method notes, related-work groups, collision-risk style review
state, missing evidence, and advisor next actions.

Public demo entry points:

- `examples/public_demo/demo_related_work.md`
- `examples/public_demo/demo_advisor_pack.md`
- `docs/v1.0.0-public-demo-walkthrough.md`

## Plugin System

Plugins are policy-gated. Unknown third-party plugins are not executed by
default, plugin permissions must be explicit, and plugin proposals require
human review.

Useful docs:

- `docs/plugin-guide.md`
- `docs/plugin-sandbox-policy.md`
- `docs/plugin-review-policy.md`

## Privacy And Safety

The showcase excludes private data and credentials. Public demo artifacts are
demo-only fixtures, not private research payloads.

Safety principles:

- no API keys in examples;
- no raw private data;
- no private local paths;
- no restricted model files;
- no unsupported experiment claims;
- no fake/demo output presented as observed evidence.

## Limitations

- No SaaS or cloud user system.
- Live adapters are optional and disabled by default.
- Unknown plugins are disabled by default.
- The local server dashboard is localhost-only and read-only.
- Split-ready bundles are local export bundles, not published child repos.
- The project does not automate research completion.
- The project does not write final papers automatically.

## Roadmap

The v1.1 showcase path focuses on:

1. main repo stabilization;
2. split-ready case/example bundles;
3. local docs site;
4. local server dashboard;
5. public demo expansion;
6. release and CI hardening.
