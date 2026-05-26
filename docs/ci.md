# TuringResearch Plus CI

TuringResearch Plus uses GitHub Actions for release-candidate smoke validation.

## Workflows

| Workflow | File | Blocking |
| --- | --- | --- |
| test | `.github/workflows/test.yml` | yes |
| lint | `.github/workflows/lint.yml` | ruff yes, mypy optional |

## Python Matrix

The test workflow runs on:

- Python 3.11
- Python 3.12

## Test Workflow

The `test` workflow installs:

```bash
python -m pip install -e ".[dev,pdf,mcp]"
```

Then runs:

```bash
python -m pytest tests/unit
python -m pytest tests/contract
python -m pytest tests/workflow
python -m pytest
```

The examples job runs workflow tests in fake mode/dry-run mode only.

## Lint Workflow

The `lint` workflow runs:

```bash
python -m ruff check .
```

Mypy runs as an optional non-blocking job:

```bash
python -m mypy src
```

The mypy configuration is intentionally release-candidate friendly: it preserves typed function boundaries while avoiding strict-mode blocking on complex generic or plugin edge cases.

## Secrets Policy

CI does not require or consume real API keys. Do not add repository secrets for default tests. Future live/manual jobs must be opt-in and isolated from the default matrix.
