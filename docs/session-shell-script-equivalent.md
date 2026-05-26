# Session Shell Script Equivalent Export

Status: implemented.

Round: 293.

This feature exports safe shell script equivalents for the Session runtime
workflow. It borrows the idea of atomic scripts plus SOP from Neocortica-Session
without copying upstream code.

The scripts are generated for human review and optional manual use. They are
not executed by TuringResearch during export.

## Exported Scripts

- `preflight.sh`
- `build-context-pack.sh`
- `fake-transfer.sh`
- `verify-return.sh`
- `workflow-replay.sh`

## Safety Requirements

- shellcheck-style safety notes;
- no secrets;
- no unquoted variables;
- no destructive commands;
- no remote execution by default;
- live steps are commented and marked manual;
- no automatic Evidence Ledger write.

## Runtime Meaning

The scripts call the fake/default Session CLI commands from Round 292. They
serve as operator-facing references for the local workflow:

1. preflight;
2. context pack;
3. fake transfer;
4. return verification;
5. workflow replay.

## Non-goals

- no script execution during export;
- no SSH provisioning;
- no tmux attach;
- no remote command execution;
- no secret injection;
- no automatic data upload;
- no automatic evidence mutation.
