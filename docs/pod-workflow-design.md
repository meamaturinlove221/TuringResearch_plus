# Pod Workflow Design

Status: v0.3 Sprint 1 design draft.

Pod Workflow describes how TuringResearch Plus prepares context for a remote
worker environment and receives structured outputs back for local review.

## Workflow

1. Build a context package from route, hard gates, artifact requirements,
   advisor intent, and memory summary.
2. Commit or stage the context package in a Git branch or handoff repository.
3. A remote pod consumes the context package manually or through a separate
   operator-controlled process.
4. The pod writes structured outputs.
5. Outputs return via git push or handoff bundle.
6. TuringResearch imports outputs through Run Ingestor and Artifact Auditor.
7. Evidence Ledger receives proposed updates only after human review.
8. Advisor Pack can summarize accepted inputs.

## Pod Output Package

Required files:

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

## Execution Boundary

TuringResearch Plus does not execute remote code and does not control Modal,
RunPod, or other pod providers. It designs context, validates outputs, and
maintains evidence discipline.

## Review Boundary

Pod output is not automatically trusted. Every returned package is checked for:

- missing files;
- unsafe files;
- inconsistent sha256;
- planned status written as observed;
- missing hard-gate evidence;
- missing visual or artifact proof.
