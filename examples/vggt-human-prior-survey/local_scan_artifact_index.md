# VGGT Local Scan Artifact Index

Round: Optional 337.5
Date: 2026-05-25
Index mode: metadata-only, no artifact copy

This index records lightweight local file evidence from the VGGT co-location scan. It intentionally avoids private machine paths in the current cloud baseline and does not copy VGGT artifacts into TuringResearch Plus.

## Root Candidates

| Candidate | Status | Notes |
| --- | --- | --- |
| VGGT parent workspace | local-observed | Local VGGT parent existed during the scan. |
| VGGT main checkout | local-observed | Main checkout existed during the scan. |
| VGGT feature-adapter checkout | local-observed | Feature-adapter checkout existed during the scan. |
| VGGT live high-res crop checkout | local-observed | Live crop checkout existed during the scan. |

## Lightweight Reports And Manifests

| Evidence class | Status | Notes |
| --- | --- | --- |
| V44 visual pre-promotion gate report | local-observed | Report metadata existed; not treated as promotion. |
| V32 Open3D point review report | local-observed | Point-review metadata existed; no pointcloud copied. |
| V600 quality rebuild final status | local-observed | Local status metadata existed; ready-not-promoted wording remains guarded. |
| V600 completion audit | local-observed | Audit metadata existed; content is local report evidence only. |
| V850 integrity summary | local-observed | Existing summary mentioned npz/ply integrity; arrays and pointcloud files were not copied. |
| V900 readiness review report | local-observed | Report stated readiness-review-not-promotion. |
| V930 package/process reports | local-observed | Package and process metadata existed. |
| V120/V121 goal manifests | local-observed | Goal-manifest evidence existed; not proof of backend success. |

## Tool And Controller File Evidence

| Evidence class | Status | Notes |
| --- | --- | --- |
| V120 causal-batch tooling | local-observed | File presence only; not executed. |
| V120 paper-grade surface backend tooling | local-observed | File presence only; not executed. |
| V121 SparseConv mentor visual gate tooling | local-observed | File presence only; success requires human review. |
| V999 long-run feature-adapter controller | local-observed | File presence only; not executed. |

## Large Artifact Handling

- planned: huge npz, ply, zip, raw data, and SMPL-X model files should remain outside TuringResearch Plus.
- local-observed: existing integrity summaries can describe keys and shapes, but this index does not copy arrays.
- requires-human-review: any public split package must pass a privacy gate before assets are selected.
