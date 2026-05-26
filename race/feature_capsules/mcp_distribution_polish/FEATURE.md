# MCP Distribution Polish

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Public users need clearer MCP installation, smoke-test, and configuration
guidance without requiring live services or real API keys.

## 2. Research Motivating Example

A user should be able to install locally, run MCP smoke checks, inspect the
manifest, and understand fake/default boundaries.

## 3. Inputs

- pyproject metadata
- CLI entrypoints
- MCP server reference
- example MCP config

## 4. Outputs

- MCPDistributionReport
- MCPInstallChecklist
- MCPConfigExampleReport

## 5. Proposed Commands / Tools

- command: `turing mcp doctor`
- tool: `mcp.distribution_doctor`
- output: `MCPDistributionReport`

## 6. Related Contracts

- mcp_distribution_polish.yaml
- mcp_plugin_registry.yaml

## 7. Related Skills

- turingresearch-qa-release
- turingresearch-architecture-contracts

## 8. Required Tests

- entrypoint metadata tests
- config example no-secret tests
- MCP smoke docs tests

## 9. Risks

- install docs imply public hosted service
- examples include credentials
- live adapters become expected by default

## 10. Done Criteria

- install path is documented
- fake/default smoke checks are clear
- examples contain no real secrets

## 11. Non-goals

- no PyPI publication in this capsule
- no hosted MCP service
- no live adapter requirement
