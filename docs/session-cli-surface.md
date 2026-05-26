# Session CLI Surface

Status: implemented.

Round: 292.

The Session CLI surface makes the v1.4 Session runtime parity line usable as a
local tool entry point, not just a Python module. It is still fake/dry-run by
default and does not execute remote commands.

## Entrypoint

```text
turingresearch-session = turing_research_plus.session_runtime.cli:main
```

The same CLI can be invoked as:

```powershell
python -m turing_research_plus.session_runtime.cli report
```

## Commands

| Command | Purpose | Default mode |
| --- | --- | --- |
| `session preflight` | Run local context/session preflight checks. | dry-run |
| `session pack` | Build a safe local context pack. | local only |
| `session transfer --fake` | Copy a context pack to a local fake target. | fake only |
| `session verify-return` | Verify a structured fake/remote return package. | review-only |
| `session replay` | Run preflight, pack, fake transfer, fake return, verifier, and proposed update report. | fake replay |
| `session report` | Render the static CLI surface and safety boundaries. | docs/report |

## Safety Boundaries

- live SSH disabled by default;
- no remote command execution;
- no secrets logging;
- no automatic Evidence Ledger write;
- proposed updates only;
- human review required.

## Runtime Meaning

This closes the tool-entry gap for Session parity. It does not make the project
a remote orchestrator. Live SSH/tmux/provision, remote command execution,
automatic cleanup, automatic experiment execution, and automatic evidence
mutation remain out of scope.
