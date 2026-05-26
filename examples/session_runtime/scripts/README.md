# Session Script Equivalent Demo

Status: fake/demo only.

Round: 293.

This directory contains generated shell script equivalents for the Session
runtime workflow. They are review artifacts and manual references only.

## Scripts

- `preflight.sh`
- `build-context-pack.sh`
- `fake-transfer.sh`
- `verify-return.sh`
- `workflow-replay.sh`

## Safety

- shellcheck-style notes are included;
- live steps are commented and marked manual;
- no secrets are stored here;
- no destructive commands are included;
- no remote command execution is enabled;
- no automatic Evidence Ledger write occurs.

Do not paste credentials into these files. Review before any manual execution.
