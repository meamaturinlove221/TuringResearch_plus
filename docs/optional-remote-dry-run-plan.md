# Optional Remote Dry-run Plan

Status: v1.4 production parity planning.

Round: 295.

The Optional Remote Dry-run Plan turns Session runtime preflight and context
pack review into a manual remote pod checklist. It tells a human what would need
to be reviewed before a remote attempt, which files are selected, which files
are excluded, and what return artifacts are required.

It does not connect to a remote machine.

## Output

The generated plan includes:

- preflight result
- files to transfer
- forbidden files excluded
- remote target placeholder
- manual command references
- rollback plan
- return artifact requirements
- human confirmation checklist

## Boundaries

- No SSH.
- No SFTP.
- No tmux.
- No Modal.
- No remote command execution.
- No automatic Evidence Ledger write.
- Dry-run only.
- Human review required.

Manual commands in the plan are comments and references. They are not executed
by TuringResearch.

## Runtime API

```python
from pathlib import Path

from turing_research_plus.session_runtime import (
    RemoteDryRunPlanRequest,
    build_remote_dry_run_plan,
    write_remote_dry_run_plan,
)

plan = build_remote_dry_run_plan(
    RemoteDryRunPlanRequest(
        plan_id="dry-run-demo",
        session_id="session-demo",
        package_id="ctx-demo",
        route_id="route-demo",
        project_root=Path("."),
        context_source=Path("examples/session_runtime/context_pack_fixture/source"),
        output_dir=Path("tmp/session-dry-run"),
    )
)
write_remote_dry_run_plan(plan, Path("tmp/REMOTE_DRY_RUN_PLAN.md"))
```

## Human Confirmation

Before any human-run remote workflow, the operator must confirm:

- preflight is not blocked
- forbidden files are excluded
- remote target is reviewed outside public repo files
- no secrets, raw data, or restricted model payloads are transferred
- manual commands are reviewed by a human
- return artifact requirements are understood
- no automatic Evidence Ledger write will occur
