# PR #2 Post-Merge Test Plan

Round: 394R
Status: test plan

## Purpose

This test plan applies if PR #2 community intake files are merged or
cherry-picked into a target branch.

## Required Checks

1. Confirm the diff is community-docs only:

```powershell
git diff --name-status <base>...HEAD
```

2. Confirm forbidden paths are untouched:

```powershell
git diff --name-only <base>...HEAD -- src tests .github pyproject.toml README.md CHANGELOG.md VERSION
```

Expected result: no output.

3. Run public naming and open-source hygiene checks:

```powershell
python -m pytest tests/contract/test_public_name_integrity_turingresearch.py tests/contract/test_open_source_hygiene_gate.py tests/contract/test_public_release_hygiene.py tests/contract/test_name_integrity.py -q
```

4. Run v1.6 release smoke:

```powershell
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
```

5. Run lint:

```powershell
python -m ruff check .
```

6. Run whitespace check:

```powershell
git diff --check
```

## Manual Review Checklist

- PR #1 is not included.
- Community files are Markdown only.
- No implementation code is included.
- No tests or CI files are changed.
- No release files are changed.
- No secrets, raw data, private logs, copied PDFs/images, or fake results are
  present.
- Intake log credits contributors without exposing private data.
- Templates explain that implementation must be separate.

## Expected Result

PR #2 integration is acceptable only if all checks pass and the diff remains
limited to community documentation intake.
