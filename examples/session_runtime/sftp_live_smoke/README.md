# SFTP Optional Live Smoke Example

Status: fake smoke example / live skipped by default.

This folder contains a public-safe SFTP smoke example. It uses local fake
transfer and does not require network access, password, real key path, remote
command execution, or remote delete.

## Fake Smoke

The fake smoke path reads:

- `fake_sftp_smoke.json`
- `expected_fake_smoke_report.md`

Expected behavior:

- fake smoke pass;
- no password;
- no key path;
- no remote command;
- no remote delete;
- transfer target explicit;
- all output requires human review.

## Live Smoke

Live mode is skipped by default. A private live smoke requires all environment
values to be set outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SFTP_LIVE=1
TURINGRESEARCH_SFTP_CREDENTIAL=<private local credential reference>
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

If any value is missing, the live smoke test must skip or return a typed
blocked report rather than connecting to a remote host.

## Boundary

This example is not a live SFTP transfer, not a remote command workflow, not a
remote delete workflow, and not observed research evidence.
