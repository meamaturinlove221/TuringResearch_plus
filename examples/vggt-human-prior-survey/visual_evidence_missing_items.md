# VGGT Visual Evidence Missing Items

Round: 39B
Project: TuringResearch

These missing items are non-fatal for the local dry-run. They block advisor-ready
visual proof and must not be replaced by inferred or fabricated conclusions.

| Missing item | Status | Impact |
| --- | --- | --- |
| Machine-local private config | missing | The private local config is absent, so no VGGT project path was read. |
| Full-scene RGB pointcloud board | missing | Required as the mentor main visual evidence. |
| Same-scene VGGT baseline / adapter / controls board | missing | Required before advisor visual readiness. |
| Viewer-openable full-scene pointcloud artifact | missing | Required before pointcloud morphology can be inspected. |
| Board inventory | metadata-only | `local_scan_artifact_index.md` records lightweight report metadata only. |
| Full-body visual evidence | missing | Required for advisor visual readiness. |
| Hairline visual evidence | missing | Required because hairline regression is a known risk. |
| Hand close-up visual evidence | missing | Required because hand quality is a known failure area. |

## Not Accepted As Proof

- Root candidate paths from `local_scan_summary.md`.
- Mask boards without provenance.
- Delta boards without provenance.
- Heatmaps or proxy visualizations without a true visual evidence level.
- Any absent board file.
- Metadata-only report references without the underlying full-scene RGB pointcloud.

## Required Before Promotion

- Source artifact paths or stable artifact ids.
- Region labels for full body, hairline, and hands.
- Explicit proxy-versus-true-closeup classification.
- Evidence ledger links.
- Human review when the visual item is ambiguous.
