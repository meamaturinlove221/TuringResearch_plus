# Experiment Runbook E2E

Status: v1.4 fake/default production parity demo.

Round: 319.

This E2E demo turns a safe experiment intent into a route DSL, artifact
requirements, runbook, and ingest expectations:

```text
experiment intent -> route DSL -> hard gates -> artifact requirements -> runbook -> ingest expectations
```

It does not run an experiment and does not call GPU, Modal, SSH, or any remote
executor.

## Inputs

The demo workspace is:

- `examples/experiment_execution/e2e_runbook_demo/experiment_intent.md`
- `examples/experiment_execution/e2e_runbook_demo/route_dsl.json`

## Runtime Surfaces

The workflow test runs:

- `ExperimentRouteSpec.model_validate_json`
- `build_artifact_requirements`
- `build_experiment_execution_plan`
- `render_experiment_execution_runbook`

## Outputs

- `artifact_requirements.md`
- `safe_runbook.md`
- `ingest_expectations.json`
- `e2e_summary.md`

## Safety Boundary

- fake/demo only;
- no automatic experiment execution;
- no GPU;
- no Modal;
- no remote execution;
- no observed result write;
- only generates runbook and ingest contract;
- proposed evidence only;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_experiment_runbook_e2e.py -q
```
