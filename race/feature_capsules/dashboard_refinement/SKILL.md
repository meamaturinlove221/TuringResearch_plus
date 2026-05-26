# Dashboard Refinement Skill

Status: planning skill draft.

Use this skill for v0.7 static dashboard refinement planning. It does not run a
server or convert dashboard display into experiment results.

## Inputs

- workspace overview
- evidence summary
- dashboard report
- paper assembly report
- benchmark report

## Outputs

- RefinedDashboardBundle
- DashboardSectionIndex
- DashboardReadinessReport

## Safety Rules

- Keep dashboard static and local.
- Do not run experiments.
- Do not mark dashboard display as observed evidence.
- Do not require network access.

## Related Contracts

- dashboard_refinement.yaml
- lightweight_dashboard.yaml
- modal_run_dashboard.yaml
