# Public Demo Quickstart

Status: demo only.

Round: 179.

This quickstart is public-safe. It does not require API keys, private VGGT
data, restricted body model files, live networking, or remote experiment
execution.

## 1. Run Demo Tests

From the repository root:

```powershell
python -m pytest tests/workflow/test_public_demo_suite.py tests/workflow/test_public_demo_expansion.py -q
```

## 2. Open The Demo Dashboard

Open:

- `examples/public_demo/dashboard/index.html`

Then inspect:

- `examples/public_demo/projects/vggt_like_demo/dashboard.html`
- `examples/public_demo/projects/paper_survey_demo/dashboard.html`
- `examples/public_demo/projects/software_tooling_demo/dashboard.html`

## 3. Inspect Evidence

Open:

- `examples/public_demo/demo_evidence_ledger.json`
- `examples/public_demo/projects/vggt_like_demo/evidence_ledger.json`
- `examples/public_demo/projects/paper_survey_demo/evidence_ledger.json`
- `examples/public_demo/projects/software_tooling_demo/evidence_ledger.json`

Expected: demo-only status and no observed result claim.

## 4. Inspect Advisor Pack

Open:

- `examples/public_demo/demo_advisor_pack.md`
- `examples/public_demo/projects/vggt_like_demo/advisor_pack.md`

Expected: current state, questions, limitations, and human review boundary.

## 5. Inspect Paper / Related Work Demo

Open:

- `examples/public_demo/demo_related_work.md`
- `examples/public_demo/projects/paper_survey_demo/related_work.md`

Expected: scaffold only, not final paper text.

## Boundary

- Demo only.
- No real experiment result.
- No final paper conclusion.
- No private data.
- No raw data.
- No model payload.
- No live adapter by default.
