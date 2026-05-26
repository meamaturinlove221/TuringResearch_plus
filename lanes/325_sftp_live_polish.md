# Lane 325 - SFTP Live Polish

Round: 347.

Status: complete.

## Objective

Polish optional SFTP live transfer documentation, example configuration, and
skipped tests without connecting to a remote host.

## Files

- `docs/sftp-live-optional-guide.md`
- `examples/session_runtime/sftp_live_optional/`
- `tests/live/test_sftp_live_skipped_by_default.py`
- `tests/contract/test_sftp_live_env_policy.py`

## Result

SFTP live remains optional and disabled by default. Fake/local transfer remains
the default path.

## Safety Boundaries

- SFTP live disabled by default.
- No password in repo.
- Key path must be placeholder in committed examples.
- No remote command.
- No remote delete.
- Transfer target must be explicit.
- No connection to remote host in this round.
