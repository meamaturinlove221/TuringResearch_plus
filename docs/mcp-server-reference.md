# MCP Server Reference

Status: v0.5 packaging polish.

## Server

- server name: `turingresearch-plus`
- module: `turing_research.mcp_server`
- entrypoint: `turing_research.mcp_server:main`
- transport target: STDIO

## Example Client Config

Use `.mcp.example.json` as a no-secret template. It contains environment
variable names only and keeps live tests disabled by default.

## STDIO Safety

- Importing the MCP module must not start network services.
- Default invocation writes human-readable status to stderr only.
- `--manifest` writes a JSON manifest to stdout.
- `--health-check` writes a JSON health payload to stdout.

## Live Adapter Boundary

Live adapters are opt-in. Missing API keys must not break default tests or local
smoke commands. Live results are retrieved material, not human-verified evidence.

## Public API Boundary

Many v0.2-v0.5 capabilities are local Python helpers or proposed tool surfaces.
They remain documented but are not automatically promoted to public MCP APIs.
