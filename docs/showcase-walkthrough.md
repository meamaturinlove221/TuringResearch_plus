# Showcase Walkthrough

Status: v1.1 showcase walkthrough draft.

Round: 220.

This walkthrough gives a GitHub visitor or interviewer a safe path through the
TuringResearch public materials. It uses only public/demo files.

## 1. Read The Pitch

Open `README.md`, then `docs/public-showcase.md`.

Expected takeaway: TuringResearch is a local-first Research OS for evidence,
artifact, paper, route, dashboard, plugin, and privacy-aware review workflows.

## 2. Inspect The Architecture

Open:

- `docs/architecture-diagram-final.mmd`
- `docs/research-os-flow.mmd`
- `docs/v1.1.0-docs-dashboard-integration-report.md`

Expected takeaway: the project is a monorepo with modular namespaces, public
demo fixtures, local docs, and read-only dashboard surfaces.

## 3. Run The Public Demo Path

Read:

- `docs/v1.0.0-quickstart.md`
- `docs/v1.0.0-public-demo-walkthrough.md`
- `examples/public_demo/SHOWCASE.md`

Expected takeaway: the demo path is fake/demo only and does not require API
keys, network access, VGGT data, or private files.

## 4. Open Dashboard Surfaces

Inspect:

- `examples/public_demo/demo_dashboard_refined.html`
- `docs/dashboard-data-api.md`
- `docs/local-server-dashboard.md`

Expected takeaway: dashboards are review surfaces, not experiment result
claims.

## 5. Review Paper Workflow

Inspect:

- `examples/public_demo/demo_related_work.md`
- `examples/public_demo/demo_advisor_pack.md`

Expected takeaway: paper material is scaffold and review state. It does not
automatically create a final paper.

## 6. Review Plugin Safety

Inspect:

- `docs/plugin-guide.md`
- `docs/plugin-sandbox-policy.md`
- `.github/ISSUE_TEMPLATE/plugin_proposal.md`

Expected takeaway: plugin permissions are explicit, unknown plugin execution is
restricted, and review is required.

## 7. Review Privacy And Claims

Inspect:

- `docs/v1.0.0-security-audit.md`
- `docs/v1.0.0-privacy-audit.md`
- `split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md`

Expected takeaway: public materials avoid private payloads and unsupported
claims.

## Suggested Demo Order

1. README first screen.
2. Public showcase page.
3. Public demo walkthrough.
4. Evidence ledger and artifact audit.
5. Dashboard screenshot or local preview.
6. VGGT public-safe case study.
7. Plugin safety policy.
8. Roadmap and limitations.
