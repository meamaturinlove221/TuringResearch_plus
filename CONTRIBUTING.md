# Contributing To TuringResearch

Thank you for considering a contribution to TuringResearch.

## Current License Posture

The current repository metadata is proprietary. Contributions are welcome for
review only after maintainers confirm the contribution path, license posture,
and source hygiene boundary. This document is not legal advice and does not
grant open source rights by itself.

## Naming Boundary

- Use TuringResearch as the public project name.
- Keep compatibility package, console, MCP, and import names unchanged unless a
  dedicated compatibility migration round approves the change.
- Treat compatibility names as runtime surfaces, not as the public brand.

## Fake / Live Boundary

- Default tests must use fake services, fixtures, and dry-run workflows.
- Do not add live network behavior to default tests.
- Do not require API keys, tokens, SSH, SFTP, Modal, GPU services, or remote
  machines for default checks.
- Do not mark fake/demo/planned output as observed evidence.
- Do not make remote command execution a default behavior.

## No Private Data

Do not submit:

- real API keys, credentials, private SSH keys, or tokens;
- `.env` files with real values;
- `local_project_links.yaml`;
- raw data or private datasets;
- private papers or restricted datasets;
- private local paths;
- restricted model payloads;
- private advisor feedback;
- unsupported experiment success claims.

## Development Flow

1. Start with contracts for public tool or artifact changes.
2. Add or update typed models where appropriate.
3. Implement through local services, adapters, or deterministic workflows.
4. Add unit, contract, or workflow dry-run tests.
5. Update docs and lane ledgers.
6. Keep public-facing prose honest about planned, fake, live, and observed
   states.

## Local Checks

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m mypy src
```

## Public Release Hygiene

Before proposing release-facing changes, check:

- no `.env` file is included;
- no real API key or token is included;
- no `local_project_links.yaml` is included;
- no raw data, restricted dataset, private paper, or private model file is
  included;
- public examples are fake/demo or fully authorized;
- limitations and evidence boundaries are documented;
- Source Hygiene blocks unsafe or unauthorized source material.

## Pull Requests

Use the pull request template and include:

- scope summary;
- contract changes;
- test commands;
- Source Hygiene notes;
- privacy/data impact;
- release or documentation impact.

## License And Source Hygiene

Do not contribute code copied from incompatible-license projects. Public
reference projects may be discussed only as references or inspiration unless a
license review explicitly approves reuse.
