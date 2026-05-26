# Lane 149 - Repo Split Dry-run Exporter

Status: implemented minimal.

Round: 168.

## Goal

Implement a dry-run exporter for future physical repository split candidates.
The exporter writes a local export directory only. It does not create GitHub
repositories, push git remotes, or move source files out of the monorepo.

## Outputs

- `src/turing_research_plus/repo_split/`
- `contracts/repo_split_dry_run.yaml`
- `tests/unit/test_repo_split_models.py`
- `tests/unit/test_repo_split_dry_run_exporter.py`
- `tests/unit/test_repo_split_safety.py`
- `tests/workflow/test_vggt_case_split_dry_run.py`
- `docs/repo-split-dry-run-exporter.md`
- `examples/split_exports/turingresearch-vggt-case/`
- `lanes/00_master_ledger.md`

## Safety Boundary

- Public-safe files only.
- Writes `split_manifest.yaml`.
- Writes `safety_report.md`.
- No secrets.
- No raw data.
- No SMPL-X files.
- No private paths.
- No `git push`.
- No GitHub repository creation.

## Decision

Dry-run export is suitable for review of `turingresearch-vggt-case` skeletons.
It is not approval for physical split or publication.

## Tests

- `tests/unit/test_repo_split_models.py`
- `tests/unit/test_repo_split_dry_run_exporter.py`
- `tests/unit/test_repo_split_safety.py`
- `tests/workflow/test_vggt_case_split_dry_run.py`
