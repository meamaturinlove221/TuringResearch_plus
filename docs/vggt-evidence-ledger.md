# TuringResearch Plus VGGT Evidence Ledger

The VGGT Evidence Ledger is a v0.2.0 Sprint 1 minimal implementation for
recording VGGT / SMPL-X dogfooding evidence without overclaiming results.

## Purpose

It separates engineering context, local-observed evidence, planned work, missing
evidence, hard blockers, and human-review requirements.

## Required Row Fields

- `run_id`
- `version_label`
- `claim`
- `status`
- `evidence_refs`
- `source_files`
- `limitations`
- `blockers`
- `next_actions`

## Current VGGT Defaults

| Version | Status | Boundary |
| --- | --- | --- |
| V770 | `local-observed` | Diagnostic context from committed local scan summary; not promotion. |
| V129 | `observed` | Engineering context with limitations. |
| V260 | `hard-blocked` | Semantic assets unavailable in committed scan. |
| V900 | `observed` | Entrypoint engineering context. |
| V930 | `observed` | Short-training signal context. |
| V999 | `observed` | Route status only. |
| V999-SparseConv3D | `not-enough-evidence` | Backend success not proven. |
| V120 | `requires-human-review` | Missing local evidence ledger JSON. |
| V121 | `requires-human-review` | Missing visual inventory. |

## Safety

The ledger does not read VGGT local paths, run experiments, or infer success
from missing files. It only consumes committed scan summaries and optional
explicit local evidence ledger input.

## Non-Goals

- No advisor promotion decision.
- No final experiment result.
- No Visual Evidence Auditor.
- No cross-machine sync.
