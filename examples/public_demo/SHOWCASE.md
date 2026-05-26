# Public Demo Showcase

Status: demo only.

This page gives a compact tour of the TuringResearch public demo. It does not
use private data, API keys, live adapters, real VGGT data, or restricted model
files.

## Project Pitch

TuringResearch is a local-first Research OS for evidence-led research
workflows. The public demo shows how evidence, artifacts, routes, paper
scaffolds, advisor packs, dashboards, and privacy checks can be inspected
without pretending that demo output is observed research evidence.

## Architecture

The demo connects:

- workspace overview;
- evidence ledger;
- artifact audit;
- visual inventory;
- paper and related-work scaffold;
- advisor pack;
- static dashboard;
- privacy gate.

## Public Demo Path

Start with:

- `README.md`
- `WALKTHROUGH.md`
- `EXPECTED_OUTPUTS.md`
- `demo_evidence_ledger.json`
- `demo_artifact_index.md`
- `demo_dashboard_refined.html`

## VGGT Case Study

The VGGT material in this repository is a public-safe dogfooding case study. It
is not a VGGT experiment source repository and does not claim SparseConv3D
success.

## Dashboard

Open:

- `demo_dashboard_refined.html`
- `dashboard/index.html`
- project dashboard files under `projects/*/dashboard.html`

Dashboards are review surfaces. They are not experiment outputs.

## Paper Workflow

Open:

- `demo_related_work.md`
- `demo_advisor_pack.md`

The paper workflow is scaffold-only and requires human review. It does not
write a final paper automatically.

## Plugin System

The demo does not execute unknown plugins. Plugin behavior is governed by the
main repository's manifest, permission, sandbox, and review policies.

## Privacy And Safety

The public demo excludes:

- private local paths;
- raw private data;
- credentials;
- restricted model files;
- unsupported success claims;
- observed fake results.

## Limitations

- Demo only.
- No live adapters are enabled.
- No real experiment is executed.
- No final research conclusion is generated.
- Human review remains required.

## Roadmap

The next public-showcase work focuses on richer docs pages, local dashboard
polish, more public demo cases, and release hardening.
