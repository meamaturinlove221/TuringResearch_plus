# Project Screenshot Plan

Status: planning draft.

Round: 157.

This plan lists screenshot candidates for future public positioning. It does
not generate images.

## Screenshot Goals

- show the product shape quickly;
- avoid private data;
- show fake/demo boundaries;
- make the project feel concrete without overclaiming results.

## Candidate Screenshots

1. Public demo dashboard
   - Source: `examples/public_demo/dashboard/`
   - Shows: multiple demo projects, safe demo mode, dashboard cards.

2. Refined VGGT dashboard
   - Source: `examples/vggt-human-prior-survey/dashboard_html/refined_dashboard.html`
   - Shows: evidence status, artifact readiness, route status, failures, advisor next action.
   - Boundary: dogfooding case, not success evidence.

3. Advisor export quality report
   - Source: `examples/vggt-human-prior-survey/advisor_export/export_quality_report.md`
   - Shows: export gate and optional backend skip behavior.

4. Public case-study draft
   - Source: `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
   - Shows: redacted case-study structure and what not to claim.

5. Vault UI
   - Source: `examples/vggt-human-prior-survey/vault_ui/index.html`
   - Shows: concept, paper, method, artifact, claim, failure, and route nodes.

## Safety Rules

- Use fake/demo or redacted material only.
- Do not show private paths.
- Do not show raw data.
- Do not show model payloads.
- Do not show API keys or tokens.
- Do not imply experiment success.

## Output Location

Future screenshots should go under a dedicated public-safe asset directory only
after privacy and claim-safety review.
