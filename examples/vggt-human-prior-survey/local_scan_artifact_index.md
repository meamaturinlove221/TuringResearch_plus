# VGGT Local Scan Artifact Index

Round: Optional 337.5
Date: 2026-05-25
Index mode: metadata-only, no artifact copy

This index records lightweight local file evidence from the VGGT co-location scan. Paths point to the local VGGT workspace and are not copied into TulingResearch Plus.

## Root Candidates

| Path | Status | Notes |
| --- | --- | --- |
| `D:/vggt` | local-observed | Local VGGT parent exists. |
| `D:/vggt/vggt-main` | local-observed | Main VGGT checkout exists. |
| `D:/vggt/vggt-feature-adapter` | local-observed | Feature-adapter checkout exists. |
| `D:/vggt/vggt-live-highres-crop` | local-observed | Live high-res crop checkout exists. |

## Lightweight Reports And Manifests

| Path | Size bytes | Modified | Status | Notes |
| --- | ---: | --- | --- | --- |
| `D:/vggt/vggt-main/reports/20260509_v44_strict_visual_pre_promotion_gate.md` | 294 | 2026-05-09 05:47:46 | local-observed | Visual pre-promotion gate report; not treated as promotion. |
| `D:/vggt/vggt-main/reports/20260509_v44_strict_visual_pre_promotion_gate.json` | 1558 | 2026-05-09 05:47:46 | local-observed | Local report claims gate pass; requires human review before advisor readiness claims. |
| `D:/vggt/vggt-main/reports/20260508_v32_candidate_open3d_review.md` | 228 | 2026-05-09 05:44:29 | local-observed | Open3D point review report stub. |
| `D:/vggt/vggt-main/reports/20260508_v32_candidate_open3d_review.json` | 218 | 2026-05-09 05:44:29 | local-observed | Local report references sampled point review; no pointcloud copied. |
| `D:/vggt/vggt-main/local_report_auxiliary/V600_quality_rebuild/reports/V900000000000_completion_audit.json` | 4124 | 2026-05-25 01:10:21 | local-observed | Completion audit report; content is local report evidence only. |
| `D:/vggt/vggt-main/local_report_auxiliary/V600_quality_rebuild/reports/V900000000000_final_status.json` | 1168 | 2026-05-25 01:10:21 | local-observed | Final status report says ready-not-promoted; no promotion inferred. |
| `D:/vggt/vggt-main/local_report_auxiliary/V600_quality_rebuild/reports/V850000000000_npz_ply_html_integrity.json` | 9900 | 2026-05-25 01:10:21 | local-observed | Existing integrity summary was read; referenced npz/ply files were not copied. |
| `D:/vggt/vggt-feature-adapter/reports/V900000_plan_completed_to_readiness_review.json` | 494 | 2026-05-19 12:55:44 | local-observed | States readiness-review-not-promotion in local report. |
| `D:/vggt/vggt-feature-adapter/reports/V930000_package_manifest.json` | 266 | 2026-05-19 12:55:44 | local-observed | Package manifest exists. |
| `D:/vggt/vggt-feature-adapter/reports/V930000_final_process_and_modal_scan.json` | 252 | 2026-05-19 12:55:44 | local-observed | Local scan says no residual training or Modal worker detected. |
| `D:/vggt/vggt-feature-adapter/reports/V120100000000_goal_file_manifest.json` | 574 | 2026-05-23 23:36:23 | local-observed | V120-series goal manifest exists; not proof of backend success. |
| `D:/vggt/vggt-feature-adapter/reports/V1210000000_goal_file_manifest.json` | 423 | 2026-05-22 15:28:00 | local-observed | V121-series goal manifest exists; not proof of final advisor approval. |

## Tool And Controller File Evidence

| Path | Size bytes | Modified | Status | Notes |
| --- | ---: | --- | --- | --- |
| `D:/vggt/vggt-feature-adapter/tools/v120_build_causal_batches.py` | 8339 | 2026-05-22 11:19:35 | local-observed | File presence only; not executed. |
| `D:/vggt/vggt-feature-adapter/tools/v120100000000_paper_grade_surface_backend_pipeline.py` | 38584 | 2026-05-23 23:40:47 | local-observed | File presence only; not executed. |
| `D:/vggt/vggt-feature-adapter/tools/v12100000_sparseconv_mentor_visual_gate.py` | 7121 | 2026-05-20 03:26:08 | local-observed | SparseConv/mentor visual gate file exists; success requires human review. |
| `D:/vggt/vggt-feature-adapter/tools/v9400000_v9990000_longrun_feature_adapter_controller.py` | 42248 | 2026-05-19 17:07:56 | local-observed | V999 route controller exists; not executed. |

## Large Artifact Handling

- planned: huge npz, ply, zip, raw data, and SMPL-X model files should remain in `D:/vggt`.
- local-observed: existing integrity summaries mention npz keys and shapes, but this Round 337.5 output does not copy or submit those arrays.
- requires-human-review: any future public split package should use an explicit privacy gate before selecting visual thumbnails or derived summaries.
