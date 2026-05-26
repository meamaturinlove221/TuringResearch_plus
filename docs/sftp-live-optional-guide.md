# SFTP Live Optional Guide

Status: optional live polish.

Round: 347.

SFTP live transfer is optional, private, and disabled by default. The default
Session transfer path remains fake/local and requires no SSH host, password,
private key, remote machine, or network access.

## Default Fake Mode

Default mode is fake/local:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
TURINGRESEARCH_SFTP_CREDENTIAL=
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path placeholder>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

The key path is a placeholder only. Do not commit a real key path if it reveals
private filesystem layout.

## Optional Live Mode

Private live mode requires explicit opt-in outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SFTP_LIVE=1
TURINGRESEARCH_SFTP_CREDENTIAL=<private local credential reference>
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

Live transfer still requires a project-specific reviewed adapter before any
real transfer is allowed.

## Safety Boundaries

- SFTP live disabled by default;
- no password in repo;
- key path must be placeholder in committed examples;
- no remote command;
- no remote delete;
- transfer target must be explicit;
- no broad root target;
- path traversal blocked;
- secrets must not be logged;
- human review required.

## Test Policy

- fake/local transfer tests run by default;
- live SFTP tests are skipped by default;
- explicit live env and credential reference are required before any live test;
- current optional SFTP transfer returns typed skip/block reports instead of
  opening a network connection.
