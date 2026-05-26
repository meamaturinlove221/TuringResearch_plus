# README Launch Checklist v1.6

Round: 383
Status: checked

## Required Launch Sections

| Requirement | Status | Evidence |
| --- | --- | --- |
| local-first Research OS | pass | README opening and architecture |
| original repo production parity | pass | README parity section |
| docs site ready | pass | README docs site ready section |
| dashboard showcase | pass | README dashboard showcase section |
| split manual packs | pass | README split manual packs section |
| optional live disabled by default | pass | README MCP/optional live section |
| privacy/security gates | pass | README safety and privacy boundary |
| ARIS deferred | pass | README parity, roadmap, and references |

## Prohibited Claims

| Prohibited claim | Status |
| --- | --- |
| automatic research completion | absent |
| automatic final-paper writing | absent |
| fake benchmark result claims | absent |
| fake GitHub or Pages URL | absent |
| fake `user` count | absent |
| fake `star` count | absent |
| VGGT `success` claim | absent |
| SparseConv3D `success` claim | absent |
| ARIS implementation claim | absent |

## Manual Review Still Required

- final public license decision;
- release timing;
- GitHub release draft;
- docs deployment approval;
- split repository creation approval;
- PyPI/package name decision;
- any live-provider smoke run.

## Validation Targets

Run:

```powershell
python -m pytest tests/contract/test_public_name_integrity_turingresearch.py tests/contract/test_open_source_hygiene_gate.py tests/contract/test_public_release_hygiene.py -q
python -m pytest tests/contract/test_name_integrity.py -q
python -m ruff check .
```
