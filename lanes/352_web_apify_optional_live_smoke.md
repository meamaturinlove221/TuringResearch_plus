# Round 374 - Web / Apify Optional Live Smoke

Status: complete

## Objective

Add a Web / Apify optional live smoke path that keeps fake smoke passing by
default and live smoke skipped unless explicitly enabled with private
environment variables.

## Files

- `docs/web-apify-optional-live-smoke.md`
- `examples/apify_workflows/live_smoke/`
- `tests/workflow/test_web_apify_fake_smoke.py`
- `tests/live/test_web_apify_live_smoke_skipped_by_default.py`
- `lanes/352_web_apify_optional_live_smoke.md`
- `lanes/00_master_ledger.md`

## Requirements Covered

- fake smoke pass;
- live skipped by default;
- `APIFY_TOKEN` optional;
- no token in repo;
- no private scraping;
- no login bypass.

## Non-actions

- No live Web request was made.
- No live Apify request was made.
- No network access was required.
- No `APIFY_TOKEN` was committed.
- No private scraping was performed.
- No login bypass was performed.
- No output was written as observed evidence.

## Validation

- Web / Apify fake smoke: passed with 3 tests.
- Web / Apify live smoke skipped: passed with 1 skipped live test selected via `-m live`.
- Apify live env/skipped policy: passed with 4 tests.
- Privacy/security focused gate: passed with 22 tests.
- Ruff: passed.
- `git diff --check`: passed.
