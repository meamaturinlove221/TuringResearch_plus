# Experiment Intent

Status: fake/demo only.

Intent: plan a safe review route for a hypothetical experiment bundle without
running the experiment.

The output should be a route DSL, hard gate checklist, artifact requirement
table, safe runbook, and ingest expectation contract.

Safety constraints:

- no automatic experiment execution;
- no GPU;
- no Modal;
- no remote execution;
- no observed result write;
- only generates runbook and ingest contract;
- human review required.
