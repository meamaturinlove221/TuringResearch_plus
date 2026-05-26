# Lightweight Dashboard UI

Status: v0.5 minimal static implementation.

The Lightweight Dashboard UI renders existing local review artifacts into a
static HTML page and a Markdown companion file. It does not run a server, does
not require login, does not use network access, and does not execute VGGT or
Modal.

## Sections

- project overview
- evidence status
- artifact completeness
- visual readiness
- run dashboard
- related work
- failure taxonomy
- advisor next actions

## Outputs

- `index.html`
- `dashboard.md`
- `StaticDashboardSpec`

## VGGT Fixture

The VGGT fixture reads from:

- `examples/vggt-human-prior-survey/research_knowledge_pack/`
- `examples/vggt-human-prior-survey/advisor_pack/`
- `examples/vggt-human-prior-survey/dashboard/`

and writes:

- `examples/vggt-human-prior-survey/dashboard_html/index.html`
- `examples/vggt-human-prior-survey/dashboard_html/dashboard.md`

## Boundaries

- No login.
- No server.
- No complex JavaScript.
- No cloud deployment.
- No network access.
- No private VGGT local path reads.
- UI display is not an experiment result.
- SparseConv3D success is not claimed by the UI.
