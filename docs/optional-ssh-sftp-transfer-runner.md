# Optional SSH/SFTP Transfer Runner

Status: v1.3 fake-first runtime parity.

Round: 266.

The Optional SSH/SFTP Transfer Runner adds a transfer step after local session
preflight and context pack generation. Default behavior is fake/local transfer.
It does not connect to a remote host unless live mode is explicitly enabled.

## Default Fake Mode

Fake mode copies safe context pack files from a local source directory to a
local target directory and returns a `TransferReport`.

It is useful for testing the handoff shape without network access, credentials,
or remote writes.

## Optional Live SFTP

Live SFTP remains guarded:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` is required.
- `TURINGRESEARCH_SFTP_CREDENTIAL` is required.
- A project-specific reviewed adapter is still required before real transfer.

Without the explicit opt-in and credential, the runner returns a typed skip
status instead of connecting.

## Safety Rules

- Fake mode is the default.
- No password or credential is stored in the repository.
- Secrets are not logged in reports.
- No remote command execution.
- No remote delete.
- No remote write except an explicit transfer target in a later reviewed live
  adapter.
- Path traversal is blocked before any optional transfer path.
- Human review remains required.

## Runtime API

```python
from pathlib import Path

from turing_research_plus.session_runtime import (
    TransferRunnerRequest,
    run_transfer,
)

report = run_transfer(
    TransferRunnerRequest(
        transfer_id="tx-demo",
        package_id="ctx-demo",
        source_dir=Path("tmp/context_pack"),
        target="tmp/fake_transfer_target",
    )
)
```

## Non-goals

- No SSH provision.
- No tmux attach.
- No remote command execution.
- No remote delete.
- No automatic experiment execution.
- No automatic Evidence Ledger write.
- No default live network.
