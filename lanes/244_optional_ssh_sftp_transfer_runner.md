# Lane 244 - Optional SSH/SFTP Transfer Runner

Status: completed.

Round: 266.

## Goal

Add a fake-first optional SSH/SFTP transfer runner for session runtime parity
without enabling remote work by default.

## Implemented

- Transfer report models.
- Fake/local transfer runner.
- Optional SFTP opt-in guard.
- Transfer orchestration request.
- Live skipped-by-default test.

## Safety

- Fake mode is default.
- Live SFTP requires `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.
- Credentials are environment-only and not logged.
- No password in repository.
- No remote command execution.
- No remote delete.
- No remote write except explicit transfer target in a later reviewed adapter.
- Path traversal is blocked.
- Human review remains required.

## Outputs

- `src/turing_research_plus/session_runtime/transfer_runner.py`
- `src/turing_research_plus/session_runtime/fake_transfer.py`
- `src/turing_research_plus/session_runtime/sftp_transfer_optional.py`
- `src/turing_research_plus/session_runtime/transfer_report.py`
- `contracts/optional_sftp_transfer_runner.yaml`
- `tests/unit/test_transfer_runner.py`
- `tests/unit/test_fake_transfer.py`
- `tests/unit/test_transfer_report.py`
- `tests/workflow/test_optional_sftp_transfer_fake.py`
- `tests/live/test_optional_sftp_transfer_live_skipped_by_default.py`
- `docs/optional-ssh-sftp-transfer-runner.md`
