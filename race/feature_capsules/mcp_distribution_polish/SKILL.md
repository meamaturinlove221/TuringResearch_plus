# MCP Distribution Polish Skill

Status: planning skill draft.

Use this skill for v0.7 MCP install and distribution polish planning. It does
not publish packages or start a hosted service.

## Inputs

- pyproject metadata
- CLI entrypoints
- MCP server reference
- example MCP config

## Outputs

- MCPDistributionReport
- MCPInstallChecklist
- MCPConfigExampleReport

## Safety Rules

- Keep fake/default path first.
- Do not require real API keys.
- Do not require live network access.
- Do not publish or tag.

## Related Contracts

- mcp_distribution_polish.yaml
- mcp_plugin_registry.yaml
