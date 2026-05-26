# Pod Workflow Replay Fixture

This directory documents the fake/local replay introduced in Round 268.

The replay uses existing public-safe fixtures:

- `examples/session_runtime/preflight_fixture/`
- `examples/session_runtime/context_pack_fixture/source/`
- `examples/session_runtime/return_fixture/`

Generated replay output is written by tests into a temporary directory. It is
not committed here because the replay is reproducible and should not add runtime
churn to the repository.

Safety boundaries:

- fake/demo only;
- no live SSH;
- no remote command execution;
- no automatic Evidence Ledger write;
- no secrets;
- no raw data;
- no restricted model payloads.
