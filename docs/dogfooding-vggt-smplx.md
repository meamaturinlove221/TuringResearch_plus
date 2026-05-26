# VGGT / SMPL-X Dogfooding Plan

Status legend: `observed`, `local-observed`, `planned`, `fake-data`,
`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,
`missing`.

Round 34 makes TuringResearch Plus the planning surface for local VGGT / SMPL-X
feature-adapter dogfooding. It is a planning round only: no VGGT experiment is
executed, no VGGT file is changed, no network source is queried, and no paper or
advisor conclusion is fabricated.

## North Star

| Topic | Status | Direction |
| --- | --- | --- |
| Method pivot | observed | SMPL-X direct replacement to SMPL-X feature encoding for VGGT. |
| Feature route | planned | Encode SMPL-X canonical, raster, tri-plane, sparse voxel, or sparse latent features as VGGT-readable context. |
| Advisor readiness | requires-human-review | Requires visual evidence inventory and human review; review-ready is not promotion. |

## Workflow

1. Local Evidence Intake: read `local_scan_summary.md`,
   `local_scan_artifact_index.md`, `local_scan_missing_items.md`,
   `local_scan_visual_inventory.md`, and `local_scan_evidence_ledger.json` when
   available.
2. Literature Survey: verify NeuralBody, HumanRAM, HART, HGGT, Fus3D,
   VGGT-HPE, human reconstruction, and sparse backend claims from real papers.
3. Gap Analysis: separate VGGT token-conditioning novelty from direct SMPL-X
   patch replacement and from existing human reconstruction methods.
4. Hypothesis Formation: keep H1-H5 evidence labels separate from promotion.
5. Ideation: score feature encodings, sparse backends, gates, auditors, and
   visual evidence workflows.
6. Convergence: select a Round 35 sprint only after evidence readiness is clear.
7. Experiment Planning: define baselines, ablations, metrics, and visual checks
   without running experiments in Round 34.

## Current Evidence Boundary

| Evidence class | Status | Notes |
| --- | --- | --- |
| Local root co-location | local-observed | Local scan summary records candidate VGGT roots. |
| Local artifact inventory | missing | Artifact index says no artifacts were scanned. |
| Local evidence ledger | missing | `local_scan_evidence_ledger.json` is absent. |
| Local visual inventory | missing | `local_scan_visual_inventory.md` is absent. |
| V900/V930/V999 | observed | User-provided engineering context only; local confirmation requires-human-review. |
| V120/V121 | requires-human-review | Not local-observed in Round 34. |

## Future Sync Adapters

These are future plans only:

| Adapter | Status |
| --- | --- |
| v0.3 Handoff Bundle Export / Import | planned |
| v0.4 NAS / SMB Shared Artifact Store | planned |
| v0.5 SSH / SFTP Remote Artifact Reader | planned |
| v0.6 GitHub Artifact Sync | planned |
| Cloud object storage adapter | planned |

