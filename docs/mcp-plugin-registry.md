# MCP Plugin Registry

Status: v0.6 minimal implementation.

Round 110 adds an MCP-facing registry layer for manifest-only plugins. The
registry describes which plugin capabilities could be exposed as MCP tool
declarations, while keeping them disabled and review-gated by default.

## Purpose

The registry records:

- `plugin_id`
- `exposed_tool_name`
- `namespace`
- `input_schema`
- `output_schema`
- `permissions`
- `safety_level`
- `default_enabled`
- `live_required`
- `requires_api_key`
- `fake_mode_supported`

It does not start the MCP server. It does not dynamically load plugin tools.

## Rules

- Third-party plugins must have `default_enabled: false`.
- Live-required plugins must have `default_enabled: false`.
- `requires_api_key` must be explicit.
- Plugin tools cannot override `core.*`.
- Every plugin tool needs a namespace.
- Registry validation requires human review.

## Local Helpers

- command: `turing mcp registry-check`
- local helper: `mcp_plugin_registry_check`
- output: `MCPPluginValidationReport`

- command: `turing mcp registry-md`
- local helper: `mcp_plugin_registry_markdown`
- output: Markdown

These helpers are local Python helpers and are not frozen public MCP APIs.

## Demo Fixture

`examples/plugins/demo_mcp_plugin/registry.yaml`

The fixture exposes a disabled fake/demo tool declaration:

- `mcp.demo_export`

No plugin code is included or executed.

## Limitations

- No marketplace publishing.
- No automatic install.
- No live plugin execution.
- No public MCP tool registration.
- No dynamic Python import.
