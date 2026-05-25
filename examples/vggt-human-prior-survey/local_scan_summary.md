# VGGT Local Freshness Scan Summary

Round: Optional 337.5
Date: 2026-05-25
Mode: local co-location freshness scan, read-only

## Safety Envelope

- observed: local VGGT root candidates existed on the VGGT desktop during the original scan.
- observed: no files were written inside the VGGT workspace.
- observed: no VGGT code or experiment command was run.
- observed: no raw data, SMPL-X model files, huge npz, ply, zip, or experiment bundle was copied into TuringResearch Plus.
- observed: no network access was used for the local scan itself.
- missing-at-scan-time: the private `local_project_links.yaml` was not committed and remains intentionally excluded.

## Current Integration Note

This file carries the Round 337.5 local freshness evidence forward onto the newer TuringResearch Plus cloud baseline. Some supporting case-study docs and split directories now exist in the new cloud branch; the evidence labels below still reflect the original read-only scan and should not be upgraded without human review.

## Freshness Signals

| Signal | Status | Evidence scope |
| --- | --- | --- |
| VGGT root co-location | local-observed | Candidate roots existed on the VGGT desktop during the scan. |
| V900/V930 feature-adapter reports | local-observed | Report files and package manifests existed; contents are local file evidence, not independent experiment reruns. |
| V999 long-run controller evidence | local-observed | Controller file existed; no run was executed. |
| V120/V121 file evidence | local-observed | Goal manifests and tool files existed; Modal/spconv success remains requires-human-review. |
| V600 quality rebuild reports | local-observed | Recent report metadata existed under the local VGGT workspace. |
| Visual evidence candidates | local-observed | Gate reports and PNG/pointcloud review metadata existed; no image or pointcloud content was analyzed. |
| split-ready case package | requires-human-review | Current cloud baseline includes split-ready case files, but public release readiness still requires human review. |

## Interpretation

- observed: the local VGGT workspace was present and contained report metadata at scan time.
- local-observed: V900/V930/V999/V120/V121 had local file-level evidence, but this scan does not promote any result, validate advisor readiness, or replace human review.
- requires-human-review: public split readiness, SparseConv3D backend success, advisor approval, and promotion.

## Output Policy

The scan outputs are summaries only. Raw datasets, SMPL-X model files, huge npz arrays, ply files, zips, and VGGT experiment bundles stay outside this repository.
