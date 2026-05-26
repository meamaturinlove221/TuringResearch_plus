# MCP Distribution Guide

Status: v0.7 distribution polish.

This guide describes the local MCP distribution surface for TuringResearch Plus.
It does not publish a package, upload to PyPI, create a GitHub release, or start
a network service.

## Package And Server

- package name: `turingresearch-plus`
- server name: `turingresearch-plus`
- console script: `turingresearch-plus-mcp`
- module entrypoint: `turing_research.mcp_server:main`
- transport: `stdio`

## Install Shape

Local development install:

```powershell
python -m pip install -e .[dev]
```

MCP smoke checks:

```powershell
python -m turing_research.mcp_server --manifest
python -m turing_research.mcp_server --health-check
turingresearch-plus-mcp --manifest
```

These commands are fake/default safe. They do not require real API keys or live
network access.

## Fake Mode

Fake/default mode is the release-safe path:

- local fixtures only;
- live adapters disabled;
- plugin tools disabled by default;
- no third-party plugin execution;
- no secret values in config examples.

Use `.mcp.example.json` as the safe config template.

## Live Mode

Live mode is optional and must be explicitly enabled in a private local config:

- set `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`;
- provide provider credentials outside the repo;
- keep live results labelled as retrieved material, not verified evidence;
- keep plugin live mode disabled unless a future review explicitly enables it.

## Plugin Registry Boundary

The MCP plugin registry describes candidate plugin tool declarations. It does
not register public MCP tools by itself.

- third-party plugin tools are disabled by default;
- live-required plugin tools are disabled by default;
- plugin tools cannot override `core.*`;
- compatibility reports do not enable plugins.

## Tool Manifest Boundary

The actual stdio smoke surface is the minimal MCP tool registry in
`turing_research.tool_registry`.

The capability manifest is broader: it documents local tools, adapters,
exporters, and workflows for routing and release explanation. It is not the
same thing as enabled MCP tools.

## Release Boundary

Round 131 does not publish anything. Public release still needs a clean branch,
maintainer approval, license posture confirmation, and release gate review.
