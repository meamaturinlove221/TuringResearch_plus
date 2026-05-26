# Session Preflight Runner

Status: implemented.

Round: 264.

The Session Preflight Runner is a local-only v1.3 Session runtime parity
surface. It checks whether a context source is safe to package for a later
session handoff.

It does not execute remote commands.

## What It Checks

- project root exists;
- context source exists;
- output directory stays under project root and has a safe path;
- forbidden files are absent;
- memory policy is valid;
- platform compatibility is recorded;
- shell metacharacter risk is blocked;
- secret-like assignments are blocked;
- raw data paths are blocked unless explicitly allowed;
- remote execution is disabled by default.

## Local API

- `SessionPreflightRequest`
- `SessionPreflightReport`
- `run_session_preflight(request)`
- `run_session_environment_checks(request, lookup)`
- `build_session_lookup_record(request)`
- `render_session_preflight_report(report)`

## Safety Boundary

- local only;
- no SSH;
- no tmux;
- no remote command execution;
- no Modal or GPU call;
- no automatic git push;
- no automatic Evidence Ledger write;
- proposed updates only;
- human review required.

## Fixture

The fake/demo fixture lives under:

`examples/session_runtime/preflight_fixture/`

It contains:

- `context/PROJECT_CONTEXT.md`
- `context/MEMORY.md`
- `context/ROUTE_SPEC.yaml`
- `output/.gitkeep`

The fixture is public-safe and contains no private data or real credentials.

## Runtime Interpretation

This runner moves Session parity from docs-only policy toward a fake/default
runnable preflight. It is still not a complete pod runtime.

The next session runtime pieces are transfer and return verification, each with
separate fake-first safety gates.
