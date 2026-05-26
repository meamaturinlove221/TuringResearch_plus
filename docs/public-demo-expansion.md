# Public Demo Expansion

Status: v0.7 fake/demo expansion.

Round 142 expands `examples/public_demo/` from a single demo surface into a
small multi-project public walkthrough. The expansion is still local-first and
static. It does not contain private research material, live service output, or
experiment results.

## Projects

The expanded demo includes three project examples:

- `vggt_like_demo`: an experiment-style route and evidence planning demo.
- `paper_survey_demo`: a paper survey and source review planning demo.
- `software_tooling_demo`: a quality gate and plugin-safety planning demo.

Each project contains:

- `README.md`
- `north_star.md`
- `evidence_ledger.json`
- `artifact_index.md`
- `related_work.md`
- `advisor_pack.md`
- `dashboard.html`

## Workspace Demo

`examples/public_demo/workspace_demo/workspace.yaml` groups the three demo
projects as a public-safe workspace. The workspace is a navigation and review
aid only. It is not an evidence source and does not promote project claims.

## Dashboard

`examples/public_demo/dashboard/index.html` is a static index for the expanded
demo. It links to the per-project dashboards and keeps the same safe demo mode
boundary:

- no login;
- no server;
- no network access;
- no live experiment execution;
- no result promotion.

## Safety Boundary

- All project entries are fake/demo.
- Evidence ledgers use `planned`, `fake-data`, and `not-enough-evidence`.
- No demo ledger entry is marked `observed`.
- No private project path is included.
- No private model file is included.
- No credential value is included.
- No data payload is packaged.
- Planned work remains planned.
- Human review is required before public claims.

## Validation

`tests/workflow/test_public_demo_expansion.py` checks required project files,
demo-only labels, safe ledgers, static dashboards, workspace links, privacy
scanner compatibility, and absence of forbidden public-demo payloads.
