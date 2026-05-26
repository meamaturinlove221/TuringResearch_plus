# Lane 18: Round 38 Pre-Rename Checkpoint

## Scope

This lane records the old TulingResearch Plus Round 38 implementation surface
before the rename to TuringResearch. It is a checkpoint only.

## Confirmed Present

### Evidence Ledger

- `src/tuling_research_plus/vggt/`
- `src/tuling_research_plus/vggt/evidence_models.py`
- `src/tuling_research_plus/vggt/evidence_ledger.py`
- `src/tuling_research_plus/vggt/tools.py`
- `contracts/vggt_evidence.yaml`
- `tests/unit/test_vggt_evidence_models.py`
- `tests/unit/test_vggt_evidence_ledger.py`
- `tests/workflow/test_vggt_evidence_ledger_from_local_scan.py`

### Artifact Auditor

- `src/tuling_research_plus/artifact_audit/`
- `src/tuling_research_plus/artifact_audit/models.py`
- `src/tuling_research_plus/artifact_audit/auditor.py`
- `src/tuling_research_plus/artifact_audit/npz_summary.py`
- `src/tuling_research_plus/artifact_audit/manifest.py`
- `src/tuling_research_plus/artifact_audit/tools.py`
- `contracts/artifact_audit.yaml`
- `tests/unit/test_artifact_audit_models.py`
- `tests/unit/test_artifact_manifest.py`
- `tests/unit/test_npz_summary.py`
- `tests/workflow/test_artifact_audit_from_vggt_scan.py`

## Missing

- `src/tuling_research_plus/vggt/edge_audit.py`
- `src/tuling_research_plus/vggt/markdown_export.py`
- `tests/unit/test_vggt_evidence_edge_audit.py`

## Rename Risk Areas

- Python import paths.
- `pyproject.toml` package discovery.
- Tests imports.
- Skill names and frontmatter.
- MCP server name.
- Docs and contract references.
- Workflow references.

## Validation

Old Round 38 focused tests:

- Evidence Ledger focused tests: passed, 8 tests.
- Artifact Auditor focused tests: passed, 10 tests.
- Name and contract schema checks: passed, 7 tests.
- `tests/unit/test_vggt_evidence_edge_audit.py` not run because the file is
  missing.

## Outcome

Committed to `pre-rename-round38-checkpoint` before any rename work.
