# Visual Evidence Auditor

TuringResearch Plus uses the Visual Evidence Auditor boundary to prevent proxy
boards, masks, deltas, and missing image inventories from being mistaken for
advisor-ready visual proof.

Round 39B currently provides a dry-run artifact surface rather than a full image
classification implementation. The committed outputs are:

- `examples/vggt-human-prior-survey/visual_evidence_audit_report.md`
- `examples/vggt-human-prior-survey/visual_evidence_scorecard.json`
- `examples/vggt-human-prior-survey/visual_evidence_missing_items.md`

## Current Status

- `local_scan_visual_inventory.md` is missing.
- `local_scan_evidence_ledger.json` is missing.
- `local_scan_artifact_index.md` says no artifacts were scanned.
- Advisor-ready visual proof is blocked.
- Full body, hairline, and hand close-up evidence are missing.

## Readiness Rules

- If a board file does not exist, record it as missing.
- Mask, delta, heatmap, and proxy boards are not advisor-ready proof.
- Visual readiness requires source artifact provenance.
- Ambiguous visual evidence requires human review.
- V121 remains `requires-human-review` without true region pointcloud visual
  evidence.

## Non-Goals

- No VGGT execution.
- No image content inference without sidecar/provenance.
- No private `D:/vggt` reads.
- No fabricated visual conclusions.
