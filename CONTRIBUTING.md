# Contributing To TuringResearch Plus

Thank you for considering a contribution to TuringResearch Plus.

## Ground Rules

- Keep the project name as TuringResearch Plus.
- Keep package names as `turing_research` and `turing_research_plus`.
- Keep the MCP server name as `turingresearch-plus`.
- Keep repo-scoped skill names under the `turingresearch-` prefix.
- Do not add live network behavior to default tests.
- Do not submit private, leaked, NDA, proprietary, or unauthorized source material.
- Do not submit real API keys, credentials, private papers, restricted datasets, or secrets.

## Development Flow

1. Start with contracts for public tool or artifact changes.
2. Add or update Pydantic models.
3. Implement through service protocols or adapters.
4. Add unit, contract, or workflow dry-run tests.
5. Update docs and lane ledgers.

## Local Checks

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m mypy src
```

Default tests must not require real network access or live API keys.

## Public Release Hygiene

Before proposing release-facing changes, check:

- no `.env` file is included;
- no real API key or token is included;
- no `local_project_links.yaml` is included;
- no raw data, restricted dataset, private paper, or private model file is included;
- public examples are fake/demo or fully authorized;
- limitations and evidence boundaries are documented.

## Pull Requests

Use the pull request template and include:

- Scope summary.
- Contract changes.
- Test commands.
- Source Hygiene notes.
- Any release or documentation impact.

## License And Source Hygiene

The current license metadata is proprietary. Do not contribute code copied from incompatible-license projects. Public reference projects may be discussed only as references or inspiration unless a license review explicitly approves reuse.
