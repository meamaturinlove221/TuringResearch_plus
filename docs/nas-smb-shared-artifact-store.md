# NAS / SMB Shared Artifact Store

Status: v0.4 minimal implementation.

The NAS / SMB Shared Artifact Store scanner indexes artifacts from a local path
that the user has already mounted. TuringResearch does not mount SMB shares,
does not handle credentials, and does not write to the shared store.

## Scope

The minimal implementation supports:

- local mounted path scanning;
- relative path preservation;
- sha256 manifest generation for selected small files;
- selected small review files;
- large-file metadata-only reporting;
- unsafe file reporting;
- optional read-only lock-file check;
- proposed imports only.

## Output

`SharedStoreReport` contains:

- `mount_label`
- `root_path`
- `scan_status`
- `lock_status`
- `selected_files`
- `omitted_files`
- `large_files`
- `unsafe_files`
- `proposed_imports`
- `requires_human_review`

## Safety Rules

- Read-only scanning only.
- No deletion.
- No moving.
- No overwrite.
- No credential handling.
- No automatic mount.
- Large files are metadata-only by default.
- Raw data is omitted by default.
- SMPL-X model files are unsafe by default.
- Selected files keep relative paths and optional sha256.
- Shared artifacts are indexed, not verified.

## VGGT Use

For VGGT / Modal review, shared stores should contain thin summaries such as
`final_status.json`, `failure_report.md`, `artifact_index.md`, board inventory,
sha256 manifests, and advisor notes. Raw datasets, large arrays, body model
files, and private configs must stay out of selected imports.

## Evidence Boundary

The shared store scanner only emits proposed imports. Evidence Ledger promotion
requires a separate review step and must not write planned, missing, or indexed
artifacts as observed.
