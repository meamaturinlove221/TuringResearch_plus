# SFTP Live Optional Example

Status: example only / no password in repo.

This folder documents the private opt-in shape for optional SFTP live transfer.
It does not contain credentials and does not connect to a remote machine.

## Fake Default

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
TURINGRESEARCH_SFTP_CREDENTIAL=
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path placeholder>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

## Private Live Shape

Configure this outside the repository only after human approval:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SFTP_LIVE=1
TURINGRESEARCH_SFTP_CREDENTIAL=<private local credential reference>
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

## Safety

- SFTP live disabled by default;
- no password in repo;
- key path must be placeholder in committed examples;
- no remote command;
- no remote delete;
- transfer target must be explicit;
- path traversal blocked;
- no remote write except a future reviewed explicit transfer target.
