# Plugin Compatibility Test Harness

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Plugin manifests need compatibility checks before they can be documented,
trusted, or considered for MCP exposure.

## 2. Research Motivating Example

A dashboard renderer plugin should prove it declares inputs, outputs,
permissions, fake-mode support, and docs before it is listed as compatible.

## 3. Inputs

- plugin manifest
- MCP plugin mapping
- capability manifest entry
- extension safety report

## 4. Outputs

- PluginCompatibilityReport
- PluginCompatibilityFinding
- PluginCompatibilityMatrix

## 5. Proposed Commands / Tools

- command: `turing plugin compatibility`
- tool: `plugin.compatibility_check`
- output: `PluginCompatibilityReport`

## 6. Related Contracts

- plugin_compatibility_harness.yaml
- plugin_architecture.yaml
- mcp_plugin_registry.yaml
- tool_capability_manifest.yaml

## 7. Related Skills

- turingresearch-architecture-contracts
- turingresearch-qa-release

## 8. Required Tests

- compatibility matrix tests
- missing docs/tests detection
- MCP namespace collision tests

## 9. Risks

- compatibility mistaken for safety approval
- incomplete manifest accepted
- core tool namespace collision

## 10. Done Criteria

- compatibility report is generated
- missing fields become findings
- compatibility does not enable runtime execution

## 11. Non-goals

- no plugin execution
- no automatic registry promotion
- no live service calls
