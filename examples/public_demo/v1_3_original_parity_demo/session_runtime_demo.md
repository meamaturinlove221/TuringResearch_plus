# Session Runtime Demo

Status: fake/demo only.

This page summarizes the v1.3 Neocortica-Session parity path.

## Replay Chain

1. Session preflight checks local project context.
2. Context pack builder creates a safe local pack.
3. Fake transfer copies the pack locally.
4. Fake pod return fixture represents returned output.
5. Remote return verifier checks required files and checksums.
6. Proposed ingest report remains proposed-only.

## Demonstrated Surfaces

- preflight works;
- context pack works;
- fake transfer works;
- live transfer is skipped by default;
- return verifier works;
- workflow replay works;
- session parity dashboard works.

## Boundaries

- no live SSH by default;
- no remote command execution;
- no SSH/tmux/provision by default;
- no automatic cleanup;
- no automatic Evidence Ledger write;
- no raw data in context pack;
- no restricted model payloads;
- human review required.
