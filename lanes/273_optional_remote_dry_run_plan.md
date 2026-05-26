# Round 295 - Optional Remote Dry-run Plan

Status: completed.

Scope:
- Generate a review-only optional remote dry-run plan.
- Include preflight result, files to transfer, excluded forbidden files, remote
  target placeholder, manual command references, rollback plan, return artifact
  requirements, and human confirmation checklist.
- Do not connect to remote machines or execute remote commands.

Implemented:
- `remote_dry_run_plan.py`
- `manual_execution_plan.py`
- `contracts/optional_remote_dry_run_plan.yaml`
- docs, demo, unit tests, and workflow tests.

Safety:
- No SSH.
- No SFTP.
- No tmux.
- No Modal.
- No remote execution.
- No automatic Evidence Ledger write.
- Manual commands are comments and references only.

Validation:
- Dry-run plan tests, security/privacy gate, targeted sensitive scans,
  large-file checks, and whitespace checks were run for Round 295.

Push:
- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
