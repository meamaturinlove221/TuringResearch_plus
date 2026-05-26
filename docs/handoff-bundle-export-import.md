# Handoff Bundle Export / Import

TuringResearch Plus handoff bundles are controlled review packages for moving
small VGGT dogfooding artifacts between machines. They are not a sync layer.

## Scope

The minimal v0.2 beta implementation supports local export and import
validation for Markdown, JSON, YAML, CSV, PNG, JPG, and small text summaries.
It preserves relative paths and writes `HANDOFF_README.md` plus
`handoff_manifest.yaml`.

The manifest is intentionally review-first:

- `manual_review_required` is always true.
- status labels must stay conservative.
- import creates only a validation report and proposed updates.
- import does not overwrite Evidence Ledger, Artifact Audit, or Advisor Pack
  files.

## Safety Policy

The exporter omits unsafe files and records them in the manifest. Forbidden
content includes:

- `.env` and API key files
- paths containing `secrets`, `private_data`, `raw_data`, or cache folders
- Codex config folders that may contain secrets
- raw datasets
- `SMPLX_*.npz` and `SMPLX_*.pkl`
- large NPZ payloads unless represented by summary-only metadata

Large files are omitted and can be represented by `sha256`, size, and omitted
reason. NPZ files default to summary-only handoff.

## Export

`research.handoff_bundle_export` takes a `HandoffExportRequest` and writes a
bundle directory. Included files are copied; omitted files are recorded with
the reason and safety warnings.

Export does not use NAS, SMB, SSH, SFTP, GitHub artifact sync, cloud object
storage, or network access.

## Import

`research.handoff_bundle_import` validates a local bundle:

1. Parse `handoff_manifest.yaml`.
2. Check that included files exist.
3. Verify sha256 when requested.
4. Mark missing or unsafe files.
5. Produce `HandoffBundleImportReport`.
6. Emit proposed updates only.

The importer never auto-merges evidence and never marks planned or missing
items as observed.

## VGGT Use

For VGGT and SMPL-X work, handoff bundles should carry summaries, board
inventories, advisor notes, run ingest reports, and manifests. They must not
carry body model files or raw private data.

The fixture at
`examples/vggt-human-prior-survey/handoff_bundle_fixture/` demonstrates a
review-only bundle that keeps SparseConv3D status as not enough evidence.
