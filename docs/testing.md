# TulingResearch Plus Testing Guide

TulingResearch Plus tests are designed to run without real network access, real API keys, private datasets, or live external services.

## Default Command

```powershell
python -m pytest
```

The default pytest configuration excludes `live` and `manual` tests:

```toml
addopts = "-q -m 'not live and not manual'"
```

## Test Groups

| Group | Path or marker | Purpose |
| --- | --- | --- |
| unit | `tests/unit/` or `@pytest.mark.unit` | Local deterministic behavior and Pydantic validation |
| contract | `tests/contract/` or `@pytest.mark.contract` | MCP contracts, package metadata, namespace integrity, release gates |
| workflow | `tests/workflow/` or `@pytest.mark.workflow` | Dry-run and fake-service workflow paths |
| integration_fake | `@pytest.mark.integration_fake` | Integration-style checks using fake adapters and local fixtures only |
| live | `@pytest.mark.live` | Live network or real API credentials; skipped by default |
| manual | `@pytest.mark.manual` | Manual checks; skipped by default |

## Required Release Gates

- Default tests must not use real network access.
- Default tests must not require Semantic Scholar keys, Apify tokens, OpenAI keys, or other external credentials.
- PDF tests must use generated or committed fixture PDFs only.
- Paper draft generation must remain blocked when `ExperimentReport` is absent.
- Source Hygiene must block private, leaked, NDA, proprietary, or incompatible-license implementation ideas.
- Examples must run in fake mode or dry-run mode only.

## Local Matrix

```powershell
python -m pytest tests/unit
python -m pytest tests/contract
python -m pytest tests/workflow
python -m pytest
python -m ruff check .
python -m mypy src
```

## Live Tests

Live tests are not part of the release-candidate default suite. Any future live test must:

- use `@pytest.mark.live`
- document required credentials
- skip automatically when credentials are absent
- avoid writing credentials or tokens into fixtures, docs, logs, or snapshots

Run live tests manually only:

```powershell
python -m pytest -m live
```
