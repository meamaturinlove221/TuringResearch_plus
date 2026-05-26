# TuringResearch Plus Install Guide

TuringResearch Plus is packaged as `turingresearch-plus` with Python packages
`turing_research` and `turing_research_plus`.

## Requirements

- Python 3.11 or newer.
- No real API key is required for tests, examples, or local MCP smoke checks.
- Optional PDF/PPTX/export helpers are best-effort and skip gracefully when a
  backend is unavailable.

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

- `turingresearch-plus`
- `turingresearch-plus-mcp`

Both scripts point to `turing_research.mcp_server:main`.

Smoke commands:

```powershell
python -m turing_research.mcp_server --manifest
python -m turing_research.mcp_server --health-check
turingresearch-plus-mcp --manifest
```

## MCP Server

- Server name: `turingresearch-plus`
- Module: `turing_research.mcp_server`
- Transport target: STDIO
- Default mode: fake/local

The STDIO entry point does not start network services on import and does not
write logs to stdout. Human-readable status goes to stderr unless JSON output
is explicitly requested.

## Live Features

Live adapters are optional and disabled by default. Do not enable live features
unless the project owner has reviewed credentials, data boundaries, and
network policy.

## Release Boundary

This repository is in public release-candidate review. Installation validation
is local only until maintainers explicitly publish a package.
