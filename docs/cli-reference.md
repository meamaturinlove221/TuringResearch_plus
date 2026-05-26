# CLI Reference

Status: v0.5 packaging polish.

TuringResearch Plus exposes local console entrypoints for MCP smoke checks and
manifest inspection.

## Package

- package name: `turingresearch-plus`
- import package: `turing_research`
- import package: `turing_research_plus`

## Console Scripts

- `turingresearch-plus`
- `turingresearch-plus-mcp`
- `turingresearch-session`

The MCP scripts point to:

```text
turing_research.mcp_server:main
```

The Session runtime script points to:

```text
turing_research_plus.session_runtime.cli:main
```

## Local Smoke Commands

```powershell
python -m turing_research.mcp_server --manifest
python -m turing_research.mcp_server --health-check
python -m turing_research_plus.session_runtime.cli report
turingresearch-plus-mcp --manifest
turingresearch-session report
```

These commands do not require live API keys and do not start a network service.

The Session CLI remains fake/dry-run by default. It does not open live SSH, run
remote commands, log secrets, or write Evidence Ledger entries automatically.

## Fake Mode

Default workflows use fake adapters, local fixtures, or dry-run payloads. Live
adapters remain disabled unless the user explicitly opts in with environment
variables and provider credentials.

## Release Boundary

Round 95 does not publish to PyPI, create tags, or push a GitHub release.
