# Round 375 - SFTP Optional Live Smoke

Status: complete

## Objective

Add an SFTP optional live smoke path that keeps fake/local smoke passing by
default and live smoke skipped unless explicitly enabled with private
environment variables.

## Files

- `docs/sftp-optional-live-smoke.md`
- `examples/session_runtime/sftp_live_smoke/`
- `tests/workflow/test_sftp_fake_smoke.py`
- `tests/live/test_sftp_live_smoke_skipped_by_default.py`
- `lanes/353_sftp_optional_live_smoke.md`
- `lanes/00_master_ledger.md`

## Requirements Covered

- fake smoke pass;
- live skipped by default;
- no password;
- no key path;
- no remote command;
- no remote delete;
- transfer target explicit.

## Non-actions

- No SSH or SFTP connection was opened.
- No remote command was executed.
- No remote delete was performed.
- No password was committed.
- No key path was committed.
- No output was written as observed evidence.

## Validation

- SFTP fake smoke: passed with 3 tests.
- SFTP live smoke skipped: passed with 1 skipped live test selected via `-m live`.
- SFTP live env/skipped policy: passed with 4 tests.
- Privacy/security focused gate: passed with 22 tests.
- Ruff: passed.
- `git diff --check`: passed.
