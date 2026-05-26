# Round 373 - Scholar Optional Live Smoke

Status: complete

## Objective

Add a Scholar optional live smoke path that keeps fake smoke passing by default
and live smoke skipped unless explicitly enabled with private environment
variables.

## Files

- `docs/scholar-optional-live-smoke.md`
- `examples/scholar_demo/live_smoke/`
- `tests/workflow/test_scholar_fake_smoke.py`
- `tests/live/test_scholar_live_smoke_skipped_by_default.py`
- `lanes/351_scholar_optional_live_smoke.md`
- `lanes/00_master_ledger.md`

## Requirements Covered

- fake smoke pass;
- live skipped by default;
- live requires explicit env;
- no API key in repo;
- no paper download by default;
- no fake citation verified.

## Non-actions

- No live Scholar request was made.
- No network access was required.
- No API key was committed.
- No paper was downloaded.
- No fake citation was marked verified.
- No output was written as observed evidence.

## Validation

- Scholar fake smoke: passed with 3 tests.
- Scholar live smoke skipped: passed with 1 skipped live test selected via `-m live`.
- Scholar live env/skipped policy: passed with 4 tests.
- Privacy/security focused gate: passed with 22 tests.
- Ruff: passed.
- `git diff --check`: passed.
