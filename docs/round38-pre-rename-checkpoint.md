# TulingResearch Plus Round 38 Pre-Rename Checkpoint

Status: pre-rename checkpoint.

This checkpoint freezes the completed old Round 38 surface before any project
rename from TulingResearch to TuringResearch. This round does not rename files,
packages, skills, MCP server names, docs, or workflow references. It does not
implement new features, access the network, or read VGGT local paths.

## Completed Old Round 38 Files

### Evidence Ledger

| Path | Status |
| --- | --- |
| `src/tuling_research_plus/vggt/` | present |
| `src/tuling_research_plus/vggt/evidence_models.py` | present |
| `src/tuling_research_plus/vggt/evidence_ledger.py` | present |
| `src/tuling_research_plus/vggt/tools.py` | present |
| `contracts/vggt_evidence.yaml` | present |
| `tests/unit/test_vggt_evidence_models.py` | present |
| `tests/unit/test_vggt_evidence_ledger.py` | present |
| `tests/workflow/test_vggt_evidence_ledger_from_local_scan.py` | present |

### Artifact Auditor

| Path | Status |
| --- | --- |
| `src/tuling_research_plus/artifact_audit/` | present |
| `src/tuling_research_plus/artifact_audit/models.py` | present |
| `src/tuling_research_plus/artifact_audit/auditor.py` | present |
| `src/tuling_research_plus/artifact_audit/npz_summary.py` | present |
| `src/tuling_research_plus/artifact_audit/manifest.py` | present |
| `src/tuling_research_plus/artifact_audit/tools.py` | present |
| `contracts/artifact_audit.yaml` | present |
| `tests/unit/test_artifact_audit_models.py` | present |
| `tests/unit/test_artifact_manifest.py` | present |
| `tests/unit/test_npz_summary.py` | present |
| `tests/workflow/test_artifact_audit_from_vggt_scan.py` | present |

## Missing Old Round 38 Requested Files

These files were requested for this checkpoint surface but are not part of the
completed old Round 38 implementation currently in the repository:

| Path | Status | Action |
| --- | --- | --- |
| `src/tuling_research_plus/vggt/edge_audit.py` | missing | Record only; do not implement in checkpoint. |
| `src/tuling_research_plus/vggt/markdown_export.py` | missing | Record only; ledger currently exposes `to_markdown()` on the model. |
| `tests/unit/test_vggt_evidence_edge_audit.py` | missing | Record only; do not add edge audit tests before rename. |

## Rename Candidate Paths

These paths are likely to be touched by the future rename, but Round 38.1 does
not rename them:

| Current path or name | Future rename concern |
| --- | --- |
| `src/tuling_research/` | Core package import path. |
| `src/tuling_research_plus/` | Plus package import path. |
| `src/tuling_research_plus/vggt/` | New Round 38 VGGT package import path. |
| `src/tuling_research_plus/artifact_audit/` | New Round 38 Artifact Auditor package import path. |
| `tests/**/test_*` imports | Tests import `tuling_research_plus` and must be updated atomically. |
| `contracts/*.yaml` | Contract names and project names reference TulingResearch Plus. |
| `.agents/skills/tulingresearch-*` | Skill prefix is still TulingResearch-specific. |
| `pyproject.toml` | Package discovery, package name, scripts, and metadata reference old names. |
| `docs/**` and `README.md` | Public display name and MCP server name appear throughout docs. |
| `tulingresearch-plus` | MCP server and entry point name. |

## High-Risk Rename Points

- Python import paths: `tuling_research` and `tuling_research_plus`.
- `pyproject.toml` package discovery and entry points.
- Tests importing old package names.
- Skill directories and frontmatter names using `tulingresearch-`.
- MCP server name `tulingresearch-plus`.
- Contract names, tool docs, and release freeze docs.
- Workflow docs and examples referring to old project name.
- Existing git branches and GitHub repository name if those are later renamed.

## Validation Status

Old Round 38 focused tests run during the checkpoint:

| Command | Result |
| --- | --- |
| `python -m pytest tests/unit/test_vggt_evidence_models.py tests/unit/test_vggt_evidence_ledger.py tests/workflow/test_vggt_evidence_ledger_from_local_scan.py` | passed, 8 tests |
| `python -m pytest tests/unit/test_artifact_audit_models.py tests/unit/test_artifact_manifest.py tests/unit/test_npz_summary.py tests/workflow/test_artifact_audit_from_vggt_scan.py` | passed, 10 tests |
| `python -m pytest tests/contract/test_name_integrity.py tests/contract/test_contract_schema_integrity.py` | passed, 7 tests |

`tests/unit/test_vggt_evidence_edge_audit.py` was not run because it is missing
from the old Round 38 surface.
