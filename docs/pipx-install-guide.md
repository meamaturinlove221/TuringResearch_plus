# pipx Install Guide

Round: 379
Status: local install guidance

This guide explains how to validate TuringResearch with `pipx` without
requiring a published PyPI package.

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
python -m pipx install --editable . --include-deps
turingresearch-plus-mcp --health-check
turingresearch-plus-mcp --manifest
```

The distribution name is currently `turingresearch-plus` for compatibility.
The public project name is TuringResearch.

If you need to refresh an existing local pipx environment:

```powershell
python -m pipx uninstall turingresearch-plus
python -m pipx install --editable . --include-deps
```

## Wheel Artifact Install

After a local release-artifact dry-run has produced a wheel under `dist/`, a
human reviewer can install the wheel directly:

```powershell
python -m pipx install --include-deps .\dist\turingresearch_plus-1.5.0rc0-py3-none-any.whl
turingresearch-plus-mcp --health-check
```

The wheel path is a local artifact path. Do not use a package-index install
command until maintainers explicitly publish a package.

## Fake Smoke Command

The minimal fake smoke command is:

```powershell
turingresearch-plus-mcp --health-check
```

Expected result:

- exit code `0`;
- JSON output;
- `status` equals `ok`;
- no live network request;
- no credential prompt;
- no VGGT dependency.

## Cleanup

```powershell
python -m pipx uninstall turingresearch-plus
```

Cleanup does not remove the repository checkout or any manually generated
release artifacts.
