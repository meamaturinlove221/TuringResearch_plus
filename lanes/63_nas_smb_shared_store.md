# Lane 63 - NAS / SMB Shared Artifact Store

Status: implemented minimal.

Round 82 adds read-only scanning for already mounted NAS / SMB shared artifact
store paths.

## Added

- `src/turing_research_plus/shared_store/`
- `contracts/nas_smb_shared_store.yaml`
- `docs/nas-smb-shared-artifact-store.md`
- `docs/shared-store-safety-policy.md`
- VGGT shared store fixture under
  `examples/vggt-human-prior-survey/shared_store_fixture/`

## Boundaries

- TuringResearch does not mount SMB shares.
- TuringResearch does not handle SMB credentials.
- The scanner is read-only.
- The scanner does not delete, move, or overwrite files.
- Raw data, secrets, cache paths, large files, and SMPL-X model files are
  omitted or marked unsafe.
- Selected files keep relative paths and optional sha256.
- The scanner emits proposed imports only and does not overwrite Evidence
  Ledger.

## Validation

Round 82 validation covers shared store models, local mount scanning, lock
policy, no-delete policy, fixture workflow, package imports, type checking, and
linting.
