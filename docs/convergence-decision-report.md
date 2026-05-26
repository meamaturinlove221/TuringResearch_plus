# Convergence Decision Report

Status: implemented.

Round: 282.

This module turns convergence scoring into a local decision report that compares
routes, ranks candidates, and explains why one route is preferred.

It does not execute routes.

## What It Does

- Scores candidate routes with deterministic criteria.
- Builds a scoring matrix.
- Runs feasibility review.
- Builds optional pairwise comparisons.
- Keeps steelman notes for rejected or held routes.
- Produces a final recommendation with confidence and next actions.
- Renders a Markdown report for human review.

## Report Sections

- ranked candidates;
- scoring matrix;
- pairwise comparison;
- feasibility notes;
- rejected / held candidates;
- steelman notes;
- final recommendation;
- confidence;
- next actions.

## Safety Boundary

- local deterministic report only;
- no route execution;
- no network;
- no Evidence Ledger mutation;
- no fake/demo result promotion;
- human review required before implementation.

## Example

See:

- `examples/convergence_demo/README.md`
- `examples/convergence_demo/decision_report.md`

## Validation

Run:

```powershell
python -m pytest tests/unit/test_convergence_models.py tests/unit/test_convergence_scoring.py tests/unit/test_convergence_decision_report.py tests/workflow/test_convergence_decision_report_fake.py -q
```
