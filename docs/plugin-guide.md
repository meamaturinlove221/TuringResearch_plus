# Plugin Guide

Status: v0.7 plugin guide.

TuringResearch Plus supports plugin metadata, trusted local manifest loading,
MCP plugin declarations, compatibility checks, and sandbox policy reports.

## What Works

- Manifest validation.
- Trusted local demo plugin loading as metadata.
- Compatibility harness checks.
- MCP registry declarations.
- Capability manifest linkage.
- Sandbox policy and permission-gate reports.

## What Does Not Happen By Default

- Unknown plugin code is not executed.
- Dynamic entry points are not loaded.
- Third-party plugins are not enabled.
- Live networking is not enabled.
- Secret access is forbidden.

## Useful Docs

- [Plugin Architecture](plugin-architecture.md)
- [Trusted Local Plugin Loading](trusted-local-plugin-loading.md)
- [Plugin Sandbox Policy](plugin-sandbox-policy.md)
- [Plugin Compatibility Harness](plugin-compatibility-harness.md)
- [MCP Plugin Registry](mcp-plugin-registry.md)
- [MCP Distribution Guide](mcp-distribution-guide.md)

## Validation

```powershell
python -m pytest tests/workflow/test_v0_7_plugin_system_end_to_end_fake.py -q
```
