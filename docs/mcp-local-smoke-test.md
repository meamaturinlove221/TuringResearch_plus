# TulingResearch Plus MCP Local Smoke Test

This document records the local STDIO smoke path for the `tulingresearch-plus` MCP server.

## Server

- MCP server name: `tulingresearch-plus`
- Python module: `tuling_research.mcp_server`
- Transport expectation: STDIO
- Default mode: import-safe and network-free

## Minimal Registered Tools

- `core.health_check`
- `core.paper_content`
- `core.web_content`
- `core.session_list`
- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.markdown_content`

Other TulingResearch Plus tools may remain planned, contract-only, stubbed, or dry-run for `v0.1.0`; each public tool is marked with `implementation_status` in `docs/mcp-tools.md`.

## STDIO Safety Rules

- Importing `tuling_research.mcp_server` must not start a network service.
- Default module execution must not write operational logs to stdout.
- Logs and human-readable status messages go to stderr.
- Stdout is reserved for explicit protocol payloads such as `--manifest` or `--health-check`.
- Local smoke tests use dry-run/fake-service behavior and do not require external API keys.

## Local Commands

Run an import and registry smoke test through pytest:

```powershell
python -m pytest tests/contract/test_mcp_server_import.py tests/contract/test_mcp_tool_registry.py tests/contract/test_mcp_stdio_safety.py
```

Print the manifest as an explicit JSON payload:

```powershell
python -m tuling_research.mcp_server --manifest
```

Run the health check as an explicit JSON payload:

```powershell
python -m tuling_research.mcp_server --health-check
```

Start the module without flags to confirm stdout stays empty and the status line goes to stderr:

```powershell
python -m tuling_research.mcp_server
```

## Codex Config Example

See `.codex/config.example.toml`:

```toml
[mcp_servers.tulingresearch-plus]
command = "python"
args = ["-m", "tuling_research.mcp_server"]

[mcp_servers.tulingresearch-plus.env]
TULINGRESEARCH_CACHE_DIR = ".tulingresearch/cache"
TULINGRESEARCH_SESSION_REGISTRY_PATH = ".tulingresearch/session_registry.json"
TULINGRESEARCH_FAKE_SERVICE = "1"
TULINGRESEARCH_API_KEY = "replace-with-local-secret-outside-repo"
```

Do not commit real API keys or private credentials.

## Round 18 Result

The local MCP smoke contract verifies server naming, import safety, registry importability, minimal tool registration, health-check dry-run, and STDIO stdout safety.
