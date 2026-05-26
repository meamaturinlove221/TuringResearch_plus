# TuringResearch Plus Round 38 Implemented Surface

Status: pre-rename checkpoint surface.

## Evidence Ledger Surface

| Surface | Details |
| --- | --- |
| Package | `turing_research_plus.vggt` |
| Models | `VGGTEvidenceStatus`, `VGGTEvidenceRow`, `VGGTEvidenceLedger`, `VGGTEvidenceLedgerBuildInput` |
| Builder | `build_vggt_evidence_ledger()` |
| Tool wrapper | `vggt_evidence_ledger_build()` |
| Contract | `contracts/vggt_evidence.yaml` |
| Tests | `test_vggt_evidence_models.py`, `test_vggt_evidence_ledger.py`, `test_vggt_evidence_ledger_from_local_scan.py` |

Supported statuses:

- `observed`
- `local-observed`
- `planned`
- `fake-data`
- `failed`
- `hard-blocked`
- `requires-real-paper`
- `requires-real-experiment`
- `requires-human-review`
- `not-enough-evidence`

Known boundaries:

- V120 and V121 stay `requires-human-review` without local evidence.
- SparseConv3D backend success stays `not-enough-evidence` without real evidence.
- No VGGT local path read is required.

## Artifact Auditor Surface

| Surface | Details |
| --- | --- |
| Package | `turing_research_plus.artifact_audit` |
| Models | `ArtifactAuditInput`, `ArtifactAuditReport`, `ArtifactRecord`, `ArtifactBundleManifest`, `NPZArraySummary` |
| Auditor | `audit_artifacts()` |
| Tool wrapper | `artifact_audit()` |
| Helpers | `load_manifest_like_index()`, `infer_file_type()`, `summarize_npz()` |
| Contract | `contracts/artifact_audit.yaml` |
| Tests | `test_artifact_audit_models.py`, `test_artifact_manifest.py`, `test_npz_summary.py`, `test_artifact_audit_from_vggt_scan.py` |

Known boundaries:

- Markdown local scan indexes are supported.
- JSON manifest-like inputs are supported.
- Private or external VGGT paths such as `D:/vggt` are marked omitted and not read.
- NPZ summary reads headers only and does not load large arrays.

## Not Implemented In Old Round 38

- Visual Evidence Auditor.
- Advisor Pack Builder.
- PDF Phase B full extraction.
- `edge_audit.py`.
- `markdown_export.py`.
- Cross-machine sync adapters.
- Public MCP namespace registration for `vggt.*` or `artifact.*`.

