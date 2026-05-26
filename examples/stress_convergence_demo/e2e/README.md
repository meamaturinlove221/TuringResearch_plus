# Stress / Convergence E2E Demo

Status: public-safe fake/demo only.

Round: 318.

This demo connects the stress scenario library to the convergence decision
report:

1. Candidate routes are listed in `route_candidates.json`.
2. Each route receives a deterministic stress-test review.
3. Routes with stress blockers are excluded from convergence promotion.
4. Passing routes are compared by the convergence decision report.
5. The final recommendation remains review-only and does not execute routes.

## Contents

- `route_candidates.json`
- `stress_report.md`
- `convergence_decision.md`
- `e2e_summary.md`

## Safety Boundary

- fake/demo only;
- no multi-agent runtime;
- no route execution;
- no default network;
- no Evidence Ledger mutation;
- no automatic promotion;
- human review required.
