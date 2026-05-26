# VGGT Visual Evidence Missing Items

Round: 39B
Project: TuringResearch Plus

These missing items are non-fatal for the local dry-run. They block advisor-ready
visual proof and must not be replaced by inferred or fabricated conclusions.

| Missing item | Status | Impact |
| --- | --- | --- |
| `examples/vggt-human-prior-survey/local_project_links.yaml` | missing | The private local config is absent, so no VGGT project path was read. |
| `examples/vggt-human-prior-survey/local_scan_visual_inventory.md` | missing | Visual evidence cannot be classified. |
| `examples/vggt-human-prior-survey/local_scan_evidence_ledger.json` | missing | Visual claims cannot be tied to local ledger rows. |
| Board inventory | missing | `local_scan_artifact_index.md` reports no scanned artifacts. |
| Full-body visual evidence | missing | Required for advisor visual readiness. |
| Hairline visual evidence | missing | Required because hairline regression is a known risk. |
| Hand close-up visual evidence | missing | Required because hand quality is a known failure area. |

## Not Accepted As Proof

- Root candidate paths from `local_scan_summary.md`.
- Mask boards without provenance.
- Delta boards without provenance.
- Heatmaps or proxy visualizations without a true visual evidence level.
- Any absent board file.

## Required Before Promotion

- Source artifact paths or stable artifact ids.
- Region labels for full body, hairline, and hands.
- Explicit proxy-versus-true-closeup classification.
- Evidence ledger links.
- Human review when the visual item is ambiguous.
