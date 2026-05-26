# Round 370 - Split Repo URL Placeholder Policy

Status: complete

## Objective

Define and enforce split repository URL placeholder policy before any future
manual child repository creation.

## Files

- `docs/split-repo-url-placeholder-policy.md`
- `docs/split-repo-url-update-after-creation.md`
- `tests/contract/test_split_repo_url_placeholders.py`
- `lanes/348_split_repo_url_placeholder_policy.md`
- `lanes/00_master_ledger.md`

## Policy Summary

- Before creation, split repo docs may only use approved placeholders.
- Fake GitHub URLs are forbidden.
- Real URLs may be inserted only after manual repository creation and human
  approval.
- The main README must not imply that planned split repositories already exist.
- Child README files must point back to the flagship TuringResearch repository.
- The main repo linked as flagship placeholder remains required until the real
  URL is approved.

## Allowed Placeholders

- `<approved-real-repository-url>`
- `TuringResearch main repository URL goes here after human publication approval`
- local paths under `split_ready/` and `split_manual/`

## Non-actions

- No GitHub repository created.
- No external remote pushed.
- No release created.
- No real URL inserted.
- No fake GitHub URL added.

## Validation

- URL placeholder and split creation pack tests: passed with 18 tests.
- Privacy gate: passed with 18 focused privacy/release hygiene tests.
- Ruff: passed.
- `git diff --check`: passed.
