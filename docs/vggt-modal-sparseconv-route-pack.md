# VGGT Modal SparseConv3D Route Pack

Status: route pack generated for future VGGT-side execution.

Round 51 packages the Sprint 2 route, hard gates, failure taxonomy, controller
prompt, artifact requirements, advisor summary, and architecture diagram for a
future Modal Real SparseConv3D + SMPL-X voxel feature encoding experiment.

## Location

`examples/vggt-human-prior-survey/modal_sparseconv_route_pack/`

## North Star

`SMPL-X direct replacement -> SMPL-X feature encoding for VGGT`

The route pack keeps VGGT's core objective intact and treats SMPL-X as a source
of structured feature context rather than a direct replacement.

## Contents

| File | Purpose |
| --- | --- |
| `README.md` | Overview and safety boundary. |
| `route_spec.yaml` | Planned route spec for future VGGT-side execution. |
| `hard_gates.md` | Promotion-blocking hard gate checklist. |
| `failure_taxonomy.md` | Failure categories and next-action policy. |
| `codex_controller_prompt.md` | Prompt to use inside the VGGT project later. |
| `artifact_requirements.md` | Required outputs for any real run. |
| `advisor_summary.md` | Advisor-safe summary. |
| `architecture.mmd` | Mermaid route architecture. |

## Current Evidence State

- `local_project_links.yaml`: missing.
- `local_scan_evidence_ledger.json`: missing.
- `local_scan_visual_inventory.md`: missing.
- Modal run: not executed by TuringResearch.
- VGGT run: not executed by TuringResearch.
- SparseConv3D success: not established.

## Required Future Execution Boundary

The route can only move from planned to observed if the VGGT project produces
real artifacts:

- real sparse backend probe;
- candidate predictions;
- board inventory;
- NPZ diff or thin summary;
- sha256 manifest;
- cleanup report;
- advisor summary;
- failure report when blocked or failed.

## Non-Goals

- No Modal execution in TuringResearch.
- No VGGT execution in TuringResearch.
- No network access.
- No private `D:/vggt` reads.
- No fabricated experiment results.
- No planned-to-observed promotion without real evidence.
