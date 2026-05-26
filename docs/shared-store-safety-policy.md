# Shared Store Safety Policy

Status: active for v0.4 remote artifact foundations.

The shared store safety policy treats NAS / SMB shares as already mounted local
paths. TuringResearch only indexes allowed review artifacts.

## Hard Boundaries

- Do not mount SMB shares.
- Do not handle SMB credentials.
- Do not delete files.
- Do not move files.
- Do not overwrite files.
- Do not mark shared artifacts as human verified.
- Do not auto-write Evidence Ledger updates.

## Forbidden Content

The scanner omits `.env`, secret-like filenames, raw data folders, private data,
cache folders, unsupported file types, large payloads, and SMPL-X body model
files.

## Large File Policy

Large files are represented as metadata-only entries with an omitted reason.
NPZ and PKL payloads default to summary-only treatment.

## Manifest Policy

Selected files keep relative paths. When sha256 is enabled, selected safe files
are hashed and recorded in the report manifest. Unsafe or large files are not
hashed by default.
