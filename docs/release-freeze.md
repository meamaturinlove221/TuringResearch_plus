# TulingResearch Plus Release Freeze

Version: `v0.1.0`

Project: TulingResearch Plus

Packages:

- `tuling_research`
- `tuling_research_plus`

MCP server: `tulingresearch-plus`

## Freeze Status

TulingResearch Plus is in Release Candidate freeze for `v0.1.0`.

Allowed changes after this freeze:

- bug fixes
- tests
- naming fixes
- documentation fixes
- contract fixes
- example fixes
- packaging fixes

Not allowed after this freeze:

- new major workflow features
- default live API execution
- unreviewed namespace changes
- unreviewed schema changes
- unreviewed package structure changes

## v0.1.0 Includes

- Core local tools
- PDF Markdown Phase A
- Semantic Graph fake adapter / dry-run
- Literature Survey dry-run
- Vault / Context basic capabilities
- Race Mode basics
- Feature Capsule skeleton
- DocFlow
- Figure registry
- Paper draft gate
- Contract tests
- Workflow dry-run tests
- Examples fake mode

## v0.1.0 Does Not Include

- real network API execution by default
- heavy OCR
- complex PDF layout parsing
- full automatic paper generation
- real GPU experiment execution
- automatic PyPI publishing
- private or unauthorized source idea implementation

## Frozen Sources Of Truth

- Public API and package structure: `docs/api-freeze-v0.1.0.md`
- MCP tool namespace: `docs/tool-namespace-freeze.md`
- Tool implementation status: `docs/mcp-tools.md`
- Contracts: `contracts/`
- Release gates: `docs/public-release-checklist.md`
- Public README draft: `docs/public-readme-draft.md`
- Master ledger: `lanes/00_master_ledger.md`

## Release Validation

The freeze requires these commands to pass:

```powershell
python -m pytest
python -m ruff check .
python -m mypy src
```

## Naming Lock

All release files must use:

- Project name: TulingResearch Plus
- Core package: `tuling_research`
- Plus package: `tuling_research_plus`
- MCP server: `tulingresearch-plus`
- Skill prefix: `tulingresearch-`
