# SFTP Live Skip Report

Status: skipped by default.

Default environment:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
TURINGRESEARCH_SFTP_CREDENTIAL=
TURINGRESEARCH_SFTP_KEY_PATH=<private local key path placeholder>
TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target
```

Result:

- SFTP live disabled by default: pass
- no password in repo: pass
- key path placeholder only: pass
- no remote command: pass
- no remote delete: pass
- transfer target explicit: pass
