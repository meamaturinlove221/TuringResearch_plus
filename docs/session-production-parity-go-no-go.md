# Session Production Parity Go / No-Go

Round: 299.

## GO

- CLI surface is present and fake/default.
- Script export is runnable and does not execute exported scripts.
- Archive hardening blocks traversal, unsafe dotfiles, unsafe symlinks, and
  checksum mismatch.
- Remote dry-run plan generates manual references only.
- Return confirmation generates human-confirmation packets.
- E2E replay is fake-runnable with no release blockers.
- Dashboard v2 reflects production parity state.
- No unsafe live default is enabled.

## NO-GO

- Default live SSH.
- Default live SFTP.
- tmux attach / provision.
- Remote command execution.
- Automatic remote cleanup.
- Automatic Evidence Ledger write.
- Trusting remote claims as observed evidence.
- Promoting fake/demo output to observed evidence.

## Decision

GO for local fake/default Session production parity.

NO-GO for live remote orchestration until a dedicated live safety design and
review gate exists.
