# Lane 112 - MCP Distribution Polish

Status: documentation and contract polish.

Round 131 clarifies the local MCP distribution surface: package metadata,
server name, safe config examples, fake/live boundaries, plugin registry
defaults, and the difference between enabled stdio tools and the broader
capability manifest.

## Outputs

- `docs/mcp-distribution-guide.md`
- `docs/mcp-config-examples.md`
- `docs/mcp-troubleshooting.md`
- `docs/mcp-tool-surface.md`
- `.mcp.example.json`
- `tests/contract/test_mcp_distribution_config.py`
- `tests/contract/test_mcp_tool_surface.py`

## Checks

- MCP server name is `turingresearch-plus`.
- Package name is `turingresearch-plus`.
- Config examples contain no real API key values.
- Fake mode examples are present.
- Live mode is opt-in.
- Plugin tools are disabled by default.
- Tool surface docs match the stdio smoke tool registry.
- Capability manifest relationship is documented.

## Boundaries

- No publishing.
- No PyPI upload.
- No GitHub release.
- No network access.
- No MCP server startup.
- No real credentials.
- No prior project naming.
