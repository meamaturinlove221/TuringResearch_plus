# SFTP Optional Live Smoke

Round: 375
Status: fake smoke ready / live skipped by default

## Objective

Define an SFTP optional live smoke path that keeps fake/local transfer runnable
by default and keeps live transfer skipped unless a maintainer explicitly opts
in with private environment variables.

This round does not open SSH or SFTP connections, require a password, require a
real key path, run remote commands, delete remote files, or write live transfer
output as observed evidence.

## Default Fake Smoke

Default smoke uses local fake transfer only:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
TURINGRESEARCH_SFTP_CREDENTIAL=
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path placeholder>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

Expected result:

- fake smoke pass;
- no password;
- no real key path;
- no remote command;
- no remote delete;
- transfer target explicit;
- all outputs require human review.

## Optional Live Smoke

Private live smoke requires all of the following outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SFTP_LIVE=1
TURINGRESEARCH_SFTP_CREDENTIAL=<private local credential reference>
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

If any flag, credential reference, or reviewed target is missing, the live smoke
test must skip or return a typed blocked report. Skipping is the correct default
behavior.

## Example Files

See `examples/session_runtime/sftp_live_smoke/`:

- `README.md`
- `fake_sftp_smoke.json`
- `expected_fake_smoke_report.md`
- `live_skip_report.md`

## Safety Rules

- live skipped by default;
- live requires explicit env;
- no password in repo;
- no real key path in repo;
- no remote command;
- no remote delete;
- transfer target explicit;
- no automatic Evidence Ledger write;
- no public claim from fake or skipped live output.

## Decision

SFTP optional live smoke is ready for fake/default review. It remains NO-GO for
default SSH/SFTP networking.
