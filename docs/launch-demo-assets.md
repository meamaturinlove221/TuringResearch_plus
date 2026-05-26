# Launch Demo Assets

Status: planning draft.

Round: 163.

This document identifies public-safe demo assets for a future main repo launch.
It does not generate screenshots or GIFs.

## Primary Assets

- `examples/public_demo/dashboard/`
- `examples/public_demo/demo_dashboard_refined.html`
- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`
- `examples/vggt-human-prior-survey/dashboard_html/refined_dashboard.html`
- `examples/portfolio/turingresearch_architecture.mmd`

## Screenshot Candidates

1. Public demo dashboard.
2. Refined VGGT dashboard.
3. Case-study draft with safety boundary.
4. Plugin safety / compatibility report.
5. Architecture diagram.

## GIF Candidates

1. Public demo walkthrough.
2. VGGT case redaction and claim-safety review.
3. Plugin manifest to sandbox policy to compatibility report.

## Acceptance Gate

Every asset must pass:

- privacy scan;
- no-secrets scan;
- no raw-data scan;
- no private-path scan;
- no model-payload scan;
- claim safety review;
- README wording review.

## Asset Copy Rules

- Mark demo output as fake/demo.
- Do not imply experiment success.
- Do not show raw data.
- Do not show private paths.
- Do not show credentials.
- Do not use fake user quotes.
