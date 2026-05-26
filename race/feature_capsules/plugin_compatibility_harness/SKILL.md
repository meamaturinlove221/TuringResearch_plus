# Plugin Compatibility Test Harness Skill

Status: planning skill draft.

Use this skill for plugin compatibility planning and test design. It validates
metadata expectations only and does not run plugin code.

## Inputs

- plugin manifest
- MCP plugin mapping
- capability manifest entry
- extension safety report

## Outputs

- PluginCompatibilityReport
- PluginCompatibilityFinding
- PluginCompatibilityMatrix

## Safety Rules

- Do not execute plugins.
- Do not promote compatibility to trust.
- Do not allow core tool namespace override.
- Do not require network access.

## Related Contracts

- plugin_compatibility_harness.yaml
- plugin_architecture.yaml
- mcp_plugin_registry.yaml
- tool_capability_manifest.yaml
