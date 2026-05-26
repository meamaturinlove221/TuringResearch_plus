# TuringResearch Plus Post-Rename Test Report

Status: Round 38.6 validation complete.

## Focused Test Results

| Test group | Command | Result |
| --- | --- | --- |
| Name integrity | `python -m pytest tests/contract/test_name_integrity.py` | passed |
| Package imports | `python -m pytest tests/contract/test_package_imports.py` | passed |
| Skills integrity | `python -m pytest tests/contract/test_skills_integrity.py` | passed |
| Round 38 Evidence Ledger | `python -m pytest tests/unit/test_vggt_evidence_models.py tests/unit/test_vggt_evidence_ledger.py tests/workflow/test_vggt_evidence_ledger_from_local_scan.py` | passed |
| Round 38 Artifact Auditor | `python -m pytest tests/unit/test_artifact_audit_models.py tests/unit/test_artifact_manifest.py tests/unit/test_npz_summary.py tests/workflow/test_artifact_audit_from_vggt_scan.py` | passed |
| Contract suite | `python -m pytest tests/contract` | passed |
| Workflow suite | `python -m pytest tests/workflow` | passed |
| Full suite | `python -m pytest` | passed, 352 tests |
| Type check | `python -m mypy src` | passed |
| Lint | `python -m ruff check .` | passed |

## Repairs Made

- Added `turing_research_plus.vggt.edge_audit` as a minimal evidence-edge audit
  compatibility module.
- Added `turing_research_plus.vggt.markdown_export` as a minimal wrapper around
  existing ledger Markdown serialization.
- Extended package import tests to lock the post-rename Round 38 module surface.
- Kept subprocess MCP stdio tests independent of stale absolute paths by
  injecting the current repository `src` path into child-process `PYTHONPATH`.

## Residual Risk

The working branch still contains the large rename diff and has not been
committed or pushed. The old empty parent directory may remain on disk if held
open by an external process, but the active repository path is
`E:\TuringResearch\TuringResearch_plus`.
