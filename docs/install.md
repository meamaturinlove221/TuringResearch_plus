# TulingResearch Plus Install Guide

TulingResearch Plus is packaged as `tulingresearch-plus` with Python packages `tuling_research` and `tuling_research_plus`.

## Requirements

- Python 3.11 or newer
- No real API key is required for tests, examples, or local MCP smoke checks
- Optional local PDF conversion uses PyMuPDF through the `pdf` extra

## Editable Install

```powershell
python -m pip install -e .[dev]
```

For local PDF conversion and MCP CLI smoke checks:

```powershell
python -m pip install -e .[dev,pdf,mcp]
```

For all optional local extras:

```powershell
python -m pip install -e .[dev,all]
```

## Console Scripts

The release candidate exposes:

- `tulingresearch-plus`
- `tulingresearch-plus-mcp`

Both scripts point to `tuling_research.mcp_server:main`.

Smoke commands:

```powershell
python -m tuling_research.mcp_server --manifest
python -m tuling_research.mcp_server --health-check
tulingresearch-plus-mcp --manifest
```

## MCP Server

- Server name: `tulingresearch-plus`
- Module: `tuling_research.mcp_server`
- Transport target: STDIO
- Default tests use fake services and local fixtures

The STDIO entry point does not start network services on import and does not write logs to stdout. Human-readable status goes to stderr unless JSON output is explicitly requested.

## Release Boundary

This repository is not published to PyPI in `v0.1.0`. Packaging validation is local only.
