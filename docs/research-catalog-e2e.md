# Research Catalog E2E

Round 315 turns the Research Catalog from a static dashboard into a fake/demo
workspace report workflow.

## Demo Path

`examples/research_catalog/e2e_demo/`

The demo workspace contains:

- `workspace_intent.md`
- `workspace_manifest.json`
- `vault_context.md`
- `route_spec.json`
- `catalog_report.json`
- `catalog_report.md`

## E2E Flow

1. Read the demo workspace intent.
2. Route the intent to a campaign and skill handoff.
3. Load Research Catalog dashboard groups.
4. Include local vault context.
5. Run deterministic stress review on demo inputs.
6. Build a safe experiment runbook summary.
7. Emit a catalog report for human review.

## What This Proves

- Campaign routing can connect workspace intent to `stress_test`.
- The catalog can display campaigns, skills, vault, stress, experiment
  runbooks, and advisor/release surfaces together.
- Stress review can run on demo workspace inputs.
- Experiment runbook planning can summarize artifact requirements.
- The generated report remains review-only.

## Safety Boundary

- no agent runtime;
- no automatic tool execution;
- no default network;
- no experiment execution;
- no Evidence Ledger mutation;
- no fake/demo result promotion;
- human review required.

The E2E report is not an experiment result and does not certify claims.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_research_catalog_e2e.py -q
```
