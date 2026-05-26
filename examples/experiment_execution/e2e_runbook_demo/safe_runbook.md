# Safe Experiment Execution Runbook: experiment-runbook-e2e

- Plan id: `experiment-runbook-e2e-safe-execution-plan`
- Status: `ready-for-human-run`
- Requires human review: `true`
- Automatically executes: `false`
- Remote execution: `false`
- Modal call: `false`
- GPU call: `false`
- Writes observed result: `false`

## Blockers

- none

## Runbook Steps

1. Review route `experiment-runbook-e2e` and confirm human owner.
2. Prepare artifacts listed in artifact requirements.
3. Validate hard gates: no_automatic_execution, no_gpu, no_modal, proposed_evidence_only.
4. Human operator runs experiment outside TuringResearch if approved.
5. Ingest exported run bundle with run ingest contract.
6. Review proposed evidence updates; do not write observed result automatically.
7. Expected artifact count: 10.

## Artifact Requirements

- `experiment-runbook-e2e-artifact-1`: intent summary
- `experiment-runbook-e2e-artifact-2`: route DSL
- `experiment-runbook-e2e-artifact-3`: hard gate checklist
- `experiment-runbook-e2e-artifact-4`: artifact requirement table
- `experiment-runbook-e2e-intent-route-dsl`: route DSL
- `experiment-runbook-e2e-plan-runbook-markdown`: runbook markdown
- `experiment-runbook-e2e-plan-hard-gate-checklist`: hard gate checklist
- `experiment-runbook-e2e-plan-artifact-requirement-table`: artifact requirement table
- `experiment-runbook-e2e-ingest-ingest-expectation-contract`: ingest expectation contract
- `experiment-runbook-e2e-ingest-proposed-evidence-update-draft`: proposed evidence update draft

## Hard Gates

- `no_automatic_execution`
- `no_gpu`
- `no_modal`
- `proposed_evidence_only`

## Run Ingest Contract

- Proposed evidence only: `true`
- Writes observed result: `false`
