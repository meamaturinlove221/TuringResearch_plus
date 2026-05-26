# Session Parity Dashboard

Status: v1.3 public demo dashboard.

Round: 269.

This dashboard summarizes Neocortica-Session parity in TuringResearch after the
v1.3 session runtime work. It focuses on what can run in fake/local mode and
what remains intentionally deferred.

Data source:

- `examples/session_runtime/session_parity_dashboard.json`

## Runtime Capabilities

| Capability | Status | Runtime surface | Evidence | Boundary |
| --- | --- | --- | --- | --- |
| preflight | fake-runnable | `SessionPreflightRunner` | `docs/session-preflight-runner.md` | local checks only; remote execution disabled |
| context pack | fake-runnable | `ContextPackBuilder` | `docs/context-pack-builder-runtime.md` | safe context files only; secrets and raw data excluded |
| fake transfer | fake-runnable | `FakeTransferRunner` | `docs/optional-ssh-sftp-transfer-runner.md` | local copy only; no live SSH |
| optional live transfer | deferred-live-opt-in | `OptionalSFTPTransferGuard` | `docs/optional-ssh-sftp-transfer-runner.md` | explicit live-test environment gates required |
| return verifier | fake-runnable | `RemoteReturnVerifier` | `docs/remote-return-verifier-runtime.md` | proposed updates only; no automatic ledger write |
| workflow replay | fake-runnable | `PodWorkflowReplayRuntime` | `docs/pod-workflow-replay-runtime.md` | full fake chain; no remote command execution |

## Deferred Remote Execution

- Remote execution orchestration remains deferred.
- SSH / tmux / provision remains deferred.
- Automatic pod cleanup remains deferred.

These are not treated as missing bugs. They are intentionally outside the
default v1.3 runtime because they require live remote ownership, credential
handling, and separate safety review.

## Safety Boundaries

- no live SSH by default;
- no remote command execution;
- no automatic Evidence Ledger write;
- no default live network;
- no secrets in fixtures or reports;
- no raw data in context packs;
- no restricted model payloads;
- fake/demo results remain proposed-only.

## Interpretation

The Session parity surface is now fake-runnable rather than docs-only. It is
not a live remote pod orchestrator. It is a local replay and review surface that
shows the original workflow shape without taking unsafe actions by default.

## Future Roadmap

- full original parity replay gate;
- operator-facing session runtime docs;
- optional live transfer review in a dedicated live-test round.
