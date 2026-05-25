# VGGT Case Study Redaction Report

Status: public-safe draft
Round: Optional 338.5
Date: 2026-05-25

## Redaction Rules Applied

| Rule | Status | Notes |
| --- | --- | --- |
| Remove private absolute paths | observed | Public case files use generic evidence labels instead of local machine paths. |
| Exclude raw data | observed | No raw data is included or referenced as a package asset. |
| Exclude SMPL-X model files | observed | No model files are copied or listed. |
| Exclude huge artifacts | observed | No npz, ply, zip, checkpoint, or bundle files are included. |
| Exclude unsupported claims | observed | Claims are marked `observed`, `local-observed`, `requires-human-review`, or `missing`. |
| Keep main repo flagship | observed | The split case is documented as a derived public-safe draft. |

## Redacted Evidence Categories

- Local root locations are summarized as "local VGGT workspace".
- Report files are summarized by work-stream label and evidence type.
- Visual files are summarized as metadata classes; no image content is embedded.
- Large array, pointcloud, archive, and bundle references are summarized as excluded artifact classes.

## Missing Inputs

- missing: public case safety checklist input was not present when this refresh ran.
- missing: original-repo replication progress input was not present when this refresh ran.
- requires-human-review: public split readiness still needs maintainer review.
