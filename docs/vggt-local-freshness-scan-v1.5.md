# VGGT Local Freshness Scan v1.5

Round: Optional 337.5
Date: 2026-05-25
Repository: TulingResearch Plus
Mode: read-only local co-location scan

## Purpose

This scan refreshes TulingResearch Plus metadata about the local VGGT workspace so a human can decide whether `split_ready/turingresearch-vggt-case` needs to be updated.

## Scope

- observed: scan ran on a machine where `D:/vggt` exists.
- observed: candidate VGGT roots were read as local file metadata.
- observed: scan outputs were written only under TulingResearch Plus.
- observed: no VGGT code was executed.
- observed: no VGGT experiment was run.
- observed: no file under `D:/vggt` was modified or deleted.
- observed: no raw data, SMPL-X model files, huge npz, ply, zip, or VGGT bundle was copied.

## Inputs

| Input | Status | Notes |
| --- | --- | --- |
| `examples/vggt-human-prior-survey/local_project_links.yaml` | missing | Private config absent; expected to remain untracked. |
| `examples/vggt-human-prior-survey/local_scan_summary.md` | local-observed | Refreshed this round. |
| `examples/vggt-human-prior-survey/local_scan_artifact_index.md` | local-observed | Refreshed this round. |
| `examples/vggt-human-prior-survey/local_scan_missing_items.md` | local-observed | Refreshed this round. |
| `docs/vggt-public-case-study-builder.md` | missing | Not present in this branch. |
| `docs/original-repo-replication-progress-report.md` | missing | Not present in this branch. |

## Local Evidence Findings

| Area | Status | Finding |
| --- | --- | --- |
| Co-location | local-observed | `D:/vggt`, `D:/vggt/vggt-main`, `D:/vggt/vggt-feature-adapter`, and `D:/vggt/vggt-live-highres-crop` exist. |
| V600 quality rebuild | local-observed | Recent report metadata exists under `local_report_auxiliary/V600_quality_rebuild`, including ready-not-promoted status wording. |
| V900/V930 | local-observed | Feature-adapter report files exist. V900 report states readiness review but not promotion; V930 process scan reports no residual training or Modal worker detected. |
| V999 | local-observed | Long-run controller file exists. It was not executed. |
| V120/V121 | local-observed | Goal manifests and sparseconv visual gate file evidence exist. Backend success is not confirmed by this scan. |
| Visual evidence | local-observed | V44 visual gate and V32 Open3D review report metadata exist. Visual content itself was not analyzed. |
| Split-ready case marker | missing | No explicit `split_ready`, `turingresearch-vggt-case`, or `tulingresearch-vggt-case` file-name marker was found. |

## Decision Boundary

The scan supports a conservative conclusion only:

- local-observed: local VGGT has fresh evidence worth reviewing for a public split case.
- requires-human-review: whether `split_ready/turingresearch-vggt-case` should be updated.
- missing: the case-study builder and original-repo replication progress docs were not available in this branch.
- blocked claim: this scan does not prove Modal/spconv success, final advisor approval, promotion, or paper-grade conclusion.

## Follow-Up For Public Case Work

- planned: restore or create the public case-study builder doc before making a split package decision.
- planned: run a privacy gate over any selected case assets.
- planned: include only derived summaries, small public-safe screenshots, and manifest metadata after human review.
- planned: keep raw data, SMPL-X model files, huge npz, ply, zip, and VGGT experiment archives outside TulingResearch Plus.
