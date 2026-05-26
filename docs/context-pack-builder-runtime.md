# Context Pack Builder Runtime

Status: v1.3 local runtime parity.

Round: 265.

The Context Pack Builder turns the earlier session context pack design into a
local, runnable pack builder. It writes a safe review directory and checksum
manifest. It does not transfer files, run commands, connect to a remote
machine, or promote demo output into observed evidence.

## Output

The generated pack contains:

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`
- `HARD_GATES.md`
- `ARTIFACT_REQUIREMENTS.md`
- `FAILURE_TAXONOMY.md`
- `HANDOFF_MANIFEST.yaml`
- `SHA256SUMS.txt`

The builder also writes `CONTEXT_PACK_MANIFEST.md` as a local review report.

## Safety Defaults

- Fake/local mode by default.
- No live network.
- No remote command execution.
- No SSH, tmux, Modal, GPU, or automatic git push.
- No automatic Evidence Ledger write.
- Human review remains required.

## Excluded By Default

- `.env`
- API key or token material
- `local_project_links.yaml`
- raw data paths and raw payloads
- restricted model files
- huge `npz` payloads
- private paths
- hidden dotfiles unless explicitly allowlisted

## Runtime API

```python
from pathlib import Path

from turing_research_plus.session_runtime import (
    ContextPackBuildRequest,
    build_context_pack,
)

manifest = build_context_pack(
    ContextPackBuildRequest(
        package_id="ctx-demo",
        route_id="route-demo",
        source_dir=Path("examples/session_runtime/context_pack_fixture/source"),
        output_dir=Path("tmp/context_pack"),
    )
)
```

The returned manifest lists included files, omitted files, checksums, safety
flags, and missing required files.

## Limits

This is a local builder, not a transfer runner. It does not implement SSH/SFTP,
remote launch, cleanup, or return ingest. Later session runtime rounds may add
fake-first transfer and return verification, but those must stay opt-in and
review-only.
