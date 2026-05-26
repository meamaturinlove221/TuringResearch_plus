# MCP Plugin Safety

Status: active policy draft.

## Registry Boundary

The MCP plugin registry is a declaration layer. It is not a runtime loader.

## Required Safety Properties

- Plugin code is not loaded.
- MCP server is not started during validation.
- Third-party tools are disabled by default.
- Live-required tools are disabled by default.
- API key requirements are explicit.
- Plugins cannot override `core.*` tools.
- Namespaces must be explicit and match the exposed tool name.

## Review Rule

Moving a plugin tool from disabled to enabled requires maintainer review, test
coverage, docs, and a safety decision. A valid registry entry is not permission
to execute plugin code.
