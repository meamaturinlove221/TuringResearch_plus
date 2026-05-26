# Modal Run Dashboard

Status: v0.4 Markdown-first minimal implementation.

The Modal Run Dashboard renders a dashboard from an existing `RunIngestReport`.
It does not run Modal, does not run VGGT, does not access network resources, and
does not turn dashboard rows into experiment results.

## Scope

The dashboard shows:

- run status;
- route id;
- candidate count;
- best candidate;
- backend status;
- hard gates;
- artifact completeness;
- visual readiness;
- failure categories;
- next action;
- advisor readiness.

## Status Badges

Supported badges:

- `REVIEW_READY_NOT_PROMOTED`
- `HARD_BLOCKED`
- `ROUTE_EXHAUSTED`
- `FAILED`
- `PARTIAL`
- `NOT_ENOUGH_EVIDENCE`
- `REQUIRES_HUMAN_REVIEW`

## Evidence Boundary

The dashboard displays already ingested evidence only. It does not execute an
experiment and does not promote Evidence Ledger entries. SparseConv3D success
must remain unclaimed unless a real evidence ledger entry supports it.

## VGGT Use

For the VGGT Modal SparseConv3D fixture, the dashboard should make blockers
visible: missing real backend evidence, missing predictions, missing board
inventory, missing cleanup report, and insufficient visual proof.
