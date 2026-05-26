# uv Install Guide

Round: 379
Status: local install guidance

This guide explains how to validate TuringResearch with `uv` without requiring a
published PyPI package.

## Boundary

- No PyPI package is required.
- No PyPI publication is performed.
- No API key is required.
- No VGGT data, local VGGT checkout, raw data, or restricted model file is
  required.
- Live adapters remain disabled by default.
- This guide validates local package entry points only.

## Local Editable Install

Run from the repository root:

```powershell
uv venv .venv
.\.venv\Scripts\Activate.ps1
uv pip install -e .[dev]
python -m turing_research.mcp_server --health-check
python -m turing_research.mcp_server --manifest
```

For a smaller smoke-only environment, install the local package without the
`dev` extra:

```powershell
uv pip install -e .
python -m turing_research.mcp_server --health-check
```

## Wheel Artifact Install

After a local release-artifact dry-run has produced a wheel under `dist/`, a
human reviewer can install the wheel directly:

```powershell
uv venv .venv-wheel
.\.venv-wheel\Scripts\Activate.ps1
uv pip install .\dist\turingresearch_plus-1.5.0rc0-py3-none-any.whl
python -m turing_research.mcp_server --health-check
```

The wheel path is a local artifact path. Do not use a package-index install
command until maintainers explicitly publish a package.

## Fake Smoke Command

The minimal fake smoke command is:

```powershell
python -m turing_research.mcp_server --health-check
```

Expected result:

- exit code `0`;
- JSON output;
- `status` equals `ok`;
- no live network request;
- no credential prompt;
- no VGGT dependency.

## Test Command

```powershell
python -m pytest tests/workflow/test_install_smoke_fake.py -q
```

The test command runs against the local checkout and does not install or publish
a package.
