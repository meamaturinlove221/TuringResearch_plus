# Expected Fake SFTP Smoke Report

Status: fake smoke pass.

## Expected Checks

- mode: fake
- no password
- no key path
- no remote command
- no remote delete
- transfer target explicit
- requires human review

## Expected Boundary

The fake smoke report is a local transfer check. It is not a live SFTP transfer,
not a remote command, not a remote delete, and not observed research evidence.
