# MCP Plugin Registry



Status: feature capsule draft.



Release target: v0.6 Sprint 2.



## 1. Problem



MCP-facing plugins need a registry format that stays honest about install state, compatibility, and safety.



## 2. VGGT / Research Motivating Example



A local dashboard plugin should declare its MCP tools, fake/live behavior, env vars, and safety level before being shown in docs.



## 3. Upstream / Internal Inspiration



MCP / CLI Packaging Polish and plugin ecosystem planning.



## 4. User Story



As a maintainer, I want a registry index that documents plugin metadata without implying marketplace availability.



## 5. Inputs



- plugin manifests

- tool manifests

- version constraints

- docs links



## 6. Outputs



- MCPPluginRegistry

- RegistryValidationReport



## 7. Data Model



MCPPluginRegistry, MCPPluginEntry, RegistryValidationReport



## 8. Proposed Commands / Tools



- command: `turing mcp registry-check`; tool: `mcp.registry_check`; output: `RegistryValidationReport`



## 9. Related Contracts



- mcp_plugin_registry.yaml

- plugin_architecture.yaml



## 10. Related Skills



- turingresearch-architecture-contracts

- turingresearch-qa-release



## 11. Required Tests



- registry model tests

- registry validation tests

- example registry contract tests



## 12. Risks



- registry drift

- public API overclaiming

- unsafe env vars



## 13. Done Criteria



- registry schema is documented

- entries require docs/tests

- live env vars are optional and disabled by default



## 14. Release Target



v0.6 Sprint 2



## 15. Non-goals



- no marketplace publishing

- no automatic install

- no live plugin execution
