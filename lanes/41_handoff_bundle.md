# Lane 41: Handoff Bundle Export / Import

## Scope

Round 60 implements minimal local handoff bundle export/import for
TuringResearch Plus. It supports VGGT review packages between machines without
implementing NAS, SMB, SSH, SFTP, GitHub artifact sync, or cloud storage.

## Input Notes

- `docs/local-co-location-mode.md` was not present in the current workspace.
- Existing local project link, run ingest, artifact audit, and evidence ledger
  docs were used as conservative context.

## Implemented Files

- `src/turing_research_plus/handoff/models.py`
- `src/turing_research_plus/handoff/exporter.py`
- `src/turing_research_plus/handoff/importer.py`
- `src/turing_research_plus/handoff/manifest.py`
- `src/turing_research_plus/handoff/safety.py`
- `src/turing_research_plus/handoff/tools.py`
- `contracts/handoff_bundle.yaml`
- `docs/handoff-bundle-export-import.md`
- `examples/vggt-human-prior-survey/handoff_bundle_fixture/`

## Safety Gates

- Secrets and `.env` files are omitted.
- Raw data and cache paths are omitted.
- SMPL-X body model files are omitted.
- NPZ payloads default to summary-only.
- Import validates but does not overwrite Evidence Ledger.

## Non-Goals

- No network.
- No remote sync.
- No automatic merge into ledgers.
- No real VGGT path reading.
- No claim that SparseConv3D succeeded.

## Validation

- `tests/unit/test_handoff_*.py`
- `tests/workflow/test_vggt_handoff_bundle_fixture.py`
- artifact audit focused tests
- VGGT evidence focused tests
