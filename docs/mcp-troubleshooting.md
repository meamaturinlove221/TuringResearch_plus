# MCP Troubleshooting

Status: v0.7 distribution polish.

This page covers local MCP smoke checks only. It does not describe a hosted
service or public marketplace deployment.

## Manifest Command Fails

Run:

```powershell
python -m turing_research.mcp_server --manifest
```

Expected behavior:

- prints JSON to stdout;
- does not start a network service;
- does not require API keys.

If import fails, confirm the package is installed locally:

```powershell
python -m pip install -e .[dev]
```

## Health Check Fails

Run:

```powershell
python -m turing_research.mcp_server --health-check
```

Expected status is `ok`.

## Live Adapter Confusion

Default MCP smoke checks do not use live adapters. Live adapter tests require
explicit opt-in and credentials in a private local environment.

## Plugin Tool Confusion

Plugin registry entries are review metadata. They are not enabled public MCP
tools by default.

Check these defaults:

- `TURINGRESEARCH_ENABLE_PLUGINS=0`
- `TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0`

## Tool Surface Confusion

The stdio MCP tool surface is intentionally small. The capability manifest is a
broader catalog for local helpers, adapters, exporters, and workflows.

Use:

- `docs/mcp-tool-surface.md` for enabled stdio smoke tools;
- `docs/tool-capability-manifest.md` for the broader local capability catalog.
