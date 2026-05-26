# Stress / Convergence E2E

Status: v1.4 fake/default production parity demo.

Round: 318.

This E2E demo connects the stress scenario library to the convergence decision
report:

```text
candidate routes -> stress reports -> eligible candidates -> convergence decision
```

It does not execute any route. Stress review and convergence scoring are local,
deterministic, and review-only.

## Inputs

The demo workspace is:

- `examples/stress_convergence_demo/e2e/route_candidates.json`

It contains three routes:

- `route-safe-docs-polish`
- `route-live-provider-rush`
- `route-heavy-refactor`

## Runtime Surfaces

The workflow test runs:

- `build_stress_scenario_library`
- `run_stress_test`
- `render_stress_test_report`
- `build_convergence_decision_report`
- `render_convergence_decision_report`

## Expected Review Findings

- `route-safe-docs-polish` passes stress review and wins convergence.
- `route-live-provider-rush` is blocked by stress findings.
- `route-heavy-refactor` passes stress review but is held by convergence
  feasibility/resource checks.
- The final recommendation is `route-safe-docs-polish`.

## Safety Boundary

- fake/demo only;
- no multi-agent runtime;
- no route execution;
- no default network;
- no Evidence Ledger mutation;
- no automatic promotion;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_stress_convergence_e2e.py -q
```
