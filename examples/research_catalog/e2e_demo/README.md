# Research Catalog E2E Demo

Demo-only workspace for generating a complete Research Catalog report.

Flow:

`demo workspace -> campaign route -> skill handoff -> vault context -> stress review -> experiment runbook -> catalog report`

Files:

- `workspace_intent.md`
- `workspace_manifest.json`
- `vault_context.md`
- `route_spec.json`
- `catalog_report.json`
- `catalog_report.md`

Safety:

- no agent runtime;
- no automatic tool execution;
- no default network;
- no experiment execution;
- no Evidence Ledger mutation;
- no fake/demo result promotion;
- human review required.
