# Public Demo Guide

Status: v0.7 public demo guide.

The public demo is located at `examples/public_demo/`.

## Open Locally

Start with:

- `examples/public_demo/README.md`
- `examples/public_demo/dashboard/index.html`

Then browse:

- `examples/public_demo/projects/vggt_like_demo/`
- `examples/public_demo/projects/paper_survey_demo/`
- `examples/public_demo/projects/software_tooling_demo/`
- `examples/public_demo/workspace_demo/`

## What It Demonstrates

- Evidence ledger shape.
- Artifact index shape.
- Related-work scaffold shape.
- Advisor pack shape.
- Static dashboard shape.
- Multi-project demo workspace.

## Safety Boundary

- Everything is fake/demo.
- Demo evidence is not observed experiment evidence.
- Demo dashboards are not results.
- No server, login, or network access is required.
- Human review remains required.

## Validation

```powershell
python -m pytest tests/workflow/test_public_demo_expansion.py tests/workflow/test_public_demo_suite.py -q
python -m pytest tests/workflow/test_public_demo_privacy_gate.py -q
```
