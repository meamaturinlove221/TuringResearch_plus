# Round 293 - Session Shell Script Equivalent Export

Status: completed.

Scope:
- Export safe shell script equivalents for Session runtime parity.
- Provide atomic script references and SOP.
- Do not execute scripts during export.

Exported scripts:
- `preflight.sh`
- `build-context-pack.sh`
- `fake-transfer.sh`
- `verify-return.sh`
- `workflow-replay.sh`

Safety:
- shellcheck-style notes included.
- No secrets.
- No unquoted variables.
- No destructive commands.
- No remote execution by default.
- Live steps are commented and marked manual.
- No automatic Evidence Ledger write.

Validation:
- Script export tests and security gate were run.

Push:
- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
