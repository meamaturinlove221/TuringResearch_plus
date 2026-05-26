# Experiment Runbook E2E Demo

Status: public-safe fake/demo only.

Round: 319.

This demo turns an experiment intent into a safe execution runbook and ingest
expectation contract:

```text
experiment intent -> route DSL -> hard gates -> artifact requirements -> runbook -> ingest expectations
```

It does not run experiments. It does not call GPU, Modal, or remote execution.

## Contents

- `experiment_intent.md`
- `route_dsl.json`
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
- human review required.
