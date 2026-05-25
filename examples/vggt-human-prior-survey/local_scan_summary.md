# VGGT Local Freshness Scan Summary

Round: Optional 337.5
Date: 2026-05-25
Mode: local co-location freshness scan, read-only

## Safety Envelope

- observed: `D:/vggt`, `D:/vggt/vggt-main`, `D:/vggt/vggt-feature-adapter`, and `D:/vggt/vggt-live-highres-crop` exist on this machine.
- observed: no files were written inside `D:/vggt`.
- observed: no VGGT code or experiment command was run.
- observed: no raw data, SMPL-X model files, huge npz, ply, zip, or experiment bundle was copied into TulingResearch Plus.
- observed: no network access was used for the local scan itself.
- missing: `examples/vggt-human-prior-survey/local_project_links.yaml` is not present in this checkout, so the scan used the known local co-location candidates only.

## Required Input Readiness

| Input | Status | Notes |
| --- | --- | --- |
| `examples/vggt-human-prior-survey/local_project_links.yaml` | missing | Private machine config is intentionally not committed. |
| `examples/vggt-human-prior-survey/local_scan_summary.md` | local-observed | This file was refreshed by Round 337.5. |
| `examples/vggt-human-prior-survey/local_scan_artifact_index.md` | local-observed | Refreshed with metadata-only artifact references. |
| `examples/vggt-human-prior-survey/local_scan_missing_items.md` | local-observed | Refreshed with missing config and case-study inputs. |
| `docs/vggt-public-case-study-builder.md` | missing | Not available in this branch at scan time. |
| `docs/original-repo-replication-progress-report.md` | missing | Not available in this branch at scan time. |

## Freshness Signals

| Signal | Status | Evidence scope |
| --- | --- | --- |
| VGGT root co-location | local-observed | Candidate roots exist under `D:/vggt`. |
| V900/V930 feature-adapter reports | local-observed | Report files and package manifests exist; contents are treated as local file evidence, not independent experiment reruns. |
| V999 long-run controller evidence | local-observed | Controller file exists in `vggt-feature-adapter/tools`; no run was executed. |
| V120/V121 file evidence | local-observed | Goal manifests and tool files exist; Modal/spconv success remains requires-human-review. |
| V600 quality rebuild reports | local-observed | Recent report metadata exists under `D:/vggt/vggt-main/local_report_auxiliary/V600_quality_rebuild/reports`. |
| Visual evidence candidates | local-observed | Gate reports and PNG/pointcloud review metadata exist; no image or pointcloud content was analyzed. |
| `split_ready/turingresearch-vggt-case` marker | missing | Explicit `split_ready`, `turingresearch-vggt-case`, and `tulingresearch-vggt-case` file-name markers were not found. |

## Interpretation

- observed: the local VGGT workspace is present and contains fresh report metadata, especially V600 quality rebuild outputs from 2026-05-25 and V120/V121 goal manifests from 2026-05-22 to 2026-05-23.
- local-observed: V900/V930/V999/V120/V121 have local file-level evidence, but this scan does not promote any result, does not validate advisor readiness, and does not replace human review.
- requires-human-review: whether `split_ready/turingresearch-vggt-case` needs an update cannot be decided automatically because no explicit case-study marker was found in the local file-name scan.
- missing: the branch does not currently contain the public case-study builder docs requested as inputs.

## Output Policy

The scan outputs are intentionally summaries only. Raw datasets, SMPL-X model files, huge npz arrays, ply files, zips, and VGGT experiment bundles stay in `D:/vggt` and are not copied into this repository.
