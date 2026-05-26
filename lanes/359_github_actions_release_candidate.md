# Round 381 - GitHub Actions Release Candidate

Status: complete

## Objective

Strengthen GitHub Actions so they support v1.6 release candidate checks without
publishing.

## Files

- `.github/workflows/ci.yml`
- `.github/workflows/docs-check.yml`
- `.github/workflows/privacy-gate.yml`
- `.github/workflows/release-artifact-dry-run.yml`
- `docs/github-actions-release-candidate-v1.6.md`
- `tests/contract/test_github_actions_release_candidate.py`
- `lanes/359_github_actions_release_candidate.md`
- `lanes/00_master_ledger.md`

## Checks

- CI release-candidate unit/contract/package/install checks.
- Docs build dry-run checks.
- Privacy gate checks.
- Release artifact dry-run checks.
- Live tests skipped by default.

## Safety

- No secrets.
- No API keys.
- No live tests.
- No PyPI publish.
- No GitHub release publish.
- No release artifact upload.
- No tag creation.
- No VGGT access.

## Validation

- Workflow config tests passed.
- Pre-push checks passed.
