# Public Demo Walkthrough

Status: demo only.

This walkthrough shows how to inspect the public demo safely. It does not use
network access, API keys, real VGGT material, raw data, or private project
files.

## 1. Workspace

Open:

- `workspace_demo/workspace_overview.md`
- `workspace_demo/workspace.yaml`

The workspace lists three demo projects: VGGT-like, paper survey, and software
tooling.

## 2. Evidence Ledger

Open:

- `demo_evidence_ledger.json`
- `projects/vggt_like_demo/evidence_ledger.json`
- `projects/paper_survey_demo/evidence_ledger.json`
- `projects/software_tooling_demo/evidence_ledger.json`

Expected status: `demo-only`.

Expected entry states: `planned`, `fake-data`, or `not-enough-evidence`.

There should be no observed result claim.

## 3. Artifact Audit

Open:

- `demo_artifact_index.md`
- each project `artifact_index.md`

Selected, missing, and omitted artifacts should be visible. Unsafe/raw items
stay excluded.

## 4. Visual Audit

Open:

- `demo_visual_inventory.md`
- `demo_dashboard.html`
- `demo_dashboard_refined.html`

Visual readiness is review state, not visual proof.

## 5. Paper Method

Open:

- `demo_related_work.md`
- `projects/paper_survey_demo/related_work.md`

The method and related-work material is scaffold-only and requires human
review.

## 6. Related Work

Read the safe and unsafe claim sections in the related-work files. The demo
shows how unsafe claims stay visible instead of becoming final prose.

## 7. Route DSL

Open:

- `projects/vggt_like_demo/north_star.md`
- `projects/vggt_like_demo/advisor_pack.md`

The route is planned review material. Planned does not mean executed.

## 8. Advisor Pack

Open:

- `demo_advisor_pack.md`
- each project `advisor_pack.md`

Advisor packs summarize status, limitations, and next actions. They do not
produce final research conclusions.

## 9. Dashboard

Open:

- `dashboard/index.html`
- each project `dashboard.html`

Dashboards are static review surfaces and not experiment results.

## 10. Privacy Gate

Run from the repository root:

```powershell
python -m pytest tests/workflow/test_public_demo_privacy_gate.py -q
```

The demo should remain free of private paths, raw data, private model payloads,
and credentials.
