# Dashboard Guide

Status: v0.7 dashboard guide.

TuringResearch Plus dashboards are local-first and static-first. They are
designed for browsing project state, evidence gaps, artifacts, routes, failures,
related work, and advisor next actions.

## Dashboard Types

- Public demo dashboard.
- Refined project dashboard.
- Modal run dashboard reports.
- Run comparison reports.
- Local vault UI.

## Safety Boundary

- No login.
- No hosted server.
- No default network access.
- No experiment execution.
- No dashboard card should be treated as a paper result.
- Human review remains required.

## Useful Docs

- [Lightweight Dashboard UI](lightweight-dashboard-ui.md)
- [Dashboard Refinement](dashboard-refinement.md)
- [Modal Run Dashboard](modal-run-dashboard.md)
- [Run Comparison](run-comparison.md)
- [Local-first Research Vault UI](local-first-research-vault-ui.md)

## Validation

```powershell
python -m pytest tests/workflow/test_vggt_refined_dashboard_html.py tests/workflow/test_vggt_vault_ui_fake.py -q
```
