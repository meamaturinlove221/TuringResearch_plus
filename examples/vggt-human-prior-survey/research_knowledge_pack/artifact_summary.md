# Artifact Summary

## Available Artifacts

The committed TuringResearch example tree contains review artifacts, not raw
VGGT experiment outputs:

- Advisor pack Markdown files.
- Modal SparseConv3D route pack.
- Run ingest fixture and dry-run reports.
- Paper method card fixtures.
- Citation graph, collision risk, related work, and vault graph fixtures.
- Web fetch fixture HTML pages.
- Pod workflow and handoff bundle fixtures.

## Missing Artifacts

The current local scan reports no scanned artifacts. Required missing items
include:

- `local_scan_evidence_ledger.json`
- `local_scan_visual_inventory.md`
- `predictions.npz` or thin prediction summary
- board inventory
- full-body visual board
- hairline close-up visual board
- hand close-up visual board
- real sparse backend probe log
- sha256 manifest for real run outputs
- cleanup report

## Omitted Large Files

Large arrays and raw result payloads are not part of this review pack. Future
large files should be summarized with keys, shapes, dtypes, file size, and
sha256 hashes rather than copied into the repo.

## Unsafe or Unavailable Files

The pack must not include private configs, raw datasets, API keys, secrets,
SMPL-X body model files, cache folders, or huge NPZ payloads. Missing files
should stay missing in the report until a future local VGGT dry-run supplies
auditable summaries.
