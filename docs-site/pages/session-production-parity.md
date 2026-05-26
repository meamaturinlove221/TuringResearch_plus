# Session Production Parity

TuringResearch v1.4 updates Session parity from structural parity to
production parity. The fake/local chain is runnable end to end, while live
remote behavior remains disabled or opt-in.

## Runnable

- preflight
- context pack
- script export
- fake transfer
- return verifier
- human confirmation
- production E2E replay

## Deferred Or Disabled

- optional live transfer is deferred / opt-in;
- remote execution is disabled;
- SSH / tmux / provision remain outside the default runtime;
- automatic Evidence Ledger write is disabled.

## Safety Boundaries

- live steps disabled by default;
- no remote execution;
- no secrets;
- no raw data;
- no restricted model payloads;
- no automatic observed claim;
- fake/demo returns remain proposed-only.

## Data

The dashboard data lives at:

- `examples/session_runtime/session_production_dashboard_v2.json`

See also:

- `docs/session-production-dashboard-v2.md`
- `docs/session-production-parity-e2e.md`
- `docs/session-cli-surface.md`
- `docs/session-shell-script-equivalent.md`
- `docs/return-import-human-confirmation.md`
