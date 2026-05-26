# Session Production Parity Remaining Gaps

Round: 299.

These are deliberate gaps after the v1.4 Session production parity gate.

## Deferred

- Optional live transfer remains explicit opt-in.
- Live SSH/SFTP needs a separate live-test design.
- SSH / tmux / provision remains outside the default runtime.
- Automatic remote cleanup remains deferred.
- Remote command execution remains disabled.

## Not Implemented

- A live pod lifecycle manager.
- Credential management for real remote machines.
- Automatic remote process launch.
- Automatic Evidence Ledger mutation.
- Automatic observed claim creation.

## Why These Gaps Remain

The current goal is production parity for a safe local review workflow, not a
remote execution platform. Live remote behavior changes the safety model:
credentials, ownership, cleanup, path scope, data upload, and command execution
all need separate design and review.
