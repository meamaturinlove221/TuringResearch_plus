# Session Parity

TuringResearch v1.3 adds a fake/local Session parity dashboard for the
Neocortica-Session style workflow.

## Fake-Runnable

- preflight
- context pack
- fake transfer
- return verifier
- workflow replay

## Deferred

- optional live transfer remains explicit opt-in;
- remote execution orchestration is deferred;
- SSH / tmux / provision is deferred;
- automatic pod cleanup is deferred.

## Safety Boundaries

- no live SSH by default;
- no remote command execution;
- no automatic Evidence Ledger write;
- no default live network;
- no secrets;
- no raw data;
- no restricted model payloads;
- fake/demo results remain proposed-only.

## Data

The dashboard data lives at:

- `examples/session_runtime/session_parity_dashboard.json`

See also:

- `docs/session-parity-dashboard.md`
- `docs/session-preflight-runner.md`
- `docs/context-pack-builder-runtime.md`
- `docs/optional-ssh-sftp-transfer-runner.md`
- `docs/remote-return-verifier-runtime.md`
- `docs/pod-workflow-replay-runtime.md`
