# Round 371 - Main Repo Split Link Patch

Status: complete

## Objective

Update the main repository README and split docs to show planned / manual-ready
split repository status without writing nonexistent real URLs.

## Files

- `README.md`
- `docs/future-split-repos.md`
- `docs/split-manual-packs.md`
- `docs/main-repo-split-link-patch-v1.6.md`
- `lanes/349_main_repo_split_link_patch.md`
- `lanes/00_master_ledger.md`

## Requirements Covered

- planned / manual-ready status is clear;
- no fake URL;
- main repository remains the only install entry;
- child repositories are only case/demo spokes;
- star focus stays with the flagship repository.

## Non-actions

- No GitHub repository created.
- No external remote pushed.
- No release created.
- No real child repository URL inserted.
- No install target moved out of the flagship repository.

## Validation

- Docs deployment preflight/gate tests passed with 11 tests.
- URL placeholder tests passed with 6 tests.
- Privacy/release hygiene tests passed with 18 tests.
- Ruff: passed.
- `git diff --check`: passed.
