# Pod Workflow Pack

Status: v0.3 Sprint 1 minimal implementation.

The Pod Workflow Pack turns an existing route pack into a review-only context
package plus a structured output template. It is meant for operator-controlled
VGGT / Modal / RunPod work, but TuringResearch Plus does not run the pod,
does not run SSH, does not run Modal, and does not execute remote code.

## Inputs

- Modal SparseConv3D route pack
- hard gates
- failure taxonomy
- artifact requirements
- advisor intent

## Generated Context Package

The generated context package contains:

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`
- `HARD_GATES.md`
- `ARTIFACT_REQUIREMENTS.md`
- `FAILURE_TAXONOMY.md`
- `ADVISOR_INTENT.md`
- `HANDOFF_MANIFEST.yaml`
- `README.md`

`MEMORY.md` is a handoff-safe summary only. It is not the source of truth.
Evidence Ledger, Artifact Audit, Run Ingest, and Handoff Manifest remain the
structured review surfaces.

## Structured Output Template

The pod-side output template contains:

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

Returned outputs must be audited before any evidence ledger update. Proposed
evidence updates are review inputs, not accepted observations.

## VGGT Fixture

The fixture at
`examples/vggt-human-prior-survey/pod_workflow_pack/` is derived from the Modal
SparseConv3D route pack. It is marked:

- `planned`
- `not executed by TuringResearch`
- `requires-real-experiment`

It does not claim SparseConv3D success and does not contain raw data, secrets,
or SMPL-X body model files.

## Safety

- Do not include API keys.
- Do not include `.env`.
- Do not include raw data.
- Do not include SMPL-X body model files.
- Large files must be represented by manifest, sha256, and omitted reason.
- Pod outputs must be auditable.

## Non-Goals

- No Git command execution.
- No SSH execution.
- No Modal or RunPod execution.
- No network access.
- No upstream code copying.
- No automatic Evidence Ledger overwrite.
