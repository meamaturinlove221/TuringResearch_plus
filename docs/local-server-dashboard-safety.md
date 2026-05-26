# Local Server Dashboard Safety

Status: safety policy.

Round: 217.

The local server dashboard is intentionally small and local-only.

## Required Safety Boundary

- Bind only to `127.0.0.1` or `localhost`.
- Serve read-only summaries.
- Do not provide login.
- Do not expose a public network service.
- Do not upload data.
- Do not execute commands.
- Do not read private VGGT paths.
- Do not display secrets.
- Do not enable live adapters by default.

## Allowed Inputs

- `examples/public_demo/demo_dashboard_refined.html`
- `examples/public_demo/demo_research_intent.md`
- `examples/public_demo/demo_evidence_ledger.json`
- `examples/public_demo/demo_artifact_index.md`
- `examples/public_demo/demo_related_work.md`
- `examples/public_demo/demo_advisor_pack.md`

## Human Review

Any route added after v1.1 must pass privacy, secret, and local-path checks
before it is exposed by the local dashboard.
