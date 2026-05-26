# Lane 91 - MCP Plugin Registry

Status: implemented minimal.

## Scope

Round 110 implements a manifest-only MCP plugin registry for describing which
plugin capabilities may be exposed as MCP tool declarations.

## Added

- `src/turing_research_plus/mcp_plugins/`
- `contracts/mcp_plugin_registry.yaml`
- `docs/mcp-plugin-registry.md`
- `docs/mcp-plugin-safety.md`
- `examples/plugins/demo_mcp_plugin/registry.yaml`
- MCP plugin unit and workflow tests

## Boundaries

- No MCP server start.
- No dynamic plugin tool loading.
- No third-party code execution.
- Third-party tools default to disabled.
- Live-required tools default to disabled.
- `core.*` overrides are blocked.
