# Dashboard Refinement

Status: implemented minimal.

Round 133 refines the lightweight dashboard into a more browsable static page
for public demos and local research reviews.

## What It Adds

- project overview cards;
- evidence status cards;
- artifact completeness cards;
- visual readiness cards;
- route status section;
- failure board section;
- related work board section;
- advisor next action card;
- static section navigation;
- static search index payload;
- safe demo mode badge.

## Outputs

- `RefinedDashboardBundle`
- `DashboardNavItem`
- `DashboardCard`
- `DashboardFilterOption`
- `DashboardSearchEntry`
- `refined_dashboard.html`

## VGGT Fixture

The refined VGGT dashboard reads only committed local review artifacts from:

- `examples/vggt-human-prior-survey/research_knowledge_pack/`
- `examples/vggt-human-prior-survey/advisor_pack/`
- `examples/vggt-human-prior-survey/dashboard/`

and writes:

- `examples/vggt-human-prior-survey/dashboard_html/refined_dashboard.html`

## Public Demo Fixture

The public demo refined dashboard is written to:

- `examples/public_demo/demo_dashboard_refined.html`

It is fake/demo material only.

## Safety Boundary

- No login.
- No SaaS.
- No cloud service.
- No server requirement.
- No default networking.
- No private VGGT path read.
- No Modal execution.
- No VGGT execution.
- UI display is not an experiment result.
- SparseConv3D success is not claimed by the UI.

## Limitations

- Search is a static JSON payload, not an interactive remote search service.
- Filters are static labels and counts.
- Cards summarize existing Markdown artifacts; they are not evidence
  verification.
- Human review remains required.
