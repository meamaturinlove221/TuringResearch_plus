# Lane 123: Public Demo Expansion

Round: 142

Status: implemented minimal.

## Goal

Expand the public demo from a single VGGT-like walkthrough into a small
multi-project demo suite covering experiment-style, paper-survey, and
software-tooling research workflows.

## Implemented

- `examples/public_demo/projects/vggt_like_demo/`
- `examples/public_demo/projects/paper_survey_demo/`
- `examples/public_demo/projects/software_tooling_demo/`
- `examples/public_demo/workspace_demo/`
- `examples/public_demo/dashboard/`
- `docs/public-demo-expansion.md`
- `tests/workflow/test_public_demo_expansion.py`

## Demo Project Files

Each demo project includes:

- `README.md`
- `north_star.md`
- `evidence_ledger.json`
- `artifact_index.md`
- `related_work.md`
- `advisor_pack.md`
- `dashboard.html`

## Boundaries

- All content is fake/demo.
- No private VGGT material.
- No private model file.
- No credential value.
- No data payload.
- No fake result marked observed.
- No live service or network requirement.
- Human review remains required.

## Validation

- `tests/workflow/test_public_demo_expansion.py`
- public demo privacy gate
- public demo suite tests
