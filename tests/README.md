# TuringResearch Plus Tests

The test suite is split into deterministic local groups:

- `tests/unit/`: local model, service, gate, and utility tests
- `tests/contract/`: MCP, package, namespace, release, and schema integrity tests
- `tests/workflow/`: fake-service and dry-run workflow examples

Default pytest excludes `live` and `manual` markers. The default suite must not require network access, API keys, or private data.

## Commands

```powershell
python -m pytest tests/unit
python -m pytest tests/contract
python -m pytest tests/workflow
python -m pytest
```

## Markers

- `unit`
- `contract`
- `workflow`
- `integration_fake`
- `live`
- `manual`

`live` and `manual` tests are skipped by default through the project pytest configuration.

## Release-Critical Checks

- PDF tests use fixture PDFs.
- Paper draft gate remains blocked without `ExperimentReport`.
- Source Hygiene blocks unsafe implementation ideas.
- Example tests run only in fake mode or dry-run mode.
